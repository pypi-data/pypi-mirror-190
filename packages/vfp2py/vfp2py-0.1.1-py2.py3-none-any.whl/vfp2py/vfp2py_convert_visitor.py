# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import logging
import ntpath
import datetime as dt
import re
import tokenize
import keyword
from collections import OrderedDict

import isort

import antlr4

from .VisualFoxpro9Visitor import VisualFoxpro9Visitor

from . import vfpfunc
from .vfpfunc import DB

from .function_abbreviations import expander as function_expander

if sys.version_info < (3,):
    str=unicode
    CHR = chr
    def chr(x):
        return CHR(x).decode('ascii')

class CodeStr(str):
    def __repr__(self):
        return str(self)

    def __add__(self, val):
        return CodeStr('{} + {}'.format(self, repr(val)))

    def __radd__(self, val):
        return CodeStr('{} + {}'.format(repr(val), self))

    def __sub__(self, val):
        return CodeStr('{} - {}'.format(self, repr(val)))

    def __rsub__(self, val):
        return CodeStr('{} - {}'.format(repr(val), self))

    def __mul__(self, val):
        return CodeStr('{} * {}'.format(self, repr(val)))

    def __rmul__(self, val):
        return CodeStr('{} * {}'.format(repr(val), self))
PASS = CodeStr('pass')


class Expr:
    precedence = 0


class Number:
    def __init__(self, val):
        self.val = val

    def __int__(self):
        return int(self.val)

    def __repr__(self):
        return self.val


class BinaryExpr:
    op = '.'

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        left = repr(self.left)
        right = repr(self.right)
        if hasattr(self.left, 'precedence') and self.left.precedence > self.precedence:
            left = '(' + left + ')'
        if hasattr(self.right, 'precedence') and self.right.precedence > self.precedence:
            right = '(' + right + ')'
        return '{} {} {}'.format(left, self.op, right)


class AddExpr(BinaryExpr):
    op = '+'
    precedence = 1

class SubExpr(BinaryExpr):
    op = '-'
    precedence = 1

class MulExpr(BinaryExpr):
    op = '*'
    precedence = 2

class DivExpr(BinaryExpr):
    op = '*'
    precedence = 2


def leftify_with_associativity(value):
    while isinstance(value, BinaryExpr) and isinstance(value.left, BinaryExpr) and type(value) == type(value.left):
        value = type(value)(value.left.left, type(value)(value.left.right, value.right))
    return value


class RedirectedBuiltin(object):
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __call__(self, *args, **kwargs):
        try:
            return self.func(*args, **kwargs)
        except:
            return make_func_code(self.name, *args, **kwargs)

for func in (chr, int, str, float):
    globals()[func.__name__] = RedirectedBuiltin(func)

real_isinstance = isinstance
def isinstance(obj, istype):
    if not real_isinstance(istype, tuple):
        istype = (istype,)
    istype = tuple(x.func if real_isinstance(x, RedirectedBuiltin) else x for x in istype)
    return real_isinstance(obj, istype)

class OperatorExpr(object):
    precedence = -1
    operator = '?'

    def __init__(self, *args):
        self.args = args

    def wrap_arg(self, arg):
        if isinstance(arg, OperatorExpr) and arg.precedence < self.precedence:
            return '({})'.format(repr(arg))
        return arg

    def __repr__(self):
        args = [self.wrap_arg(arg) for arg in self.args]
        if len(args) == 1:
            return '{}{}'.format(self.operator, args[0])
        else:
            return '{}{}{}'.format(args[0], self.operator, args[1])

class OrExpr(OperatorExpr):
    precedence = 0
    operator = ' or '

class AndExpr(OperatorExpr):
    precedence = 1
    operator = ' and '

class NotExpr(OperatorExpr):
    precedence = 2
    operator = 'not '

def make_func_code(funcname, *args, **kwargs):
    args = [repr(x) for x in args]
    if not all(valid_identifier(name) for name in kwargs):
        args.append(add_args_to_code('**{}', [kwargs]))
    else:
        args += ['{}={}'.format(key, repr(kwargs[key])) for key in kwargs]
    return CodeStr('{}({})'.format(funcname, ', '.join(args)))

def string_type(val):
    return isinstance(val, str) and not isinstance(val, CodeStr)

def create_string(val):
    try:
        return str(val)
    except UnicodeEncodeError: #can this happen?
        return val

def add_args_to_code(codestr, args):
    return CodeStr(codestr.format(*[repr(arg) for arg in args]))

def valid_identifier(name):
    return re.match(tokenize.Name + '$', name) and not keyword.iskeyword(name)

class PythonConvertVisitor(VisualFoxpro9Visitor):
    def __init__(self, filename):
        super(PythonConvertVisitor, self).__init__()
        self.filename = filename
        self.filesystem_caseless = True
        self.imports = []
        self.scope = True
        self.withid = ''
        self.class_list = []
        self.function_list = []
        self.skip_extract = False
        self.must_assign = False

    def visit(self, ctx):
        if ctx:
            return super(type(self), self).visit(ctx)

    def visit_with_disabled_scope(self, ctx):
        self.scope = False
        retval = self.visit(ctx)
        self.scope = True
        return retval

    def list_visit(self, list_ctx):
        return [self.visit(x) for x in list_ctx]

    def getCtxText(self, ctx):
        start, stop = ctx.getSourceInterval()
        tokens = ctx.parser._input.tokens[start:stop+1]
        return ''.join(token.text for token in tokens)

    def visitPrg(self, ctx):
        if ctx.classDef():
            self.class_list = [self.visit(classDef.classDefStart())[0] for classDef in ctx.classDef()]
        if ctx.funcDef():
            self.function_list = [self.visit(funcdef.funcDefStart())[0] for funcdef in ctx.funcDef()]

        #self.imports = ['from __future__ import division, print_function']
        #self.imports.append('from vfp2py import vfpfunc')
        #self.imports.append('from vfp2py.vfpfunc import DB, Array, C, F, M, S')
        #self.imports.append('from vfp2py.vfpfunc import parameters, lparameters, vfpclass')
        defs = []

        for i, child in enumerate(ctx.children):
            if isinstance(child, ctx.parser.FuncDefContext):
                funcname, decorator, parameters, funcbody = self.visit(child)
                if i == 0 and funcname == '_program_main':
                    if len(funcbody) == 1 and funcbody[0] == 'pass':
                        continue
                    funcname = CodeStr('MAIN')
                defs += ([
                        add_args_to_code('@{}', (decorator,)),
                    ] if decorator else []) + [
                    add_args_to_code('def {}({}):', (funcname, CodeStr(','.join(parameters)))),
                    funcbody
                ]
                if child.lineComment():
                    defs += sum((self.visit(comment) for comment in child.lineComment()), [])
            elif not isinstance(child, antlr4.tree.Tree.TerminalNodeImpl):
                defs += self.visit(child)

        imports = isort.SortImports(file_contents='\n'.join(set(self.imports)), line_length=100000).output.splitlines()
        return  [CodeStr(imp) for imp in imports] + defs

    def visitLine(self, ctx):
        try:
            retval = self.visit(ctx.cmd() or ctx.controlStmt() or ctx.lineComment())
            if retval is None:
                if ctx.MACROLINE():
                    retval = make_func_code('MACRO_EVAL', create_string(ctx.MACROLINE().getText().strip()))
                else:
                    raise Exception('just to jump to except block')
        except Exception as err:
            logging.getLogger(__name__).exception(str(err))
            lines = self.getCtxText(ctx)
            print(lines)
            retval = [CodeStr('#FIX ME: {}'.format(line)) for line in lines.split('\n') if line]
        return retval if isinstance(retval, list) else [retval]

    def visitLineComment(self, ctx):
        fixer = re.compile('^\s*(&&|\*!\*|\**)(.*[^*; ]\s*|.*[^* ];\s*|;\s*)?(\**)\s*;*$')
        def repl(match):
            groups = match.groups()
            if not any(groups):
                return ''
            start = '*' if not groups[0] or groups[0] in ('&&', '*!*') else groups[0]
            middle = groups[1] or ''
            end = groups[2] or ''
            if len(start) == 1 and not end:
                middle = middle.strip()
            return ('#' * len(start) + middle + '#' * len(end)).strip()
        comments = [comment.strip() for comment in self.getCtxText(ctx).splitlines()]
        return [CodeStr(fixer.sub(repl, comment)) for comment in comments]

    def visitLines(self, ctx):
        retval = sum((self.visit(line) for line in ctx.line()), [])
        def badline(line):
            return line.startswith('#') or not line if hasattr(line, 'startswith') else not line
        if not retval or all(badline(l) for l in retval):
            retval.append(PASS)
        return retval

    def visitNongreedyLines(self, ctx):
        return self.visitLines(ctx)

    def modify_superclass(self, supername):
        return supername
        if hasattr(vfpfunc, supername):
            supername = add_args_to_code('{}.{}', (CodeStr('vfpfunc'), supername))
        elif supername in self.class_list:
            supername = add_args_to_code('{}Type()', (supername,))
        else:
            supername = add_args_to_code('C[{}]', (str(supername),))
        return supername

    def visitClassDef(self, ctx):
        assignments = []
        subclasses = {}

        funcdefs = [x.funcDef() for x in ctx.classProperty() if x.funcDef()]
        classassigns = [self.visitClassAssign(stmt.cmd()) for stmt in ctx.classProperty() if isinstance(stmt.cmd(), ctx.parser.AssignContext)]
        for stmt in ctx.classProperty():
            stmt = stmt.lineComment() or stmt.cmd()
            if isinstance(stmt, ctx.parser.LineCommentContext):
                assignments += self.visit(stmt)
            elif isinstance(stmt, ctx.parser.AssignContext):
                assignments += [CodeStr('self.' + ident + value) for (ident, value) in self.visitClassAssign(stmt) if '.' not in ident]
            elif isinstance(stmt, ctx.parser.AddObjectContext):
                name, obj = self.visit(stmt)
                for assignment in classassigns:
                    for (ident, value) in assignment:
                        if '.' in ident:
                            parent, ident = ident.split('.', 1)
                            if parent == name:
                                obj['args'][ident] = CodeStr(value.replace(' = ', '', 1))
                obj['functions'] = {}
                for funcdef in funcdefs:
                    funcname, decorator, funcbody = self.visit(funcdef)
                    if '.' in funcname:
                        func_parent, funcname = funcname.rsplit('.', 1)
                        if func_parent == name:
                            obj['functions'][funcname] = [decorator, funcbody]
                obj['args']['parent'] = CodeStr('self')
                obj['args']['name'] = name
                if obj['functions']:
                    subclass = 'SubClass' + name.title()
                    subclasses[subclass] = {key: obj[key] for key in ('parent_type', 'functions')}
                    obj['parent_type'] = 'self.' + str(subclass)
                    self.class_list.append(obj['parent_type'])
                assignments.append(add_args_to_code('self.{} = {}', [CodeStr(name), self.func_call('createobject', obj['parent_type'], **obj['args'])]))


        funcs = OrderedDict((
            ('_ASSIGN', [None, None, float('inf')]),
        ))
        for funcdef in funcdefs:
            funcname, decorator, funcbody = self.visit(funcdef)
            if '.' not in funcname:
                funcs[funcname] = [decorator, funcbody, funcdef.start.line]
            assignments += sum((self.visit(comment) for comment in funcdef.lineComment()), [])

        classname, supername = self.visit(ctx.classDefStart())

        funcbody = assignments
        self.modify_func_body(funcbody)
        funcs['_ASSIGN'][1] = funcbody
        funcs['_ASSIGN'][0] = ''#make_func_code('lparameters')

        retval = [
            #add_args_to_code('BaseClass = {}', (supername,)),
            CodeStr('class {}({}):'.format(classname, supername)),
        ]
        if funcs:
            for name in subclasses:
                subclass = subclasses[name]
                supername = self.modify_superclass(CodeStr(subclass['parent_type']))
                subclass_code = [CodeStr('class {}({}):'.format(name, supername))]
                for funcname in subclass['functions']:
                    decorator, funcbody = subclass['functions'][funcname]
                    subclass_code.append(([
                        add_args_to_code('@{}', (decorator,)),
                    ] if decorator else []) + [
                        add_args_to_code('def {}(self):', (CodeStr(funcname),)),
                        funcbody,
                    ])
                retval.append(subclass_code)
            for funcname in funcs:
                decorator, funcbody, line_number = funcs[funcname]
                retval.append(([
                    add_args_to_code('@{}', (decorator,)),
                ] if decorator else []) + [
                    add_args_to_code('def {}(self):', (CodeStr(funcname),)),
                    funcbody,
                ])
        else:
            retval.append([PASS])
        #retval.append(add_args_to_code('return {}', (classname,)))
        #retval = [
        #    CodeStr('@vfpclass'),
        #    add_args_to_code('def {}():', (classname,)),
        #    retval,
        #]

        return retval + sum((self.visit(comment) for comment in ctx.lineComment()), [])

    def visitClassDef(self, ctx):
        classname, supername = self.visit(ctx.classDefStart())
        retval = []
        for stmt in ctx.classProperty():
            stmt = stmt.lineComment() or stmt.cmd() or stmt.funcDef()
            if isinstance(stmt, ctx.parser.FuncDefContext):
                funcname, decorator, parameters, funcbody = self.visit(stmt)
                if '.' in funcname:
                    funcname = funcname.split('.')
                    funcname = CodeStr('_'.join(funcname).capitalize())
                retval += ([
                        add_args_to_code('@{}', (decorator,)),
                    ] if decorator else []) + [
                    add_args_to_code('def {}({}):', (funcname, CodeStr(','.join(parameters)))),
                    funcbody
                ]
            elif isinstance(stmt, ctx.parser.AddObjectContext):
                retval.append(self.visit(stmt))
                #name, obj = self.visit(stmt)
                #retval.append(add_args_to_code('{} = {}', (CodeStr(name), make_func_code(obj['parent_type'].title(), **obj['args']))))
            else:
                retval += self.visit(stmt)

        retval = [
            CodeStr('class {}({}):'.format(classname, supername)),
            retval
        ]
        return retval + sum((self.visit(comment) for comment in ctx.lineComment()), [])

    def visitClassDefStart(self, ctx):
        names = [self.visit(ctx.identifier())] + [self.visit(ctx.asTypeOf())[0]]
        names = [CodeStr(name.title()) for name in names]
        if len(names) < 2:
            names.append('Custom')
        classname, supername = names
        if hasattr(vfpfunc, classname):
            raise Exception(str(classname) + ' is a reserved classname')
        supername = self.modify_superclass(supername)
        return classname, supername

    def visitClassAssign(self, assign):
        #FIXME - come up with a less hacky way to make this work
        args1 = self.visit_with_disabled_scope(assign)
        args2 = self.visit(assign)
        args = []
        for arg1, arg2 in zip(args1, args2):
            ident = arg1[:arg1.find(' = ')]
            value = arg2[arg2.find(' = '):]
            args.append((ident, value))
        return args

    def visitAddObject(self, ctx):
        name = str(self.visit(ctx.identifier()))
        objtype = str(self.visit(ctx.asType()))
        kwargs = {self.visit(key): self.visit(expr) for key, expr in zip(ctx.idAttr(), ctx.expr())}
        return make_func_code('ADD_OBJECT', name, objtype, **kwargs)

        name = str(self.visit_with_disabled_scope(ctx.identifier()))
        keywords = [self.visit_with_disabled_scope(idAttr) for idAttr in ctx.idAttr()]
        kwargs = {key: self.visit(expr) for key, expr in zip(keywords, ctx.expr())}
        objtype = create_string(self.visit_with_disabled_scope(ctx.asType())).title()
        return name, {'parent_type': objtype, 'args': kwargs}

    def visitFuncDefStart(self, ctx):
        params = self.visit_with_disabled_scope(ctx.parameters()) or []
        params = [name if not name.startswith('m.') else name[2:] for name in params]
        return self.visit(ctx.idAttr2()), params

    def visitParameter(self, ctx):
        return self.visit(ctx.idAttr())

    def visitParameters(self, ctx):
        return self.list_visit(ctx.parameter())

    def modify_func_body(self, body):
#        while len(body) > 0 and (not body[-1] or (isinstance(body[-1], CodeStr) and (body[-1] == 'return'))):
#            body.pop()
        while PASS in body:
            body.pop(body.index(PASS))
        if all(isinstance(x, CodeStr) and (not x.strip() or x.strip().startswith('#')) for x in body):
            body.append(PASS)

    def visitFuncDef(self, ctx):
        name, parameters = self.visit(ctx.funcDefStart())
        if parameters:
            parameter_type = 'l'
        else:
            try:
                parameter_line = next(line for line in ctx.lines().line() if not line.lineComment())
                parameter_cmd = parameter_line.cmd()
                parameter_type = parameter_cmd.PARAMETER().symbol.text.lower()[0]
                parameters = [self.visit_with_disabled_scope(p)[0] for p in parameter_cmd.declarationItem()]
                parameters = [name if not name.startswith('m.') else name[2:] for name in parameters]
                lines = ctx.lines()
                children = [c for c in lines.children if c is not parameter_line]
                while lines.children:
                    lines.removeLastChild()
                for child in children:
                    lines.addChild(child)
            except (StopIteration, AttributeError):
                parameters = []
                parameter_type = 'l'
        if parameter_type != 'l':
            parameter_type = ''
        parameter_type += 'parameters'
        parameters = [str(p) for p in parameters]
        if parameter_type == 'parameters':
            decorator = CodeStr(parameter_type.upper())
        else:
            decorator = None
        global FUNCNAME
        FUNCNAME = name
#        body = self.modify_func_body(self.visit(ctx.lines()))
        body = self.visit(ctx.lines())
        return name, decorator, parameters, body

    def visitPrintStmt(self, ctx):
        kwargs = {}
        if len([child for child in ctx.children if child.getText() == '?']) > 1:
            func = 'PRINT_NO_LINE_END'
        else:
            func = 'PRINT'
        if ctx.DEBUGOUT():
            kwargs['DEBUGOUT'] = True
        return [make_func_code('PRINT', *(self.visit(ctx.args()) or []), **kwargs)]

    def visitAtPos(self, ctx):
        if ctx.SAY() and len(ctx.SAY()) > 1:
            raise Exception('Invalid command')
        if ctx.sayExpr:
            func = make_func_code('PRINT', self.visit(ctx.sayExpr))
        else:
            func = make_func_code('PRINT')
        return add_args_to_code('{} # {}', [func, CodeStr(self.getCtxText(ctx))])

    def visitIfStart(self, ctx):
        return self.visit(ctx.expr())

    def visitIfStmt(self, ctx):
        evaluation = self.visit(ctx.ifStart())

        ifBlock = self.visit(ctx.ifBody)
        retval = [CodeStr('if {}:'.format(evaluation)), ifBlock]

        if ctx.elseBody:
            elseBlock = self.visit(ctx.elseBody)
            retval += [CodeStr('else:'), elseBlock]

        return retval

    def visitCaseStmt(self, ctx):
        retval = self.list_visit(ctx.lineComment())

        items = self.list_visit(ctx.singleCase())

        if not items:
            retval += [CodeStr('if True:'), [PASS]]
        else:
            expr, lines = items[0]
            retval += [CodeStr('if {}:'.format(expr)), lines]
            for expr, lines in items[1:]:
                retval += [CodeStr('elif {}:'.format(expr)), lines]

        if ctx.otherwise():
            retval += [CodeStr('else:'), self.visit(ctx.otherwise())]
        return retval

    def visitSingleCase(self, ctx):
        return self.visit(ctx.expr()), self.visit(ctx.nongreedyLines())

    def visitOtherwise(self, ctx):
        return self.visit(ctx.lines())

    def visitForStart(self, ctx):
        loopvar = self.visit(ctx.idAttr())
        if ctx.EACH():
            iterator = self.visit(ctx.expr(0))
        else:
            args = [self.visit(ctx.loopStart), self.visit(ctx.loopStop)]
            if ctx.loopStep:
                args.append(self.visit(ctx.loopStep))
            iterator = make_func_code('RANGE', *args)
        return add_args_to_code('for {} in {}:', (loopvar, iterator))

    def visitForStmt(self, ctx):
        return [self.visit(ctx.forStart()), self.visit(ctx.lines())]

    def visitWhileStart(self, ctx):
        return CodeStr('while {}:'.format(self.visit(ctx.expr())))

    def visitWhileStmt(self, ctx):
        return [self.visit(ctx.whileStart()), self.visit(ctx.lines())]

    def visitWithStmt(self, ctx):
        self.withid = self.visit(ctx.idAttr())
        lines = self.visit(ctx.lines())
        self.withid = ''
        return lines

    def visitScanStmt(self, ctx):
        lines = self.visit(ctx.lines())
        scope = self.visit(ctx.scopeClause())
        kwargs = {}
        if scope:
            kwargs.update(scope)
        if ctx.FOR():
            kwargs['FOR'] = add_args_to_code('lambda: {}', [self.visit(ctx.expr())])
        func = make_func_code('SCAN', **kwargs)
        return [add_args_to_code('while {}:', [func]), lines]

    def visitTryStmt(self, ctx):
        try_lines = self.visit(ctx.tryLines)
        finally_lines = self.visit(ctx.finallyLines) or []
        if not ctx.CATCH():
            return try_lines + finally_lines

        try_lines = [CodeStr('try:'), try_lines]

        kwargs = {}
        if ctx.idAttr():
            kwargs['TO'] = self.visit(ctx.idAttr()[0])
        if ctx.expr():
            kwargs['WHEN'] = self.visit(ctx.expr()[0])

        exception = make_func_code('CATCH', **kwargs)
        catch_lines = [add_args_to_code('except {}:', [exception])]
        catch_lines.append(self.visit(ctx.catchLines))
        if len(catch_lines) > 2 and len(catch_lines[-1]) == 1 and catch_lines[-1][0] == 'pass':
            catch_lines[-1].pop()

        finally_lines = [CodeStr('finally:'), finally_lines] if finally_lines else []

        return try_lines + catch_lines + finally_lines

    def visitProgramControl(self, ctx):
        action = ctx.PROGRAMCONTROL().symbol.text.lower()[:4]
        action = {
            'loop': 'continue',
            'exit': 'break',
            'quit': 'QUIT()',
            'canc': 'CANCEL()',
            'susp': 'SUSPEND()',
            'resu': 'RESUME()',
            'node': 'NODEFAULT()',
        }.get(action, None)
        return CodeStr(action) if action else None

    def visitDeclaration(self, ctx):
        if ctx.PARAMETER():
            return
        if ctx.SCOPE() or ctx.EXTERNAL():
            scope = {
                'prot': 'PROTECTED',
                'hidd': 'HIDDEN',
                'publ': 'PUBLIC',
                'priv': 'PRIVATE',
                'loca': 'LOCAL',
                'exte': 'EXTERNAL',
            }.get((ctx.SCOPE() or ctx.EXTERNAL()).getText().lower()[:4])
        namesinds = [self.visit(x) for x in ctx.declarationItem()]
        if ctx.ARRAY() or ctx.DIMENSION() or ctx.DECLARE():
            if ctx.DIMENSION():
                scope = 'dimension'
            elif ctx.DECLARE():
                scope = 'declare'
            namesvals = [(name if not name.startswith('m.') else name[2:], make_func_code('ARRAY', *(ind or []))) for name, ind in namesinds]
        else:
            namesvals = [(name if not name.startswith('m.') else name[2:], False) for name, ind in namesinds]

        if scope:
            func = scope.upper()
            if scope in ('PRIVATE', 'PROTECTED', 'HIDDEN', 'EXTERNAL'):
                kwargs = {str(name): val for name, val in namesvals if val != False}
                args = tuple(name for name, val in namesvals if val == False)
            else:
                kwargs = {str(name): val for name, val in namesvals}
                args = ()

            return make_func_code(func, *args, **kwargs)

    def visitDeclarationItem(self, ctx):
        return self.visit(ctx.idAttr() or ctx.idAttr2()), self.visit(ctx.arrayIndex())

    def visitAsTypeOf(self, ctx):
        return self.visit(ctx.asType()), self.visit(ctx.specialExpr())

    def visitAsType(self, ctx):
        return self.visit_with_disabled_scope(ctx.datatype().idAttr())

    def visitAssign(self, ctx):
        value = self.visit(ctx.expr())
        args = []
        for var in ctx.idAttr():
            trailer = self.visit(var.trailer()) or []
            if len(trailer) > 0 and isinstance(trailer[-1], list):
                identifier = self.visit(var.identifier())
                arg = self.createIdAttr(identifier, trailer[:-1])
                args.append('{}[{}]'.format(arg, ','.join(repr(x) for x in trailer[-1])))
            else:
                args.append(self.visit(var))
        if len(args) == 1 and isinstance(value, AddExpr):
            value = leftify_with_associativity(value)
            if value.left == args[0]:
                op = value.op
                value = value.right
                return [CodeStr('{} {}= {}'.format(args[0], op, repr(value)))]
        return [CodeStr(' = '.join(args + [repr(value)]))]

    def visitArgs(self, ctx):
        exprs = [ctx.expr()] + [arg.expr() for arg in ctx.argsItem()]
        return [self.visit(expr) if expr else False for expr in exprs]

    def visitSpecialArgs(self, ctx):
        return self.list_visit(ctx.specialExpr())

    def visitComparison(self, ctx):
        symbol_dict = {
            ctx.parser.GREATERTHAN: '>',
            ctx.parser.GTEQ: '>=',
            ctx.parser.LESSTHAN: '<',
            ctx.parser.LTEQ: '<=',
            ctx.parser.NOTEQUALS: '!=',
            ctx.parser.NOTEQUALS2: '!=',
            ctx.parser.HASH: '!=',
            ctx.parser.EQUALS: '==',
            ctx.parser.DOUBLEEQUALS: 'is',
            ctx.parser.DOLLAR: 'in',
            ctx.parser.OR: 'or',
            ctx.parser.OTHEROR: 'or',
            ctx.parser.AND: 'and',
            ctx.parser.OTHERAND: 'and',
        }
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        symbol = symbol_dict[ctx.op.type]
        if symbol == 'is' and (isinstance(left, Number) or isinstance(right, Number)):
            symbol = '=='
        return CodeStr('{} {} {}'.format(repr(left), symbol, repr(right)))

    def visitBooleanOr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return OrExpr(left, right)

    def visitBooleanAnd(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return AndExpr(left, right)

    def visitUnaryNegation(self, ctx):
        return add_args_to_code('{}' if ctx.op.type == ctx.parser.PLUS_SIGN else '-{}', (self.visit(ctx.expr()),))

    def visitBooleanNegation(self, ctx):
        return NotExpr(self.visit(ctx.expr()))

    def func_call(self, funcname, *args, **kwargs):
        funcname = str(funcname)
        funcname = function_expander.get(funcname, funcname)
        if not kwargs and len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        args = list(args)
        #funcname = {
        #    'at_c': 'at',
        #    'atcc': 'atc',
        #    'atcline': 'atline',
        #    'chrtranc': 'chrtran',
        #    'leftc': 'left',
        #    'lenc': 'len',
        #    'likec': 'like',
        #    'ratc': 'rat',
        #    'rightc': 'right',
        #    'select': 'select_function',
        #    'stuffc': 'stuff',
        #    'substrc': 'substr',
        #    'sys': 'vfp_sys',
        #}.get(funcname, funcname)
        #if funcname == 'dodefault':
        #    return make_func_code('super(type(self), self).{}'.format(FUNCNAME), *args)
        #if funcname in self.function_list:
        #    return make_func_code(funcname, *args)
        if funcname == 'chr' and len(args) == 1 and isinstance(args[0], Number):
            return chr(int(args[0]))
        #if funcname == 'val' and len(args) == 1:
        #    return float(args[0])
        #if funcname == 'space' and len(args) == 1:
        #    args[0] = int(args[0])
        #    if isinstance(args[0], int) and args[0] > 8:
        #        args[0] = CodeStr(args[0])
        #    return args[0] * ' '
        #if funcname == 'asc':
        #    return make_func_code('ord', CodeStr(str(repr(args[0])) + '[0]'))
        #if funcname == 'len':
        #    return make_func_code('len', *args)
        #if funcname == 'alen':
        #    if len(args) == 1:
        #        return make_func_code('len', *args)
        #    else:
        #        args[1] = int(args[1])
        #        return add_args_to_code('{}.alen({})', args)
        #if funcname == 'ascan':
        #    if len(args) == 3:
        #        args = [add_args_to_code('{}[{}:]', [args[0], args[2]]), args[1]]
        #    elif len(args) == 4:
        #        args = [add_args_to_code('{}[{}:({} + {})]', [args[0], args[2], args[2], args[3]]), args[1]]
        #    if len(args) == 2:
        #        return add_args_to_code('{}.index({})', args)
        #if funcname == 'ains':
        #    return make_func_code(add_args_to_code('{}.insert', args[:1]), *([None] + args[1:]))
        #if funcname == 'afields':
        #    localscode = make_func_code('locals')
        #    arrname = args.pop(0)
        #    if not args:
        #        args.append(None)
        #    replace_string = 'S.'
        #    if arrname.startswith(replace_string):
        #        arrname = str(arrname[len(replace_string):]) #FIXME
        #    else:
        #        arrname = str(arrname)
        #    args.append(arrname)
        #    args.append((localscode, CodeStr('S')))
        #if funcname == 'acopy':
        #    func = add_args_to_code('{}.copy', (args[0],))
        #    arrname = args[1]
        #    replace_string = 'S.'
        #    if arrname.startswith(replace_string):
        #        arrname = str(arrname[len(replace_string):]) #FIXME
        #    else:
        #        arrname = str(arrname)
        #    return make_func_code(func, arrname, *args[2:])
        #if funcname == 'empty':
        #    return add_args_to_code('(not {} if {} is not None else False)', args + args)
        #if funcname == 'occurs':
        #    return add_args_to_code('{}.count({})', reversed(args))
        #if funcname in ('atc',):
        #    funcname = funcname[:-1]
        #    args[0] = add_args_to_code('{}.lower()', [args[0]])
        #    args[1] = add_args_to_code('{}.lower()', [args[1]])
        #if funcname in ('at', 'rat'):
        #    funcname = {
        #        'at': 'find',
        #        'rat': 'rfind',
        #    }[funcname]
        #    return add_args_to_code('{}.{}({})', [args[1], CodeStr(funcname), args[0]]) + 1
        #if funcname == 'replicate' and len(args) == 2:
        #    args[1] = int(args[1])
        #    return add_args_to_code('{}', args[:1]) * add_args_to_code('{}', args[1:])
        #if funcname in ('date', 'datetime', 'time', 'dtot'):
        #    self.imports.append('import datetime as dt')
        #    if len(args) == 0:
        #        if funcname == 'date':
        #            return make_func_code('dt.date.today')
        #        elif funcname == 'datetime':
        #            return make_func_code('dt.datetime.now')
        #        elif funcname == 'time':
        #            return make_func_code('dt.datetime.now().time().strftime', '%H:%M:%S')
        #    else:
        #        if funcname == 'date':
        #            return make_func_code('dt.date', *args)
        #        elif funcname == 'datetime':
        #            return make_func_code('dt.datetime', *args)
        #        elif funcname == 'time':
        #            return add_args_to_code('{}[:11]', [make_func_code('dt.datetime.now().time().strftime', '%H:%M:%S.%f')])
        #    if funcname == 'dtot':
        #        return make_func_code('dt.datetime.combine', args[0], make_func_code('dt.datetime.min.time'))
        #if funcname in ('year', 'month', 'day', 'hour', 'minute', 'sec', 'dow', 'cdow', 'cmonth', 'dmy'):
        #    self.imports.append('import datetime as dt')
        #    funcname = {
        #        'sec': 'second',
        #        'dow': 'weekday()',
        #        'cdow': "strftime('%A')",
        #        'cmonth': "strftime('%B')",
        #        'dmy': "strftime('%d %B %Y')",
        #    }.get(funcname, funcname)
        #    retval = add_args_to_code('{}.{}', [args[0], CodeStr(funcname)])
        #    if funcname == 'weekday()':
        #        return make_func_code('vfpfunc.dow_fix', retval, *args[1:])
        #    return retval
        #if funcname in ('dtoc', 'dtos'):
        #    if len(args) == 1 or args[1] == 1:
        #        if len(args) < 2:
        #            args.append('')
        #        if args[1] == 1 or funcname == 'dtos':
        #            if args[0] == 'dt.datetime.now()':
        #                args[1] = '%Y%m%d%H%M%S'
        #            elif args[0] == 'dt.datetime.now().date()':
        #                args[0] = CodeStr('dt.datetime.now()')
        #                args[1] = '%Y%m%d'
        #            else:
        #                return make_func_code('vfpfunc.dtos', args[0])
        #        else:
        #            return make_func_code('vfpfunc.dtoc', args[0])
        #        return make_func_code('{}.{}'.format(args[0], 'strftime'), args[1])
        if funcname == 'iif' and len(args) == 3:
            return add_args_to_code('({} if {} else {})', [args[i] for i in (1, 0, 2)])
        #if funcname == 'between':
        #    return add_args_to_code('({} <= {} <= {})', [args[i] for i in (1, 0, 2)])
        #if funcname == 'nvl':
        #    return add_args_to_code('({} if {} is not None else {})', [args[0], args[0], args[1]])
        #if funcname == 'evl':
        #    return add_args_to_code('({} or {})', args)
        #if funcname == 'sign':
        #    return add_args_to_code('1 if {} > 0 else (-1 if {} < 0 else 0)', [args[0], args[0]])
        #if funcname in ('alltrim', 'ltrim', 'rtrim', 'lower', 'upper', 'padr', 'padl', 'padc', 'proper'):
        #    funcname = {
        #        'alltrim': 'strip',
        #        'ltrim': 'lstrip',
        #        'rtrim': 'rstrip',
        #        'padr': 'ljust',
        #        'padl': 'rjust',
        #        'padc': 'center',
        #        'proper': 'title',
        #    }.get(funcname, funcname)
        #    funcname = '{}.{}'.format(repr(args[0]), funcname)
        #    return make_func_code(funcname, *args[1:])
        #if funcname == 'strtran':
        #    args = args[:6]
        #    if len(args) > 3:
        #        args[3:] = [int(arg) for arg in args[3:]]
        #    if len(args) == 6 and int(args[5]) in (0, 2):
        #        args.pop()
        #    if len(args) == 2:
        #        args.append('')
        #    str_replace = add_args_to_code('{}.replace', [args[0]])
        #    if len(args) == 3:
        #        return make_func_code(str_replace, *args[1:])
        #    elif len(args) == 4 and args[3] < 2:
        #        args.pop()
        #        return make_func_code(str_replace, *args[1:])
        #    elif len(args) == 5 and args[3] < 2:
        #        args[3] = args[4]
        #        args.pop()
        #        return make_func_code(str_replace, *args[1:])
        #if funcname == 'strconv' and len(args) == 2:
        #    self.imports.append('import base64')
        #    if args[1] == 13:
        #        return make_func_code('base64.b64encode', args[0])
        #    if args[1] == 14:
        #        return make_func_code('base64.b64decode', args[0])
        #if funcname == 'right':
        #    args[1] = int(args[1])
        #    return add_args_to_code('{}[-{}:]', args)
        #if funcname == 'left' and len(args) == 2:
        #    args[1] = int(args[1])
        #    return add_args_to_code('{}[:{}]', args)
        #if funcname == 'substr':
        #    args[1:] = [int(arg) for arg in args[1:]]
        #    args[1] -= 1
        #    if len(args) < 3:
        #        return add_args_to_code('{}[{}:]', args)
        #    if args[2] == 1:
        #        return add_args_to_code('{}[{}]', args[:2])
        #    if args[1] == 0:
        #       return add_args_to_code('{}[:{}]', (args[0], args[2]))
        #    args[2] += args[1]
        #    return add_args_to_code('{}[{}:{}]', args)
        #if funcname == 'getenv':
        #    args.append('')
        #    args[0] = args[0].upper() if string_type(args[0]) else add_args_to_code('{}.upper()', args[0])
        #    return make_func_code('os.environ.get', *args)
        #if funcname == 'getwordcount':
        #    if len(args) < 2:
        #        args.append(CodeStr(''))
        #    return add_args_to_code('len([w for w in {}.split({}) if w])', args)
        #if funcname == 'rand':
        #    self.imports.append('import random')
        #    return make_func_code('random.random')
        #if funcname in ('ceiling', 'exp', 'log', 'log10', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2', 'pi', 'sqrt', 'dtor', 'rtod'):
        #    self.imports.append('import math')
        #    if funcname == 'pi':
        #        return CodeStr('math.pi')
        #    funcname = {
        #        'ceiling': 'ceil',
        #        'atn2': 'atan2',
        #        'rtod': 'degrees',
        #        'dtor': 'radians',
        #    }.get(funcname, funcname)
        #    funcname = 'math.' + funcname
        #    return make_func_code(funcname, *args)
        #if funcname in ('bitand', 'bitclear', 'bitlshift', 'bitnot', 'bitor', 'bitrshift', 'bitset', 'bittest', 'bitxor'):
        #    op = {
        #        'bitand': '({} & {})',
        #        'bitclear': '({} & ((1 << {}) ^ 0xffffffff))',
        #        'bitlshift': '({} << {})',
        #        'bitnot': '~{}',
        #        'bitor': '({} | {})',
        #        'bitrshift': '({} >> {})',
        #        'bitset': '({} | (1 << {}))',
        #        'bittest': '(({} & (1 << {})) > 0)',
        #        'bitxor': '({} ^ {})'
        #    }
        #    return add_args_to_code(op[funcname], [int(arg) for arg in args])
        #if funcname in ('abs', 'round', 'max', 'min'):
        #    return make_func_code(funcname, *args)
        #if funcname == 'mod':
        #    return add_args_to_code('({} % {})', args)
        #if funcname == 'int':
        #    return int(args[0])
        #if funcname == 'isnull':
        #    return add_args_to_code('{} == {}', [args[0], None])
        #if funcname in ('isalpha', 'islower', 'isdigit', 'isupper'):
        #    return add_args_to_code('{}[:1].{}()', [args[0], CodeStr(funcname)])
        #if funcname == 'inlist':
        #    return add_args_to_code('({} in {})', [args[0], tuple(args[1:])])
        #if funcname == 'parameters':
        #    return CodeStr('vfpfunc.PARAMETERS')
        #if funcname == 'pythonfunctioncall' and len(args) >= 2:
        #    self.imports.append('import {}'.format(args[0]))
        #    if len(args) == 2:
        #        return make_func_code('{}.{}'.format(args[0], args[1]))
        #    elif isinstance(args[2], tuple):
        #        return make_func_code('{}.{}'.format(args[0], args[1]), *args[2])
        #    else:
        #        return make_func_code('{}.{}'.format(args[0], args[1]), add_args_to_code('*{}', (args[2],)))
        #if funcname == 'createobject':
        #    if len(args) > 0 and string_type(args[0]) and args[0].lower() == 'pythontuple':
        #        return tuple(args[1:])
        #    elif len(args) > 0 and string_type(args[0]) and args[0].lower() == 'pythonlist':
        #        if len(args) > 1 and isinstance(args[1], list):
        #            return add_args_to_code('{}.data[:]', args[1])
        #        return []
        #    elif len(args) > 0 and string_type(args[0]) and args[0].lower() == 'pythondictionary':
        #        return {}
        #    elif len(args) == 2 and string_type(args[0]) and args[0].lower() == 'pythonmodule' and string_type(args[1]):
        #        self.imports.append('import {}'.format(args[1]))
        #        return CodeStr(args[1])
        #    elif len(args) > 0 and string_type(args[0]):
        #    if len(args) > 0 and string_type(args[0]) and valid_identifier(args[0].title()):
        #        objtype = args[0]
        #        if not objtype.startswith('self.'):
        #            objtype = objtype.title()
        #        args = args[1:]
        #        if objtype in self.class_list:
        #        if True:
        #            return make_func_code(objtype, *args, **kwargs)
        #        elif hasattr(vfpfunc, objtype):
        #            objtype = 'vfpfunc.{}'.format(objtype)
        #            return make_func_code(objtype, *args, **kwargs)
        #        else:
        #            return make_func_code('CREATE_OBJECT', *([objtype] + args), **kwargs)
        #    else:
        #        return make_func_code('vfpfunc.create_object', *args, **kwargs)
        #if funcname in ('fcreate', 'fopen'):
        #    opentypes = ('w', 'r') if funcname == 'fcreate' else ('r', 'w', 'r+')
        #    if len(args) > 1 and args[1] <= len(opentypes):
        #        args[1] = int(args[1])
        #        if isinstance(args[1], int):
        #            args[1] = opentypes[args[1]]
        #        else:
        #            args[1] = add_args_to_code({}[{}]).format(opentypes, args[1])
        #    else:
        #        args.append(opentypes[0])
        #    return make_func_code('open', *args)
        #if funcname == 'fclose':
        #    return add_args_to_code('{}.close()', args)
        #if funcname in ('fputs', 'fwrite'):
        #    if len(args) == 3:
        #        args[2] = int(args[2])
        #        args[1] = add_args_to_code('{}[:{}]', args[1:])
        #    if funcname == 'fputs':
        #        args[1] += '\r\n'
        #    return add_args_to_code('{}.write({})', args)
        #if funcname in ('fgets', 'fread'):
        #    if funcname == 'fgets':
        #        code = '{}.readline({}).strip(\'\\r\\n\')'
        #    else:
        #        code = '{}.read({})'
        #    if len(args) < 2:
        #        args.append(CodeStr(''))
        #    else:
        #        args[1] = int(args[1])
        #    return add_args_to_code(code, args)
        #if funcname == 'fseek':
        #    funcname = '{}.seek'.format(args[0])
        #    return make_func_code(funcname, *args[1:])
        #if funcname in ('file', 'directory', 'justdrive', 'justpath', 'justfname', 'juststem', 'justext', 'forceext', 'addbs', 'curdir'):
        #    if self.filesystem_caseless:
        #        args = [arg.lower() if string_type(arg) else arg for arg in args]
        #    self.imports.append('import os')
        #    operation = {
        #        'file': [make_func_code, ['os.path.isfile'] + args],
        #        'directory': [make_func_code, ['os.path.isdir'] + args],
        #        'justdrive': [add_args_to_code, ('os.path.splitdrive({})[0]', args)],
        #        'justpath': [make_func_code, ['os.path.dirname'] + args],
        #        'justfname': [make_func_code, ['os.path.basename'] + args],
        #        'juststem': [add_args_to_code, ('os.path.splitext(os.path.basename({}))[0]', args)],
        #        'justext': [add_args_to_code, ('os.path.splitext({})[1][1:]', args)],
        #        'forceext': [add_args_to_code, ('os.path.splitext({})[0] + \'.\' + {}', args)],
        #        'addbs': [make_func_code, ['os.path.join'] + args + ['']],
        #        'curdir': [make_func_code, ['os.getcwd']],
        #    }[funcname]
        #    return operation[0](*operation[1])
        #if funcname == 'set' and len(args) > 0 and string_type(args[0]):
        #    args[0] = args[0].lower()
        #if funcname == 'select_function' and not args:
        #    args = (add_args_to_code('{} if {} else {}', (0, CodeStr('vfpfunc.set(\'compatible\') == \'OFF\''), None)),)
        #if funcname in dir(vfpfunc):
        #    funcname = 'vfpfunc.' + funcname
        #elif funcname in dir(DB):
        #    funcname = 'DB.' + funcname
        #else:
        #    funcname = self.scopeId(funcname, 'func')
        if self.must_assign:
            return CodeStr('{}[{}]'.format(funcname, ', '.join(repr(x) for x in args)))
        return make_func_code(funcname, *args)

    def scopeId(self, identifier, vartype):
        scope = CodeStr({
            'val': 'S',
            'func': 'F',
        }[vartype])
        if scope != 'F':
            if not self.scope:
                return identifier
            elif identifier == 'this':
                return CodeStr('self')
            elif identifier == 'thisform':
                return CodeStr('self.parentform')
        if valid_identifier(identifier):
            if identifier == 'm':
                return CodeStr('M')
            else:
                return add_args_to_code('{}.{}', [scope, CodeStr(identifier)])
        else:
            return add_args_to_code('{}[{}]', [scope, identifier])

    def createIdAttr(self, identifier, trailer):
        if trailer and len(trailer) == 1 and isinstance(trailer[0], list):
            args = trailer[0]
            return self.func_call(identifier, args)
        #elif trailer and len(trailer) > 1 and trailer[-2] == 'setitem' and isinstance(trailer[-1], list) and len(trailer[-1]) == 2:
        #    return add_args_to_code('{}[{}] = {}', [self.createIdAttr(identifier, trailer[:-2])] + trailer[-1])
        #elif trailer and len(trailer) > 1 and trailer[-2] == 'getitem' and isinstance(trailer[-1], list) and len(trailer[-1]) == 1:
        #    return add_args_to_code('{}[{}]', [self.createIdAttr(identifier, trailer[:-2])] +  trailer[-1])
        #elif trailer and len(trailer) > 1 and trailer[-2] == 'callmethod' and isinstance(trailer[-1], list) and len(trailer[-1]) == 2:
        #    trailer[-1][0] = CodeStr(trailer[-1][0])
        #    func = add_args_to_code('{}.{}', [self.createIdAttr(identifier, trailer[:-2])] + trailer[-1][:1])
        #    return make_func_code(func, *trailer[-1][1])
        else:
            trailer = [self.convert_trailer_args(t) for t in trailer or ()]
            trailer = CodeStr(''.join(trailer))
        #if identifier.islower():
        #    identifier = self.scopeId(identifier, 'val')
        if not valid_identifier(identifier):
            identifier = add_args_to_code('ID{}', [identifier])
        return add_args_to_code('{}{}', (identifier, trailer))

    def convert_trailer_args(self, trailer):
        if isinstance(trailer, list):
            return make_func_code('', *trailer)
        else:
            return add_args_to_code('.{}', (trailer,))

    def visitFuncCallTrailer(self, ctx):
        trailer = self.visit(ctx.trailer()) or []
        retval = [[x for x in self.visit(ctx.args()) or []]]
        return retval + trailer or None

    def visitIdentTrailer(self, ctx):
        trailer = self.visit(ctx.trailer()) or []
        retval = [self.visit_with_disabled_scope(ctx.identifier())]
        return retval + trailer or None

    def visitIdAttr(self, ctx):
        identifier = self.visit(ctx.identifier())
        trailer = self.visit(ctx.trailer())
        if ctx.PERIOD() and self.withid:
            trailer = [identifier] + (trailer or [])
            identifier = self.withid
        return self.createIdAttr(identifier, trailer)

    def visitIdAttr2(self, ctx):
        return CodeStr('.'.join(([self.withid] if ctx.startPeriod else []) + self.list_visit(ctx.identifier())))

    datatypes_map = {
        'w': 'blob',
        'blob': 'blob',
        'c': 'character',
        'char': 'character',
        'character': 'character',
        'y': 'currency',
        'currency': 'currency',
        'd': 'date',
        'date': 'date',
        't': 'datetime',
        'datetime': 'datetime',
        'b': 'double',
        'double': 'double',
        'f': 'float',
        'float': 'float',
        'g': 'general',
        'general': 'general',
        'i': 'integer',
        'int': 'integer',
        'integer': 'integer',
        'l': 'logical',
        'logical': 'logical',
        'm': 'memo',
        'memo': 'memo',
        'n': 'numeric',
        'num': 'numeric',
        'numeric': 'numeric',
        'q': 'varbinary',
        'varbinary': 'varbinary',
        'v': 'varchar',
        'varchar': 'varchar',
    }

    def visitCastExpr(self, ctx):
        datatype = self.visit(ctx.asType())
        import re
        x = re.match(r'([A-Za-z]+)(\(([0-9]+)(, ([0-9]+))?\))?', datatype)
        args = []
        if x:
            x = x.groups()
            datatype = x[0]
            args = [int(y) for y in (x[2], x[4]) if y]
        func = {
            'character': 'C',
            'varchar': 'V',
            'memo': 'M',
            'general': 'G',
            'numeric': 'N',
            'currency': 'Y',
            'float': 'F',
            'double': 'B',
            'integer': 'I',
            'logical': 'L',
            'blob': 'W',
            'varbinary': 'Q',
            'date': 'D',
            'datetime': 'T',
        }[self.datatypes_map[datatype]]
        expr = self.visit(ctx.expr())
        args.append(None if not ctx.NULL() else bool(ctx.NOT()))
        return make_func_code('cast', expr, func, *args)

    def visitDatatype(self, ctx):
        dtype = self.visit_with_disabled_scope(ctx.idAttr())
        try:
            return self.datatypes_map[dtype]
        except KeyError:
            raise ValueError("invalid datatype '{}'".format(dtype))

    def visitAtomExpr(self, ctx):
        atom = self.visit(ctx.atom())
        trailer = self.visit(ctx.trailer())
        if ctx.PERIOD() and self.withid:
            trailer = [atom] + (trailer or [])
            atom = self.withid

        if ctx.idAttr():
            trailer = [atom] + (trailer or [])
            atom = CodeStr(self.visit_with_disabled_scope(ctx.idAttr()).title())

        if trailer and len(trailer) > 0 and not isinstance(trailer[-1], list) and isinstance(atom, CodeStr) and isinstance(ctx.parentCtx, ctx.parser.CmdContext):
            return self.createIdAttr(atom, trailer)
        if ctx.atom().identifier() and isinstance(atom, CodeStr):
            return self.createIdAttr(atom, trailer)
        elif trailer:
            for i, t in enumerate(trailer):
                if isinstance(t, list):
                    trailer[i] = add_args_to_code('[{}]' if self.must_assign else '({})', t)
                else:
                    trailer[i] = '.' + trailer[i]
            return CodeStr(''.join([repr(self.visit(ctx.atom()))] + trailer))
        else:
            return self.visit(ctx.atom())

    def visitComplexId(self, ctx):
        return self.visitAtomExpr(ctx)

    def visitDeleteFile(self, ctx):
        kwargs = {}
        if ctx.ERASE():
            func = 'ERASE'
        else:
            func = 'DELETE_FILE'
        if ctx.RECYCLE():
            kwargs['recycle'] = True
        if ctx.specialExpr():
            args = [self.visit(ctx.specialExpr())]
        return make_func_code(func, *args, **kwargs)

    def visitCopyMoveFile(self, ctx):
        #self.imports.append('import shutil')
        args = self.list_visit(ctx.specialExpr()) #args = [fromFile, toFile]
        if ctx.RENAME():
            return make_func_code('RENAME', *args)
        else:
            return make_func_code('COPY_FILE', *args)

    def visitChMkRmDir(self, ctx):
        #self.imports.append('import os')
        funcname = 'os.' + {
            ctx.parser.CHDIR: 'CHDIR',
            ctx.parser.MKDIR: 'MKDIR',
            ctx.parser.RMDIR: 'RMDIR',
        }[ctx.children[0].symbol.type]
        return make_func_code(funcname, self.visit(ctx.specialExpr()))

    def visitSpecialExpr(self, ctx):
        return self.visit(ctx.pathname() or ctx.expr())

    def visitPathname(self, ctx):
        return ctx.getText()

    def convert_number(self, num_literal):
        num = num_literal.getText().lower()
        if 'x' in num or 'e' in num:
            if ('x' not in num and num[-1] == 'e') or ('x' in num and len(num) == 2):
                num += '0'
        return Number(num)

    def visitNumberOrCurrency(self, ctx):
        x = self.convert_number(ctx.NUMBER_LITERAL())
        if ctx.children[0].symbol.type == ctx.parser.DOLLAR:
            return make_func_code('CURRENCY', x)
        return x

    def visitBlob(self, ctx):
        blob = ctx.BLOB_LITERAL().getText()[2:]
        if len(blob) % 2:
            blob = '0' + blob
        blob_iter = iter(blob)
        return bytearray([int(x + y, 16) for x, y in zip(blob_iter, blob_iter)])

    def visitBoolOrNull(self, ctx):
        if ctx.NULL():
            return None
        txt = ctx.BOOLEANCHAR().getText().lower()
        if len(txt) == 1 and txt in 'fnty':
            return txt in 'ty'
        raise Exception('Can\'t convert boolean:' + ctx.getText())

    def visitDate(self, ctx):
        if not ctx.NUMBER_LITERAL():
            return None
        numbers = [self.convert_number(num) for num in ctx.NUMBER_LITERAL()]
        am_pm = (self.visit(ctx.identifier()) or '').lower()
        if any(not isinstance(num, int) for num in numbers) or am_pm not in ('', 'a', 'am', 'p', 'pm'):
            raise ValueError('invalid date/datetime')
        if am_pm in ('p', 'pm'):
            numbers[3] += 12
        if len(numbers) < 4:
            return make_func_code('dt.date', *numbers)
        return make_func_code('dt.datetime', *numbers)

    def visitString(self, ctx):
        return create_string(self.getCtxText(ctx)[1:-1])

    def visitPower(self, ctx):
        return self.operationExpr(ctx, '**')

    def visitMultiplication(self, ctx):
        return self.operationExpr(ctx, ctx.op.type)

    def visitAddition(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        #if not self.skip_extract and operation == ctx.parser.PLUS_SIGN:
        #    args = self.extract_args_from_addbs(ctx)
        #    self.skip_extract = True
        #    args = [self.visit(arg) for arg in args]
        #    check_expr = self.visit(ctx.expr(0))
        #    self.skip_extract = False
        #    if len(args) > 2 or args[0] != check_expr:
        #        return make_func_code('os.path.join', *args)
        if ctx.op.type == ctx.parser.PLUS_SIGN:
            if string_type(right):
                while isinstance(left, AddExpr) and left.op == '+' and string_type(left.right):
                    left, right = left.left, left.right + right
            if string_type(left) and string_type(right):
                return left + right
            return AddExpr(left, right)
        else:
            return SubExpr(left, right)

    def visitModulo(self, ctx):
        return self.operationExpr(ctx, '%')

    def extract_args_from_addbs(self, ctx):
        leftctx, rightctx = ctx.expr()
        if isinstance(leftctx, ctx.parser.AtomExprContext) and self.visit(leftctx.atom()) == 'addbs' and isinstance(leftctx.trailer(), ctx.parser.FuncCallTrailerContext):
            leftctx = leftctx.trailer().args().expr()
            if isinstance(leftctx, ctx.parser.AdditionContext):
                return self.extract_args_from_addbs(leftctx) + [rightctx]
        return [leftctx, rightctx]

    def operationExpr(self, ctx, operation):
        def add_parens(parent, child):
            expr = self.visit(child)
            if isinstance(child, ctx.parser.SubExprContext):
                return add_args_to_code('({})', (expr,))
            return expr
        left, right = [add_parens(ctx, expr) for expr in ctx.expr()]
        symbols = {
            '**': '**',
            '%': '%',
            ctx.parser.ASTERISK: '*',
            ctx.parser.FORWARDSLASH: '/',
            ctx.parser.MINUS_SIGN: '-'
        }
        return add_args_to_code('{} {} {}', (left, CodeStr(symbols[operation]), right))

    def visitSubExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitFuncDo(self, ctx):
        func = self.visit(ctx.specialExpr(0))

        kwargs = {}
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.specialExpr(1))
        if ctx.WITH():
            kwargs['WITH'] = tuple(self.visit(ctx.args(0)) or ())
        return make_func_code('DO', func, **kwargs)

    def visitDoForm(self, ctx):
        func = self.visit(ctx.specialExpr()) or '?'
        args = self.visit(ctx.args(0)) or []
        kwargs = {}
        if ctx.NAME():
            kwargs['NAME'] = ctx.nameId.getText()
            if ctx.LINKED():
                kwargs['LINKED'] = True
        if args:
            kwargs['WITH'] = tuple(args)
        if ctx.NOSHOW():
            kwargs['NOSHOW'] = True
        form_call = make_func_code('DO_FORM', func, **kwargs)
        if ctx.TO():
            return add_args_to_code('{} = {}', (self.visit(ctx.toId), form_call))
        else:
            return form_call

    def visitClearStmt(self, ctx):
        command = 'CLEAR'
        args = []
        kwargs = {}
        if len(ctx.children) > 1:
            if ctx.expr():
                args.append(self.visit(ctx.expr()))
            elif ctx.specialExpr():
                args.append(self.visit(ctx.specialExpr()))
            elif ctx.specialArgs():
                args += self.visit(ctx.specialArgs())
            elif ctx.READ() and ctx.ALL():
                kwargs['ALL'] = True
            command += '_' + create_string(ctx.children[1].getText().lower()).upper()
        return make_func_code(command, *args, **kwargs)

    def visitDllDeclare(self, ctx):
        dll_name = self.visit_with_disabled_scope(ctx.specialExpr())
        funcname = str(self.visit_with_disabled_scope(ctx.identifier()[0]))
        alias = str(self.visit_with_disabled_scope(ctx.alias)) if ctx.alias else None
        return make_func_code('DLL_DECLARE', dll_name, funcname, alias)

    def visitReadEvent(self, ctx):
        if ctx.EVENTS():
            return make_func_code('READ_EVENTS')

    def on_event(self, ctx, func_prefix):
        retval = []
        func = self.visit(ctx.cmd())
        if func:
            if isinstance(func, list) and len(func) == 1:
                func = func[0]
            if isinstance(ctx.cmd(), ctx.parser.AssignContext):
                retval += [add_args_to_code('def _FUNC():', (CodeStr(func_prefix.upper()),)), [[func]]]
                args = add_args_to_code('_FUNC', (CodeStr(func_prefix.upper()),)),
            else:
                args = add_args_to_code('lambda: {}', (func,)),
        else:
            args = ()
        return retval + [make_func_code(CodeStr(func_prefix), *args)]

    def visitOnStmt(self, ctx):
        if ctx.KEY():
            keys = [repr(str(self.visit(i))) for i in ctx.identifier()]
            return self.on_event(ctx, 'ON_KEY[{}]'.format(', '.join(keys)))
        elif ctx.SELECTION():
            return make_func_code('ON_SELECTION_BAR', int(ctx.NUMBER_LITERAL().getText()), add_args_to_code('lambda: {}', [self.visit(ctx.cmd())]))
        elif ctx.PAD() or ctx.BAR():
            if ctx.PAD():
                args = ['pad', self.visit(ctx.specialExpr(0)), self.visit(ctx.specialExpr(1))]
            else:
                args = ['bar', self.convert_number(ctx.NUMBER_LITERAL()), self.visit(ctx.specialExpr(0))]
            if ctx.ACTIVATE():
                args.append(('popup' if ctx.POPUP() else 'menu', self.visit(ctx.specialExpr()[-1])))
            return make_func_code('ON_PAD_BAR', *args)

        event = self.visit(ctx.identifier(0))
        if event == 'error':
            return self.on_event(ctx, 'ON_ERROR')
        elif event == 'shutdown':
            return self.on_event(ctx, 'ON_SHUTDOWN')
        elif event == 'escape':
            return self.on_event(ctx, 'ON_ESCAPE')

    def visitRaiseError(self, ctx):
        expr = [self.visit(ctx.expr())] or []
        return make_func_code('ERROR', *expr)

    def visitIdentifier(self, ctx):
        altermap = {
            'class': 'classtype'
        }
        identifier = ctx.getText().lower()
        return CodeStr(altermap.get(identifier, identifier))

    def visitReference(self, ctx):
        return make_func_code('REF', self.visit(ctx.idAttr()))

    def visitArrayIndex(self, ctx):
        if ctx.twoExpr():
            return self.visit(ctx.twoExpr())
        else:
            return [self.visit(ctx.expr())]

    def visitTwoExpr(self, ctx):
        return self.list_visit(ctx.expr())

    def visitFile(self, ctx):
        return ctx.getText()

    def visitRelease(self, ctx):
        if ctx.POPUP():
            args = self.visit(ctx.args())
            kwargs = {}
            if ctx.EXTENDED():
                kwargs['EXTENDED'] = True
            return make_func_code('RELEASE_POPUPS', *args, **kwargs)
        if ctx.ALL():
            return make_func_code('RELEASE_ALL')
        args = self.visit(ctx.specialArgs())
        args = [CodeStr(arg) if valid_identifier(arg) else arg for arg in args]
        if ctx.PROCEDURE():
            return make_func_code('RELEASE_PROCEDURE', *args)
        elif ctx.CLASSLIB():
            return make_func_code('RELEASE_CLASSLIB', *args)
        elif ctx.WINDOW():
            return make_func_code('RELEASE_WINDOW', *args)
        else:
            return make_func_code('RELEASE', *args)

    def visitCloseStmt(self, ctx):
        kwargs = {}
        if ctx.ALL():
            kwargs['ALL'] = True
        if ctx.TABLE():
            return make_func_code('CLOSE_TABLES', **kwargs)
        if ctx.INDEXES():
            return make_func_code('CLOSE_INDEXES', **kwargs)
        if ctx.DATABASE():
            return make_func_code('CLOSE_DATABASES', **kwargs)
        return make_func_code('CLOSE_ALL')

    def visitWaitCmd(self, ctx):
        if ctx.CLEAR():
            return CodeStr('WAIT_CLEAR()')
        kwargs = {}
        func = 'WAIT'
        message = self.visit(ctx.message)
        args = []
        if message:
            args.append(message)
        if ctx.WINDOW():
            func = 'WAIT_WINDOW'
            if ctx.AT():
                kwargs['AT'] = (self.visit(ctx.atExpr1), self.visit(ctx.atExpr2))
        if ctx.NOWAIT():
            kwargs['NOWAIT'] = True
        if ctx.NOCLEAR():
            kwargs['NOCLEAR'] = True
        if ctx.TIMEOUT():
            kwargs['TIMEOUT'] = self.visit(ctx.timeout)
        if ctx.TO():
            kwargs['TO'] = self.visit(ctx.toExpr)
        return make_func_code(func, *args, **kwargs)
        return make_func_code('WAIT', message, to=to_expr, window=window, nowait=nowait, noclear=noclear, timeout=timeout)

    def visitDeactivate(self, ctx):
        if ctx.MENU():
            func = 'DEACTIVATE_MENU'
        else:
            func = 'DEACTIVATE_POPUP'
        args = self.visit_with_disabled_scope(ctx.parameters()) if not ctx.ALL() else []
        return make_func_code(func, *[str(arg) for arg in args])

    def visitThrowError(self, ctx):
        return self.visitRaiseError(ctx) if ctx.expr() else CodeStr('raise')

    def visitCreateTable(self, ctx):
        if ctx.TABLE():
            func = 'CREATE_TABLE'
        elif ctx.DBF():
            func = 'CREATE_DBF'
        elif ctx.CURSOR():
            func = 'CREATE_CURSOR'
        tablename = self.visit(ctx.specialExpr())
        setupstring = '; '.join(self.visit(f) for f in ctx.tableField())
        kwargs = {}
        if ctx.FREE():
            kwargs['FREE'] = True
        return make_func_code(func, tablename, setupstring, **kwargs)

    def visitTableField(self, ctx):
        fieldname = self.visit(ctx.identifier(0))
        fieldtype = self.visit(ctx.identifier(1))
        fieldsize = self.visit(ctx.arrayIndex()) or (1,)
        if fieldtype.upper() == 'L' and len(fieldsize) == 1 and fieldsize[0] == 1:
            return '{} {}'.format(fieldname, fieldtype)
        else:
            return '{} {}({})'.format(fieldname, fieldtype, ', '.join(str(int(i)) for i in fieldsize))

    def visitAlterTable(self, ctx):
        tablename = self.visit(ctx.specialExpr())
        if ctx.ADD():
            setupstring = '; '.join(self.visit(f) for f in ctx.tableField())
        else:
            setupstring = str(self.visit(ctx.identifier(0)))
        kwargs = {
            ('ADD_COLUMN' if ctx.ADD() else 'DROP_COLUMN'): setupstring,
        }
        return make_func_code('ALTER_TABLE', tablename, **kwargs)

    def visitSelect(self, ctx):
        if ctx.tablename:
            return make_func_code('SELECT', self.visit(ctx.tablename))
        else:
            fields = self.visit(ctx.sqlselectFields())
            kwargs = {}
            if ctx.fromExpr:
                kwargs['FROM'] = self.visit(ctx.fromExpr)
            if ctx.intoExpr:
                kwargs['INTO'] = make_func_code('CURSOR' if ctx.CURSOR() else 'TABLE', self.visit(ctx.intoExpr))
            if ctx.whereExpr:
                kwargs['WHERE'] = self.make_lambda_from_expr(ctx.whereExpr)
            if ctx.orderbyid:
                kwargs['ORDER_BY'] = self.visit(ctx.orderbyid)
            if ctx.groupby:
                kwargs['GROUP_BY'] = self.visit(ctx.groupby)
            if ctx.havingExpr:
                kwargs['HAVING'] = self.make_lambda_from_expr(ctx.havingExpr)
            if ctx.DISTINCT():
                kwargs['DISTINCT'] = True
            return make_func_code('SQLSELECT', fields, **kwargs)

    def make_lambda_from_expr(self, exprctx):
        return add_args_to_code('lambda: {}', [self.visit(exprctx)])

    def visitSqlselectFields(self, ctx):
        if ctx.sqlselectField():
            return ', '.join(self.visit(field) for field in ctx.sqlselectField())
        else:
            return '*'

    def visitSqlselectField(self, ctx):
        if ctx.identifier():
            return '{} AS {}'.format(self.visit(ctx.expr()), self.visit(ctx.identifier()))
        return '{}'.format(self.visit(ctx.expr()))

    def visitFieldList(self, ctx):
        return ', '.join(self.visit(id) for id in ctx.identifier())

    def visitGoRecord(self, ctx):
        args = []
        kwargs = {}
        if ctx.TOP():
            args.append(CodeStr('TOP'))
        elif ctx.BOTTOM():
            args.append(CodeStr('BOTTOM'))
        else:
            args.append(self.visit(ctx.expr()))
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.specialExpr())
        return make_func_code('GOTO', *args, **kwargs)

    def visitUse(self, ctx):
        kwargs = OrderedDict()
        shared = ctx.SHARED()
        exclusive = ctx.EXCLUSIVE()
        if shared and exclusive:
            raise Exception('cannot combine shared and exclusive')
        name = self.visit(ctx.name)
        args = []
        if name:
            args.append(name)
        workarea = self.visit(ctx.workArea)
        if workarea is not None:
            kwargs['IN'] = workarea
        if shared:
            kwargs['SHARED'] = True
        elif exclusive:
            kwargs['EXCLUSIVE'] = True
        if ctx.aliasExpr:
            kwargs['ALIAS'] = self.visit(ctx.aliasExpr)
        return make_func_code('USE', *args, **kwargs)

    def visitLocate(self, ctx):
        kwargs = OrderedDict()
        scope, for_cond, while_cond, nooptimize = self.getQueryConditions(ctx.queryCondition())
        if scope:
            kwargs.update(scope)
        if for_cond:
            kwargs['FOR'] = for_cond
        if while_cond:
            kwargs['WHILE'] = while_cond
        if nooptimize:
            kwargs['NOOPTIMIZE'] = True
        return make_func_code('LOCATE', **kwargs)

    def visitContinueLocate(self, ctx):
        return make_func_code('CONTINUE')

    def visitAppendFrom(self, ctx):
        if ctx.ARRAY():
            return make_func_code('APPEND_FROM_ARRAY', self.visit(ctx.expr()))
        sourcename = self.visit(ctx.specialExpr(0))
        kwargs = {}
        if ctx.FOR():
            kwargs['FOR'] = add_args_to_code('lambda: {}', [self.visit(ctx.expr())])
        if ctx.typeExpr:
            kwargs['TYPE'] = self.visit(ctx.typeExpr)
        return make_func_code('APPEND_FROM', sourcename, **kwargs)

    def visitAppend(self, ctx):
        args = []
        kwargs = {}
        if ctx.BLANK():
            kwargs['BLANK'] = True
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.specialExpr())
        return make_func_code('APPEND', *args, **kwargs)

    def visitInsert(self, ctx):
        kwargs = {}
        kwargs['INTO'] = self.visit(ctx.intoExpr)
        if ctx.SELECT():
            kwargs2 = {}
            if ctx.specialArgs():
                args2 = [self.visit(ctx.specialArgs())]
            else:
                args2 = ['*']
            if ctx.fromExpr:
                kwargs2['FROM'] = self.visit(ctx.fromExpr)
            values = make_func_code('SQLSELECT', *args2, **kwargs2)
        elif ctx.ARRAY():
            kwargs['FROM'] = make_func_code('ARRAY', self.visit(ctx.arrayExpr))
        elif ctx.NAME():
            kwargs['FROM'] = make_func_code('NAME', self.visit(ctx.nameExpr))
        elif ctx.MEMVAR():
            kwargs['FROM'] = CodeStr('MEMVAR')
        else:
            values = self.visit(ctx.args())
            fields = self.visit(ctx.specialArgs())
            if fields:
                if len(fields) != len(values):
                    raise Exception('number of fields must match number of values')
                values = {field: value for field, value in zip(fields, values)}
            else:
                values = tuple(values)
            kwargs['VALUES'] = values
        return make_func_code('INSERT', **kwargs)

    def visitReplace(self, ctx):
        field = self.visit_with_disabled_scope(ctx.specialExpr(0))
        scope, for_cond, while_cond, nooptimize = self.getQueryConditions(ctx.queryCondition())
        args = [field]
        kwargs = {}
        if scope:
            kwargs.update(scope)
        if for_cond:
            kwargs['FOR'] = for_cond
        if while_cond:
            kwargs['WHILE'] = while_cond
        if nooptimize:
            kwargs['NOOPTIMIZE'] = True
        if ctx.expr(0):
            kwargs['WITH'] = self.visit(ctx.expr(0))
        return make_func_code('REPLACE', *args, **kwargs)

    def visitSkipRecord(self, ctx):
        kwargs = {}
        table = self.visit(ctx.specialExpr())
        if table:
            kwargs['IN'] = table
        args = []
        skipnum = self.visit(ctx.expr())
        if skipnum:
            args.append(skipnum)
        return make_func_code('SKIP', *args, **kwargs)

    def visitCopyTo(self, ctx):
        copyTo = self.visit(ctx.specialExpr(0))
        if ctx.STRUCTURE():
            return make_func_code('COPY_STRUCTURE', copyTo)
        kwargs = {}
        if ctx.TYPE():
            kwargs['TYPE'] = self.visit(ctx.specialExpr(1))
        return make_func_code('COPY_TO', copyTo, **kwargs)

    def visitSqlDelete(self, ctx):
        return make_func_code('SQLDELETE', FROM=self.visit(ctx.specialExpr()))

    def visitDeleteRecord(self, ctx):
        kwargs = OrderedDict()
        scope, for_cond, while_cond, nooptimize = self.getQueryConditions(ctx.queryCondition())
        kwargs = {}
        if scope:
            kwargs.update(scope)
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.inExpr)
        if for_cond:
            kwargs['FOR'] = for_cond
        if while_cond:
            kwargs['WHILE'] = while_cond
        if ctx.DELETE():
            func = 'DELETE'
        elif ctx.RECALL():
            func = 'RECALL'
        return make_func_code(func, **kwargs)

    def visitPack(self, ctx):
        if ctx.DATABASE():
            return make_func_code('PACK_DATABASE')
        elif ctx.DBF():
            func = 'PACK_DBF'
        elif ctx.MEMO():
            func = 'PACK_MEMO'
        else:
            func = 'PACK'
        tablename = self.visit(ctx.tableName)
        args = []
        kwargs = {}
        if tablename:
            args.append(tablename)
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.workArea)
        return make_func_code(func, *args, **kwargs)

    def visitIndexOn(self, ctx):
        args = [self.visit(ctx.specialExpr()[0])]
        kwargs = {}
        kwargs['TAG' if ctx.TAG() else 'TO'] = self.visit(ctx.specialExpr()[1])
        if ctx.COMPACT():
            kwargs['COMPACT'] = True
        if ctx.ASCENDING() and ctx.DESCENDING():
            raise Exception('Invalid statement: {}'.format(self.getCtxText(ctx)))
        if ctx.ASCENDING():
            kwargs['ASCENDING'] = True
        elif ctx.DESCENDING():
            kwargs['DESCENDING'] = True
        if ctx.UNIQUE():
            kwargs['UNIQUE'] = True
        elif ctx.CANDIDATE():
            kwargs['CANDIDATE'] = True
        if ctx.ADDITIVE():
            kwargs['ADDITIVE'] = True
        return make_func_code('INDEX_ON', *args, **kwargs)

    def visitCount(self, ctx):
        scope, for_cond, while_cond, nooptimize = self.getQueryConditions(ctx.queryCondition())
        kwargs = {}
        if scope:
            kwargs.update(scope)
        if for_cond:
            kwargs['FOR'] = for_cond
        if while_cond:
            kwargs['WHILE'] = while_cond
        if nooptimize:
            kwargs['NOOPTIMIZE'] = True
        self.must_assign = True
        to_val = self.visit(ctx.toExpr)
        self.must_assign = False
        return add_args_to_code('{} = {}', (to_val, make_func_code('COUNT', **kwargs)))

    def visitSum(self, ctx):
        scope, for_cond, while_cond, nooptimize = self.getQueryConditions(ctx.queryCondition())
        args = [add_args_to_code('lambda: {}', [self.visit(ctx.sumExpr)])]
        kwargs = {}
        if scope:
            kwargs.update(scope)
        if for_cond:
            kwargs['FOR'] = for_cond
        if while_cond:
            kwargs['WHILE'] = while_cond
        if nooptimize:
            kwargs['NOOPTIMIZE'] = True
        self.must_assign = True
        to_val = self.visit(ctx.toExpr)
        self.must_assign = False
        return add_args_to_code('{} = {}', (to_val, make_func_code('SUM', *args, **kwargs)))

    def getQueryConditions(self, conditions):
        scope, for_cond, while_cond, nooptimize = None, None, None, None
        condition_types = [(condition.FOR() or condition.WHILE() or condition.NOOPTIMIZE() or type(condition.scopeClause())) for condition in conditions]
        condition_types = [condition_type or condition_type.symbol.type for condition_type in condition_types]
        if len(set(condition_types)) < len(condition_types):
            raise Exception('Bad Query Condition')
        for condition in conditions:
            if condition.FOR():
                for_cond = add_args_to_code('lambda: {}', [self.visit(condition.expr())])
            if condition.WHILE():
                while_cond = add_args_to_code('lambda: {}', [self.visit(condition.expr())])
            if condition.scopeClause():
                scope = self.visit(condition.scopeClause())
            if condition.NOOPTIMIZE():
                nooptimize = True
        return scope, for_cond, while_cond, nooptimize


    def visitReindex(self, ctx):
        kwargs = {}
        if ctx.COMPACT():
            kwargs['COMPACT'] = True
        return make_func_code('REINDEX', **kwargs)

    def visitUpdateCmd(self, ctx):
        table = self.visit(ctx.tableExpr)
        set_fields = [(str(self.visit_with_disabled_scope(i)), self.visit(e)) for i, e in zip(ctx.identifier(), ctx.expr())]
        kwargs = {}
        if ctx.whereExpr:
            kwargs['where'] = add_args_to_code('lambda: {}', [self.visit(ctx.whereExpr)])
        if ctx.joinArgs:
            kwargs['join'] = self.visit(ctx.joinArgs)
        if ctx.fromArgs:
            kwargs['from_args'] = self.visit(ctx.fromArgs)
        return make_func_code('UPDATE', table, set_fields, **kwargs)

    def visitSeekRecord(self, ctx):
        seek_expr = self.visit(ctx.seekExpr)
        kwargs = OrderedDict()
        if ctx.orderExpr:
            kwargs['ORDER'] = self.visit(ctx.orderExpr)
        if ctx.tagName:
            kwargs['TAG'] = self.visit(ctx.tagName)
            if ctx.cdxFileExpr or ctx.idxFileExpr:
                kwargs['OF'] = self.visit(ctx.cdxFileExpr or ctx.idxFileExpr)
        if ctx.ASCENDING():
            kwargs['ASCENDING'] = True
        elif ctx.DESCENDING():
            kwargs['DESCENDING'] = True
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.tablenameExpr)
        return make_func_code('SEEK', seek_expr, **kwargs)

    def visitZapTable(self, ctx):
        kwargs = {}
        if ctx.IN():
            kwargs['IN'] = self.visit(ctx.specialExpr())
        return make_func_code('ZAP', **kwargs)

    def visitBrowse(self, ctx):
        return make_func_code('BROWSE')

    def visitScatterExpr(self, ctx):
        if len([x for x in (ctx.NAME(), ctx.MEMVAR(), ctx.TO()) if x]) > 1:
            raise Exception('Cannot combine NAME, MEMVAR or TO clauses in SCATTER command')
        kwargs = {}
        if ctx.FIELDS():
            fields = self.visit(ctx.specialArgs(0))
            if ctx.LIKE():
                kwargs['FIELDS'] = make_func_code('LIKE', fields)
            elif ctx.EXCEPT():
                kwargs['FIELDS'] = make_func_code('EXCEPT', fields)
            else:
                kwargs['FIELDS'] = fields
        if ctx.MEMO():
            kwargs['MEMO'] = True
        if ctx.BLANK():
            kwargs['BLANK'] = True
        if ctx.MEMVAR():
            kwargs['MEMVAR'] = True
        if ctx.NAME():
            kwargs['NAME'] = self.visit(ctx.expr(0))
            if ctx.ADDITIVE():
                kwargs['ADDITIVE'] = True
        func = make_func_code('SCATTER', **kwargs)
        if ctx.TO():
            name = self.visit(ctx.expr(0))
            return add_args_to_code('{} = {}', (name, func))
        return func

    def visitGatherExpr(self, ctx):
        kwargs = {}
        if ctx.FIELDS():
            fields = self.visit(ctx.args(0))
            if ctx.LIKE():
                fields = make_func_code('LIKE', fields)
            elif ctx.EXcept():
                fields = make_func_code('EXCEPT', fields)
            kwargs['FIELDS'] = fields
        if ctx.MEMO():
            kwargs['MEMO'] = True
        if ctx.MEMVAR():
            kwargs['MEMVAR'] = True
        if ctx.NAME():
            kwargs['NAME'] = self.visit(ctx.expr(0))
        if ctx.FROM():
            kwargs['FROM'] = self.visit(ctx.expr(0))
        return make_func_code('GATHER', **kwargs)

    def visitScopeClause(self, ctx):
        if ctx.ALL():
            return {'ALL': True}
        elif ctx.NEXT():
            return {'NEXT': self.visit(ctx.expr())}
        elif ctx.RECORD():
            return {'RECORD': self.visit(ctx.expr())}
        elif ctx.REST():
            return {'REST': True}
        else:
            return {}

    def visitReport(self, ctx):
        return make_func_code('REPORT_FORM', self.visit(ctx.specialExpr()))

    def visitSetCmd(self, ctx):
        setword = ctx.setword.text.lower()
        #kwargs = {'set_value': True}
        kwargs = {}
        args = ()
        if ctx.BAR():
            setword += ' bar'
        if setword == 'printer':
            if ctx.TO():
                if ctx.DEFAULT():
                    kwargs['DEFAULT'] = True
                elif ctx.NAME():
                    kwargs['NAME'] = self.visit(ctx.specialExpr()[0])
                elif ctx.specialExpr():
                    kwargs['TO'] = self.visit(ctx.specialExpr()[0])
                    if ctx.ADDITIVE():
                        kwargs['ADDITIVE'] = True
            else:
                args = ('ON' if ctx.ON() else 'OFF',)
                if ctx.PROMPT():
                    kwargs['PROMPT'] = True
        elif setword == 'typeahead':
            args = (self.visit(ctx.expr()[0]),)
        elif setword == 'procedure':
            if ctx.ADDITIVE():
                kwargs['ADDITIVE'] = True
            args = self.list_visit(ctx.specialExpr())
        elif setword == 'bell':
            args = ('TO', self.visit(ctx.specialExpr()[0])) if ctx.TO() else ('ON' if ctx.ON() else 'OFF',)
        elif setword in ('cursor', 'deleted', 'escape', 'exact', 'exclusive', 'multilocks', 'near', 'safety', 'status', 'status bar', 'tableprompt', 'talk', 'unique'):
            args = CodeStr('ON' if ctx.ON() else 'OFF'),
        elif setword == 'century':
            if ctx.TO():
                if len(ctx.expr()) > 0:
                    kwargs.update({'century': self.visit(ctx.expr()[0])})
                else:
                    kwargs.update({'century': 19})
                if len(ctx.expr()) > 1:
                    kwargs.update({'rollover': self.visit(ctx.expr()[1])})
                else:
                    kwargs.update({'rollover': 67})
            else:
                args = ('ON' if ctx.ON() else 'OFF',)
        elif setword == 'classlib':
            args = (self.visit(ctx.specialExpr(0)),)
            if ctx.IN():
                kwargs['class_file'] = self.visit(ctx.specialExpr(1))
            if ctx.ALIAS():
                kwargs['alias'] = self.visit(ctx.specialExpr(2 if ctx.IN() else 1))
            if ctx.ADDITIVE():
                kwargs['additive'] = True
        elif setword == 'compatible':
            args = ('ON' if ctx.ON() or ctx.DB4() else 'OFF',)
            if ctx.PROMPT() or ctx.NOPROMPT():
                args = (args[0], 'PROMPT' if ctx.PROMPT() else 'NOPROMPT')
        elif setword == 'sysmenu':
            args = [x.symbol.text.lower() for x in (ctx.ON(), ctx.OFF(), ctx.TO(), ctx.SAVE(), ctx.NOSAVE()) if x]
            if ctx.expr():
                args += [self.visit(ctx.expr()[0])]
            elif ctx.DEFAULT():
                args += ['default']
        elif setword == 'date':
            args = (str(self.visit_with_disabled_scope(ctx.identifier())),)
        elif setword == 'refresh':
            args = self.list_visit(ctx.expr())
            if len(args) < 2:
                args.append(5)
        elif setword == 'notify':
            arg = 'ON' if ctx.ON() else 'OFF'
            if ctx.CURSOR():
                kwargs.update({'cursor': arg})
            else:
                args = (arg,)
        elif setword == 'clock':
            args = [x.symbol.text.lower() for x in (ctx.ON(), ctx.OFF(), ctx.TO(), ctx.STATUS()) if x]
            if ctx.expr():
                args += self.list_visit(ctx.expr())
        elif setword == 'memowidth':
            args = (self.visit(ctx.expr()[0]),)
        elif setword == 'library':
            kwargs.update({'additive': True} if ctx.ADDITIVE() else {})
            args = self.list_visit(ctx.specialExpr())
        elif setword == 'filter':
            args = self.list_visit(ctx.specialExpr())
        elif setword == 'order':
            if ctx.TAG():
                kwargs['TAG'] = self.visit(ctx.specialExpr(0))
            elif ctx.specialExpr(0):
                args = self.visit(ctx.specialExpr(0)),
            if ctx.ofExpr:
                kwargs['OF'] = self.visit(ctx.ofExpr)
            if ctx.inExpr:
                kwargs['IN'] = self.visit(ctx.inExpr)
            if ctx.ASCENDING():
                kwargs['ASCENDING'] = True
            elif ctx.DESCENDING():
                kwargs['DESCENDING'] = True
        elif setword == 'index':
            args = (self.visit(ctx.specialExpr(0)),)
        elif setword == 'udfparms':
            if ctx.VALUE():
                kwargs['TO'] = CodeStr('VALUE')
            elif ctx.REFERENCE:
                kwargs['TO'] = CodeStr('REFERENCE')
            #args = ['value' if ctx.VALUE() else 'reference']
        elif setword == 'path':
            kwargs['TO'] = self.visit(ctx.specialExpr(0))
        else:
            return
        return make_func_code('SET_' + setword.upper().replace(' ', '_'), *args, **kwargs)

    def visitPush(self, ctx):
        pass

    def visitPop(self, ctx):
        pass

    def visitShellRun(self, ctx):
        start, stop = ctx.getSourceInterval()
        if ctx.identifier():
            pass #Add /N options
            start = ctx.identifier().getSourceInterval()[0]
        tokens = ctx.parser._input.tokens[start + 1:stop + 1]
        # FIXME: Need more cleanup on the arguments.
        command = ''.join(create_string(tok.text) for tok in tokens).strip().split()
        for i, arg in enumerate(command):
            if arg.startswith('&'):
                command[i] = CodeStr(arg[1:])
        return make_func_code('RUN', command)

    def visitReturnStmt(self, ctx):
        if not ctx.expr():
            return [CodeStr('return')]
        return [add_args_to_code('return {}', [self.visit(ctx.expr())])]

    def visitAssert(self, ctx):
        if ctx.expr(1):
            return add_args_to_code('assert {}, {}', (self.visit(ctx.expr(0)), self.visit(ctx.expr(1))))
        else:
            return add_args_to_code('assert {}', (self.visit(ctx.expr(0)),))

    def visitListStmt(self, ctx):
        pass

    def visitSaveToCmd(self, ctx):
        pass

    def visitUnlockCmd(self, ctx):
        pass

    def visitCompileCmd(self, ctx):
        pass

    def visitSortCmd(self, ctx):
        pass

    def visitCopyToArray(self, ctx):
        pass

    def visitRestoreCmd(self, ctx):
        pass

    def visitZoomCmd(self, ctx):
        pass

    def visitTextBlock(self, ctx):
        kwargs = {}
        if ctx.NOSHOW():
            kwargs['show'] = False
        text = self.visit(ctx.textChunk())
        val = make_func_code('TEXT', text, **kwargs)
        if ctx.TO():
            name = self.visit(ctx.idAttr(0))
            return add_args_to_code('{} = {}', [name, val])
        else:
            return val

    def visitTextChunk(self, ctx):
        start, stop = ctx.getSourceInterval()
        ltoks = ctx.parser._input.getHiddenTokensToLeft(start) or []
        rtoks = ctx.parser._input.getHiddenTokensToRight(stop) or []
        toks = ctx.parser._input.tokens[start:stop+1]
        text = ''.join(t.text for t in ltoks + toks + rtoks)
        return CodeStr('[' + ',\n'.join(repr(l) for l in text.splitlines()) + ']')

    def visitDefineMenu(self, ctx):
        menu_name = self.visit(ctx.specialExpr()[0])
        kwargs = {}
        if len(ctx.specialExpr()) > 1:
            kwargs['window'] = self.visit(ctx.specialExpr()[1])
        elif ctx.SCREEN():
            kwargs['window'] = CodeStr('SCREEN')
        if ctx.BAR():
            kwargs['bar'] = True
            if ctx.NUMBER_LITERAL():
                kwargs['line'] = self.convert_number(ctx.NUMBER_LITERAL())
        if ctx.NOMARGIN():
            kwargs['nomargin'] = True
        return make_func_code('DEFINE_MENU', menu_name, **kwargs)

    def visitDefinePad(self, ctx):
        if ctx.AT() or ctx.BEFORE() or ctx.AFTER() or ctx.NEGOTIATE() or ctx.FONT() or not ctx.MESSAGE() or not ctx.KEY() or ctx.MARK() or ctx.SKIPKW() or not ctx.COLOR():
            pass
        pad_name = str(self.visit(ctx.specialExpr(0)))
        menu_name = str(self.visit(ctx.specialExpr(1)))
        prompt = str(self.visit(ctx.expr(0)))
        kwargs = {}
        kwargs['message'] = self.visit(ctx.expr(1))
        kwargs['key'] = tuple(['+'.join(self.visit(identifier) for identifier in ctx.identifier())] + [self.visit(ctx.expr(2))] if len(ctx.expr()) > 2 else [])
        kwargs['color_scheme'] = self.convert_number(ctx.NUMBER_LITERAL(0))
        return make_func_code('DEFINE_PAD', pad_name, menu_name, prompt, **kwargs)

    def visitDefinePopup(self, ctx):
        popup_name = self.visit(ctx.specialExpr())
        kwargs = {}
        if ctx.SHADOW():
            kwargs['shadow'] = True
        if ctx.MARGIN():
            kwargs['margin'] = True
        if ctx.RELATIVE():
            kwargs['relative'] = True
        if ctx.NUMBER_LITERAL():
            kwargs['color_scheme'] = self.convert_number(ctx.NUMBER_LITERAL())
        return make_func_code('DEFINE_POPUP', popup_name, **kwargs)

    def visitDefineBar(self, ctx):
        bar_number = self.convert_number(ctx.NUMBER_LITERAL())
        menu_name = self.visit(ctx.specialExpr())
        prompt = self.visit(ctx.expr(0))
        kwargs = {}
        if ctx.MESSAGE():
            kwargs['message'] = self.visit(ctx.expr(1))
        return make_func_code('DEFINE_BAR', bar_number, menu_name, prompt, **kwargs)

    def visitActivateWindow(self, ctx):
        pass

    def visitActivateScreen(self, ctx):
        pass

    def visitActivateMenu(self, ctx):
        menu_name = self.visit(ctx.specialExpr(0))
        kwargs = {}
        if ctx.NOWAIT():
            kwargs['nowait'] = True
        if ctx.PAD():
            kwargs['pad'] = self.visit(ctx.specialExpr(1))
        return make_func_code('ACTIVATE_MENU', menu_name, **kwargs)

    def visitActivatePopup(self, ctx):
        pass

    def visitShowCmd(self, ctx):
        pass

    def visitHideCmd(self, ctx):
        pass

    def visitModifyWindow(self, ctx):
        pass

    def visitModifyFile(self, ctx):
        pass

    def visitRetry(self, ctx):
        return make_func_code('RETRY')

    def visitLabelCmd(self, ctx):
        kwargs = {}
        if ctx.formExpr:
            kwargs['FORM'] = self.visit(ctx.formExpr)
        if ctx.PRINTER():
            kwargs['TO'] = make_func_code('PRINTER')
        return make_func_code('LABEL', **kwargs)

    def visitExprCmd(self, ctx):
        exprs = tuple(self.visit(x) for x in ctx.expr())
        if len(exprs) == 1:
            return exprs[0]
        else:
            return CodeStr(repr(exprs)[1:-1])

    def visitComplexIdCmd(self, ctx):
        last_trailer = ctx.complexId()
        while last_trailer.trailer():
            last_trailer = last_trailer.trailer()
        if isinstance(last_trailer, ctx.parser.FuncCallTrailerContext):
            return self.visit(ctx.complexId())
        else:
            return make_func_code(self.visit(ctx.complexId()))
