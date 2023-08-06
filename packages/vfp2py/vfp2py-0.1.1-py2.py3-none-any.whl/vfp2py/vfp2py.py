# coding=utf-8
from __future__ import absolute_import, division, print_function

import sys
import logging
import os
import ntpath
import time
import re
import tempfile
import shutil
import tokenize
import io
from contextlib import contextmanager

import dbf

import antlr4

import autopep8

from .VisualFoxpro9Lexer import VisualFoxpro9Lexer
from .VisualFoxpro9Parser import VisualFoxpro9Parser
from .VisualFoxpro9Visitor import VisualFoxpro9Visitor

from .vfp2py_convert_visitor import PythonConvertVisitor, CodeStr
from . import vfpfunc

SEARCH_PATH = ['.']
INCLUDE = {}

WHICH_CACHE = {}
def which(filename):
    '''find file on path'''
    if filename.lower() in WHICH_CACHE:
        return WHICH_CACHE[filename.lower()]
    for path in filter(None, SEARCH_PATH):
        testpath = os.path.join(path, filename)
        if os.path.isfile(testpath):
            WHICH_CACHE[filename.lower()] = testpath
            return testpath
    for path in filter(None, SEARCH_PATH):
        files = os.listdir(path)
        for file in files:
            if filename.lower() == file.lower():
                testpath = os.path.join(path, file)
                WHICH_CACHE[filename.lower()] = testpath
                return testpath
    return filename


@contextmanager
def temporary_change_to_file_dir(filename):
    olddir = os.path.abspath(os.curdir)
    newdir = os.path.abspath(os.path.dirname(filename))
    if newdir != olddir:
        os.chdir(newdir)
    try:
        yield
    finally:
        if newdir:
            os.chdir(olddir)


class PreprocessVisitor(VisualFoxpro9Visitor):
    def __init__(self, encoding):
        self.tokens = None
        self.memory = {}
        self.encoding = encoding

    def visitPreprocessorCode(self, ctx):
        return self.visit(ctx.preprocessorLines())

    def visitPreprocessorLines(self, ctx):
        lines = []
        for line in ctx.preprocessorLine():
            lines += self.visit(line)
        return lines

    def visitPreprocessorDefine(self, ctx):
        name = ctx.identifier().getText().lower()
        namestart, _ = ctx.identifier().getSourceInterval()
        _, stop = ctx.getSourceInterval()
        tokens = ctx.parser._input.tokens[namestart+1:stop]
        while len(tokens) > 0 and tokens[0].type == ctx.parser.WS:
            tokens.pop(0)
        while len(tokens) > 0 and tokens[-1].type in (ctx.parser.WS, ctx.parser.COMMENT):
            tokens.pop()
        self.memory[name] = tokens
        return []

    def visitPreprocessorUndefine(self, ctx):
        name = ctx.identifier().getText().lower()
        self.memory.pop(name)
        return []

    def visitPreprocessorInclude(self, ctx):
        visitor = PythonConvertVisitor('')
        visitor.scope = {}
        TreeCleanVisitor().visit(ctx.specialExpr())
        filename = visitor.visit(ctx.specialExpr())
        if isinstance(filename, CodeStr):
            filename = eval(filename)
        filename = which(filename)
        if filename in INCLUDE:
            include_visitor = INCLUDE[filename]
        else:
            import ntpath
            if os.path is not ntpath:
                filename = filename.replace(ntpath.sep, os.path.sep)
            include_visitor = preprocess_file(filename, self.encoding)
            INCLUDE[filename] = include_visitor
        self.memory.update(include_visitor.memory)
        return include_visitor.tokens

    def visitPreprocessorIf(self, ctx):
        if ctx.IF():
            ifexpr = ''.join(x.text for x in self.replace_define_tokens(ctx.expr()))
            run = repr(prg2py_after_preproc(ifexpr, 'expr', ''))
            try:
                ifexpr = eval(run, vfpfunc.vfp_sys.__globals__)
            except Exception as err:
                raise Exception('Failed to evaluate preprocessor IF expr {!r}'.format(ctx.expr().getText()))
        else:
            name = ctx.identifier().getText().lower()
            ifexpr = name in self.memory
        if ifexpr:
            return self.visit(ctx.ifBody)
        elif ctx.ELSE():
            return self.visit(ctx.elseBody)
        else:
            return []

    def replace_define_tokens(self, ctx):
        start, stop = ctx.getSourceInterval()
        hidden_tokens = ctx.parser._input.getHiddenTokensToLeft(start)
        retval = []
        process_tokens = (hidden_tokens if hidden_tokens else []) + ctx.parser._input.tokens[start:stop+1]
        hidden_tokens = []
        for tok in process_tokens:
            if tok.text.lower() in self.memory:
                retval += self.memory[tok.text.lower()]
            else:
                if tok.type == ctx.parser.COMMENT:
                    tok.text = '*' + tok.text[2:] + '\n'
                    hidden_tokens.append(tok)
                    continue
                retval.append(tok)
        return hidden_tokens + retval

    def visitNonpreprocessorLine(self, ctx):
        return self.replace_define_tokens(ctx)

def add_indents(struct, num_indents):
    retval = []
    for item in struct:
        if isinstance(item, list):
            retval.append(add_indents(item, num_indents+1))
        elif item:
            retval.append(' '*4*num_indents + repr(item))
        else:
            retval.append('')
    return '\n'.join(retval)

def contains_exceptions(ctx):
    return (isinstance(ctx, ctx.parser.AtomExprContext) and ctx.trailer() and isinstance(ctx.trailer(), ctx.parser.FuncCallTrailerContext)) or \
           isinstance(ctx, ctx.parser.ConstantExprContext) or \
           isinstance(ctx, ctx.parser.SubExprContext) or \
           any(contains_exceptions(c) for c in ctx.children if isinstance(c, ctx.parser.ExprContext))

class TreeCleanVisitor(VisualFoxpro9Visitor):
    def visitSpecialExpr(self, ctx):
        if ctx.pathname():
            return

        start, stop = ctx.getSourceInterval()
        stream = ctx.parser._input
        tokens = stream.tokens[start:stop+1]

        if not (any(tok.type == ctx.parser.WS for tok in tokens) or contains_exceptions(ctx)):
            stream.seek(start)
            ctx.removeLastChild()
            pathname = VisualFoxpro9Parser(stream).pathname()
            ctx.addChild(pathname)
            pathname.stop = stream.tokens[stop]
            while pathname.children and pathname.children[-1].getSourceInterval()[0] > stop:
                pathname.removeLastChild()

        self.visitChildren(ctx)

    def visitSubExpr(self, ctx):
        self.visit(ctx.expr())
        if isinstance(ctx.expr(), ctx.parser.SubExprContext):
            ctx.removeLastChild()
            newexpr = ctx.expr().expr()
            ctx.removeLastChild()
            ctx.addChild(newexpr)

    def visitPower(self, ctx):
        self.visitChildren(ctx)
        left, right = ctx.expr()
        if isinstance(right, ctx.parser.SubExprContext) and isinstance(right.expr(), ctx.parser.PowerContext):
            ctx.removeLastChild()
            right = right.expr()
            ctx.addChild(right)
        if isinstance(left, ctx.parser.PowerContext):
            newleft = ctx.parser.SubExprContext(ctx.parser, ctx.parser.ExprContext(ctx.parser, ctx))
            newleft.addChild(left)
            while ctx.children:
                ctx.removeLastChild()
            ctx.addChild(newleft)
            ctx.addChild(right)

    def visitUnaryNegation(self, ctx):
        self.visit(ctx.expr())
        if ctx.op.type == ctx.parser.MINUS_SIGN and isinstance(ctx.expr(), ctx.parser.UnaryNegationContext):
            ctx.expr().op.type = ctx.parser.PLUS_SIGN
            ctx.op.type = ctx.parser.PLUS_SIGN

def preprocess_code(data, encoding):
    input_stream = antlr4.InputStream(data)
    lexer = VisualFoxpro9Lexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = VisualFoxpro9Parser(stream)
    tree = run_parser(stream, parser, 'preprocessorCode')
    visitor = PreprocessVisitor(encoding)
    visitor.tokens = visitor.visit(tree)
    return visitor

def preprocess_file(filename, encoding):
    with open(filename, 'r', encoding=encoding) as fid:
        data = fid.read()
    with temporary_change_to_file_dir(filename):
        return preprocess_code(data, encoding)

def convert_prg(infile, outfile, encoding):
    if os.path.isdir(outfile):
        basename, file_ext = os.path.splitext(os.path.basename(infile))
        file_ext = file_ext.lower()
        suffix = '' if file_ext == '.prg' else file_ext.replace('.', '_')
        outfile = os.path.join(outfile, basename + '.py')
    if os.path.isfile(outfile):
        raise Exception('File {} already exists'.format(outfile))
    tokens = preprocess_file(infile, encoding).tokens
    data = 'procedure _program_main\n' + ''.join(token.text.replace('\r', '') for token in tokens)
    with tempfile.NamedTemporaryFile(suffix='.prg') as fid:
        pass
    with open(fid.name, 'wb') as fid:
        fid.write(data.encode('cp1252'))
    output = prg2py_after_preproc(data, 'prg', os.path.splitext(os.path.basename(infile))[0])
    with open(outfile, 'wb') as fid:
        fid.write(('# coding=utf-8\n# runtime=vfp2py\n\n' + output).encode('utf-8'))

def find_file_ignore_case(filename, directories):
    for directory in directories:
        for testfile in os.listdir(directory):
            if testfile.lower() == filename.lower():
                return os.path.join(directory, testfile)

def memo_filename(filename, ext):
    directory = os.path.dirname(filename) or '.'
    basename = os.path.basename(filename)
    memofile = os.path.splitext(basename)[0] + '.' + ext
    return find_file_ignore_case(memofile, [directory])

def copy_obscured_dbf(filename, memo_ext, dbf_basename):
    memofile = memo_filename(filename, memo_ext)
    dbffile = dbf_basename + '.dbf'
    shutil.copy(filename, dbffile)
    if memofile:
        shutil.copy(memofile, dbf_basename + '.fpt')
    return dbffile

def split_vcx_props(props):
    while props:
        try:
            prop, props = props.split(' = ', 1)
        except ValueError:
            break
        if props:
            if props.startswith('\x01'):
                some_kind_of_length = re.match('(\x01*\s*([0-9]+))', props).groups()
                l1 = len(some_kind_of_length[0])
                l2 = int(some_kind_of_length[1])
                value = props[l1:l1 + l2]
                _, props = props[l1 + l2:].split('\r\n', 1)
            else:
                value, props = props.split('\r\n', 1)
        else:
            value = ''
        yield prop, value

def convert_vcx(infile, outfile, encoding):
    origoutfile = outfile
    if os.path.isdir(outfile):
        basename = os.path.splitext(os.path.basename(infile))[0]
        outfile = os.path.join(outfile, basename + '_vcx.py')
    if os.path.isfile(outfile):
        raise Exception('File {} already exists'.format(outfile))
    with tempfile.NamedTemporaryFile() as tmpfile:
        pass
    tmpfile = tmpfile.name
    dbffile = copy_obscured_dbf(infile, 'vct', tmpfile)

    codes = []
    with dbf.Table(dbffile) as table:
        for record in table:
            code = '\n'.join('#include "{}"'.format(x) for x in record.reserved8.splitlines()) + '\n'
            if not (record.objname and record['class']):
                continue
            code += 'DEFINE CLASS {} AS {}\n'.format(record.objname, record['class'])
            props = []
            for prop, value in split_vcx_props(record.properties):
                if not prop:
                    props.append('')
                    continue
                if not value:
                    value = '""'
                elif re.match(r'^[0-9]*,[0-9]*,[0-9]*$', value):
                    value = 'RGB({})'.format(value)
                elif re.match(r'^\(.*\)$', value):
                    pass
                else:
                    if value.startswith('-'):
                        input_stream = antlr4.InputStream(value[1:])
                    else:
                        input_stream = antlr4.InputStream(value)
                    lexer = VisualFoxpro9Lexer(input_stream)
                    stream = antlr4.CommonTokenStream(lexer)
                    parser = VisualFoxpro9Parser(stream)
                    parser._interp.PredictionMode = antlr4.PredictionMode.SLL
                    parser.removeErrorListeners()
                    parser._errHandler = antlr4.error.ErrorStrategy.BailErrorStrategy()
                    try:
                        tree = parser.constant()
                        TreeCleanVisitor().visit(tree)
                        output_tree = PythonConvertVisitor('').visit(tree)
                    except:
                        if '"' not in value:
                            format_string = '"{}"'
                        else:
                            if "'" not in value:
                                format_string = "'{}'"
                            else:
                                if '[' not in value and ']' not in value:
                                    format_string = '[{}]'
                                else:
                                    format_string = '{}'
                        value = format_string.format(value)

                props.append('{} = {}'.format(prop.strip(), value))

            code += '\n'.join(props) + '\n\n'
            code += '\n'.join(record.methods.splitlines()) + '\n'
            code += 'ENDDEFINE\n\n'
            codes.append(code)

    os.remove(table.filename)
    os.remove(table.memoname)

    if os.path.isdir(origoutfile):
        basename = os.path.splitext(os.path.basename(infile))[0]
        with open(os.path.join(origoutfile, basename + '_vcx.prg'), 'w', encoding=encoding) as fid:
            for data in codes:
                fid.write(data)
    datas = codes
    with temporary_change_to_file_dir(infile):
        tokens = [token for data in datas for token in preprocess_code(data, encoding).tokens]
    data = 'procedure _program_main\n' + ''.join(token.text.replace('\r', '') for token in tokens)
    with tempfile.NamedTemporaryFile(suffix='.prg') as fid:
        pass
    with open(fid.name, 'wb') as fid:
        fid.write(data.encode('cp1252'))
    output = prg2py_after_preproc(data, 'prg', os.path.splitext(os.path.basename(infile))[0])
    with open(outfile, 'wb') as fid:
        fid.write(('# coding=utf-8\n# runtime=vfp2py\n\n' + output).encode('utf-8'))

def convert_scx(infile, outfile, encoding):
    if os.path.isdir(outfile):
        basename = os.path.splitext(os.path.basename(infile))[0]
        outfile = os.path.join(outfile, basename + '_scx.py')
    if os.path.isfile(outfile):
        raise Exception('File {} already exists'.format(outfile))
    with tempfile.NamedTemporaryFile() as tmpfile:
        pass
    tmpfile = tmpfile.name
    dbffile = copy_obscured_dbf(infile, 'sct', tmpfile)

    table = dbf.Table(dbffile)
    table.open()

    children = [list() for record in table]
    names = [record.objname for record in table]
    for record in table:
        if record['class'].lower() == 'form':
            form = record.objname
        parent = record.parent
        if not parent:
            continue
        parent_ind = names.index(parent)
        children[parent_ind].append(record)

    code = [l.format(form, form) for l in ('local {}', '{} = createObject("{}")', '{}.show()')]
    for record, child in zip(table, children):
        if not record.objname or record.parent or record['class'].lower() == 'dataenvironment':
            continue

        code.append('DEFINE CLASS {} AS {}'.format(record.objname, record['class']))
        subcode = []
        for line in record.properties.split('\r\n'):
            if line:
                prop, value = line.split('=')
                prop = prop.strip()
                value = value.strip()
                if prop == 'Picture':
                    value = '"{}"'.format(value)
                elif prop.endswith('Color'):
                    value = 'RGB({})'.format(value)
                line = ' = '.join((prop, value))
            subcode.append(line)
        for child_record in child:
            subcode.append('ADD OBJECT {} AS {}'.format(child_record.objname, child_record['class']))
            for line in child_record.properties.split('\r\n'):
                line = line.strip()
                if not line:
                    continue
                prop, value = line.split('=')
                prop = prop.strip()
                value = value.strip()
                if prop == 'Picture':
                    value = '"{}"'.format(value)
                elif prop.endswith('Color'):
                    value = 'RGB({})'.format(value)
                subcode.append(child_record.objname + '.' + prop + ' = ' + value)
            subcode.append('')

        for line in record.methods.split('\r\n'):
            subcode.append(line)
        subcode.append('')
        for child_record in child:
            for line in child_record.methods.split('\r\n'):
                if not line:
                    continue
                line = re.sub(r'PROCEDURE ', 'PROCEDURE {}.'.format(child_record.objname), line)
                subcode.append(line)
            subcode.append('')
        code.append(subcode)
        code.append('ENDDEFINE')
        code.append('')

    def add_indent(code, level):
        retval = ''
        for line in code:
            if isinstance(line, list):
                retval += add_indent(line, level+1)
            else:
                retval += '   '*level + line + '\n'
        return retval

    table.close()
    os.remove(table.filename)
    os.remove(table.memoname)

    code = add_indent(code, 0)

    code = re.sub(r'(\n\s*)+\n+', '\n\n', code)
    data = code
    with temporary_change_to_file_dir(infile):
        tokens = preprocess_code(data, encoding).tokens
    data = 'procedure _program_main\n' + ''.join(token.text.replace('\r', '') for token in tokens)
    with tempfile.NamedTemporaryFile(suffix='.prg') as fid:
        pass
    with open(fid.name, 'wb') as fid:
        fid.write(data.encode('cp1252'))
    output = prg2py_after_preproc(data, 'prg', os.path.splitext(os.path.basename(infile))[0])
    with open(outfile, 'wb') as fid:
        fid.write(('# coding=utf-8\n# runtime=vfp2py\n\n' + output).encode('utf-8'))

def find_full_path(pathname, start_directory):
    name_parts = ntpath.split(pathname)
    while ntpath.split(name_parts[0])[1]:
        name_parts = ntpath.split(name_parts[0]) + name_parts[1:]
    pathname = start_directory
    for part in name_parts:
        if part in ('..', '.', ''):
            pathname = os.path.abspath(os.path.join(pathname, part))
            continue
        next_part = find_file_ignore_case(part, [pathname])
        if next_part is None:
            badind = name_parts.index(part)
            return os.path.join(pathname, *name_parts[badind:]), True
        pathname = next_part
    return pathname, False

def read_vfp_project(pjxfile):
    directory = os.path.dirname(pjxfile)
    with tempfile.NamedTemporaryFile() as tmpfile:
        pass
    tmpfile = tmpfile.name
    dbffile = copy_obscured_dbf(pjxfile, 'pjt', tmpfile)

    table = dbf.Table(dbffile)
    table.open()

    files = {}
    main_file = ''

    for record in table:
        if dbf.is_deleted(record) or record.exclude is None or record.exclude:
            continue
        name, failed = find_full_path(record.name.rstrip('\x00'), directory)
        if failed:
            files[name] = None
        else:
            files[os.path.basename(name).lower()] = name
        if record.mainprog:
            main_file = os.path.basename(name).lower()

    table.close()
    os.remove(table.filename)
    os.remove(table.memoname)

    return files, main_file

def convert_project(infile, directory, encoding):
    project_files, main_file = read_vfp_project(infile)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if 'config.fpw' in project_files:
        with open(project_files['config.fpw'], encoding='utf-8') as fid:
            import configparser
            import io
            config_data = io.StringIO('[config]\r\n' + fid.read())
        config = configparser.RawConfigParser()
        config.readfp(config_data)
        config = {x[0]: x[1] for x in config.items('config')}
    else:
        config = {}
    with open(os.path.join(directory, '__main__.py'), 'w', encoding='utf-8') as fid:
        import pprint
        pp = pprint.PrettyPrinter(indent=4)
        print('from vfp2py.runtime import DO', file=fid)
        print(file=fid)
        print('config = {}'.format(pp.pformat(config)), file=fid)
        print(file=fid)
        print('DO({!r})'.format(main_file), file=fid)
    with open(os.path.join(directory, '__init__.py'), 'wb') as fid:
        pass
    global SEARCH_PATH
    search = SEARCH_PATH
    search += [project_files[name] for name in project_files]

    for name in project_files:
        try:
            print('processing {}'.format(name))
            SEARCH_PATH = search
            convert_file(project_files[name] or name, directory, encoding)
        except Exception as err:
            logging.getLogger().exception(err)
            print('failed to convert {}'.format(name))

class ParseKill(antlr4.error.ErrorListener.ErrorListener):
    def syntaxError(self, parser, token, line, char, msg, unknown):
        lines = token.getInputStream().strdata.splitlines()
        if len(lines) < line:
            linetxt = ''
        else:
            linetxt = lines[line - 1].strip()
        raise Exception('Syntax Error on line {}: {}\n{}'.format(line, linetxt, msg))

def run_parser(stream, parser, parser_start):
    parser._interp.PredictionMode = antlr4.PredictionMode.SLL
    parser.removeErrorListeners()
    parser._errHandler = antlr4.error.ErrorStrategy.BailErrorStrategy()
    try:
        return getattr(parser, parser_start)()
    except antlr4.error.Errors.ParseCancellationException as err:
        stream.reset();
        parser.reset();
        parser.addErrorListener(ParseKill())
        parser._errHandler = antlr4.error.ErrorStrategy.DefaultErrorStrategy()
        parser._interp.PredictionMode = antlr4.PredictionMode.LL
        return getattr(parser, parser_start)()

def prg2py_after_preproc(data, parser_start, input_filename):
    input_stream = antlr4.InputStream(data)
    lexer = VisualFoxpro9Lexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = VisualFoxpro9Parser(stream)
    tree = run_parser(stream, parser, parser_start)
    TreeCleanVisitor().visit(tree)
    output_tree = PythonConvertVisitor(input_filename).visit(tree)
    if not isinstance(output_tree, list):
        return output_tree
    return add_indents(output_tree, 0)
    #options = autopep8.parse_args(['--max-line-length', '100000', '-'])
    #output = autopep8.fix_code(output, options)
    tokens = list(tokenize.generate_tokens(io.StringIO(output).readline))
    for i, token in enumerate(tokens):
        token = list(token)
        if token[0] == tokenize.STRING and token[1].startswith('u'):
            token[1] = token[1][1:]
        tokens[i] = tuple(token)
    return tokenize.untokenize(tokens)

def prg2py(data, encoding, parser_start='prg', prepend_data='procedure _program_main\n', input_filename=''):
    tokens = preprocess_code(data, encoding).tokens
    data = prepend_data + ''.join(token.text.replace('\r', '') for token in tokens)
    return prg2py_after_preproc(data, parser_start, input_filename)

def convert_file(infile, outfile, encoding):
    file_ext = os.path.splitext(infile)[1].lower()
    if file_ext == '.pjx':
        return convert_project(infile, outfile, encoding)
    elif file_ext in ('.prg', '.mpr', '.spr'):
        return convert_prg(infile, outfile, encoding)
    elif file_ext == '.scx':
        return convert_scx(infile, outfile, encoding)
    elif file_ext == '.vcx':
        return convert_vcx(infile, outfile, encoding)
    elif file_ext in ('.frx', '.mnx', '.fll', '.app'):
        raise Exception('{} files not currently supported'.format(file_ext))
    elif file_ext in ('.fpw', '.h'):
        pass
    else:
        if os.path.isdir(outfile):
            outfile = os.path.join(outfile, os.path.basename(infile))
            shutil.copy(infile, outfile)
