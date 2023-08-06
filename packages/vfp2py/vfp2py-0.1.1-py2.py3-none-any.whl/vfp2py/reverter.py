import logging
import types
import io
import ast
import tokenize
from types import ModuleType
import decimal


DEBUG = logging.getLogger(__name__).debug


def nojoin(args):
    return args


def commajoin(args):
    return [', '.join(args)]


CMD_ARGS = {
    'SQLSELECT': (['SELECT'], commajoin, ('FROM', 'INTO', 'WHERE', 'GROUP_BY', 'HAVING')),
    'INDEX_ON': ('TAG', 'ASCENDING', 'DESCENDING'),
    'RETRY': (),
    'COPY_TO': (),
    'ON_SELECTION_BAR': (),
    'NODEFAULT': (),
    'GOTO': ('TOP', 'BOTTOM'),
    'DO': ('IN', 'WITH'),
    'DO_FORM': ('IN', 'WITH', 'NAME', 'LINKED'),
    'PUBLIC': (commajoin, ()),
}

ARGSTARTS = {key: val[0] for key, val in CMD_ARGS.items() if val and isinstance(val[0], (tuple, list))}
CMD_ARGS = {key: val[1:] if key in ARGSTARTS else val for key, val in CMD_ARGS.items()}
ARGJOINERS = {key: val[0]  for key, val in CMD_ARGS.items() if val and isinstance(val[0], types.FunctionType)}
CMD_ARGS = {key: val[1:][0] if key in ARGJOINERS else val for key, val in CMD_ARGS.items()}
VALID_KW = CMD_ARGS
COMMANDS = set(CMD_ARGS)


class VFPCommand:
    def __init__(self, something):
        self.something = something

    @classmethod
    def create_cmd(cls, name, args, kwargs):
        if name not in VALID_KW:
            raise Exception('not a command')
        invalid_kwargs = set(kwargs).difference(VALID_KW[name])
        if name != 'PUBLIC' and invalid_kwargs:
            raise Exception('invalid keyword{}: {}'.format('s' if len(invalid_kwargs) > 1 else '', ', '.join(invalid_kwargs)))
        something = ARGSTARTS.get(name, name.split('_')) + ARGJOINERS.get(name, nojoin)(args)
        for key, val in kwargs.items():
            something.append(key)
            something.append(val)
        return cls(' '.join(something))


FUNCSTART = 'PROCEDURE'
FUNCEND = 'ENDPROC'
class VFPFunctionDef:
    def __init__(self, funcname, parameters, args, body):
        self.funcname = funcname
        self.parameters = parameters and args
        self.args = args
        self.body = body

    def __repr__(self):
        if self.funcname == 'MAIN':
            something = ''
            if self.args:
                something += '   ' + ('' if self.parameters else 'L') + 'PARAMETERS {}\n'.format(', '.join(arg.upper() for arg in self.args))
        else:
            something = FUNCSTART + ' {}'.format(self.funcname.upper())
            something += ('\n   PARAMETERS {}\n' if self.parameters else '({})\n').format(', '.join(arg.upper() for arg in self.args))
        for line in self.body:
            if isinstance(line, VFPCommand):
                line = line.something
            something += '   ' + line + '\n'
        something += FUNCEND + '\n'
        return something


class VFPClassDef:
    def __init__(self, name, args, body):
        assert len(args) <= 1
        self.name = name
        self.args = args
        self.body = body

    def __repr__(self):
        something = 'DEFINE CLASS {}'.format(self.name.upper())
        if self.args:
            something += ' AS {}'.format(self.args[0].upper())
        something += '\n'
        lines = []
        for line in self.body:
            if isinstance(line, VFPFunctionDef):
                lines += repr(line).splitlines()
            else:
                lines.append(line)
        for line in lines:
            something += '   ' + line + '\n'
        something += 'ENDDEFINE\n'
        return something


class VFP2PyTransformer(ast.NodeVisitor):
    def __init__(self, source, *args, **kwargs):
        self.tokens = {token[2]: token[1] for token in tokenize.generate_tokens(io.StringIO(source).readline)}
        super().__init__(*args, **kwargs)

    def convert_call_to_cmd(self, node):
        args = [self.visit(arg) for arg in node.args]
        kwargs = {arg.arg: self.visit(arg.value) for arg in node.keywords}
        x = VFPCommand.create_cmd(node.func.id, args, kwargs)
        return x

    def visit_FunctionDef(self, node):
        if node.decorator_list and node.decorator_list[0].id == 'PURE':
            return None
        parameters = 'PARAMETERS' in [x.id for x in node.decorator_list] and node.args.args
        if node.name == 'MAIN':
            if node.args.args:
                print('   ' + ('' if parameters else 'L') + 'PARAMETERS {}'.format(', '.join(arg.upper() for arg in self.args)))
        else:
            print(FUNCSTART + ' {}'.format(node.name.upper()), end='')
            print(('\n   PARAMETERS {}' if self.parameters else '({})').format(', '.join(arg.upper() for arg in self.args)))
        body = []
        for child in node.body:
            if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
                if isinstance(child.value.func, ast.Name) and child.value.func.id.isupper() and child.value.func.id in COMMANDS:
                    body.append(self.convert_call_to_cmd(child.value))
                else:
                    body.append(self.visit(child.value))
            else:
                body.append(self.visit(child))
            print(body[-1])
            print(body[-1].something)
        return VFPFunctionDef(node.name, 'PARAMETERS' in [x.id for x in node.decorator_list], [arg.arg for arg in node.args.args], body)

    def visit_ClassDef(self, node):
        if node.decorator_list and node.decorator_list[0].id == 'PURE':
            return None
        return VFPClassDef(node.name, [arg.id for arg in node.bases], [self.visit(x) for x in node.body])

    def visit_Module(self, node):
        try:
            main_idx = next(i for i, child in enumerate(node.body) if isinstance(child, ast.FunctionDef) and child.name == 'MAIN')
        except StopIteration:
            main_idx = None
        if main_idx is not None:
            child = self.visit(node.body[main_idx])
            print(repr(child), end='')
        for i, child in enumerate(node.body):
            if i == main_idx:
                continue
            child = self.visit(child)
            if child is not None:
                print(repr(child), end='')

    def visit_Return(self, node):
        return 'RETURN' if not node.value else 'RETURN {}'.format(self.visit(node.value))

    def visit_Assign(self, node):
        import pdb
        pdb.set_trace()
        targets = [self.visit(target).upper() for target in node.targets]
        value = self.visit(node.value)
        if len(targets) > 1:
            return VFPCommand('STORE {} TO {}'.format(value, ', '.join(targets)))
        else:
            return VFPCommand('{} = {}'.format(targets[0], value))

    def visit_Lambda(self, node):
        try:
            return self.convert_call_to_cmd(node.body).something
        except Exception:
            return self.visit(node.body)

    def visit_Compare(self, node):
        return self.visit(node.left) + ''.join(self.visit(op) + self.visit(val) for op, val in zip(node.ops, node.comparators))

    def visit_BinOp(self, node):
        op = {
            ast.Add: ' + ',
            ast.Sub: ' - ',
            ast.Mult: ' * ',
            ast.Div: ' / ',
        }[type(node.op)]
        return self.visit(node.left) + op + self.visit(node.right)

    def visit_BoolOp(self, node):
        op = {
            ast.Or: ' OR ',
            ast.And: ' AND ',
        }[type(node.op)]
        return op.join(self.visit(val) for val in node.values)

    def visit_Eq(self, node):
        return ' = '

    def visit_Is(self, node):
        return ' == '

    def visit_Call(self, node):
        args = [self.visit(arg) for arg in node.args] + [arg.arg + '=' + self.visit(arg.value) for arg in node.keywords]
        if isinstance(node.func, ast.Name) and node.func.id == 'TABLE':
            return 'TABLE (' + args[0] + ')'
        else:
            name = self.visit(node.func)
            return '{}({})'.format(name, ', '.join(args))

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id == 'm':
            val = 'm'
        else:
            val = self.visit(node.value)
        return val + '.' + node.attr.upper()

    def visit_Name(self, node):
        return node.id.upper()

    def visit_Tuple(self, node):
        return ', '.join(self.visit(item) for item in node.elts)

    def visit_List(self, node):
        raise Exception('Lists not allowed')

    def visit_Dict(self, node):
        raise Exception('Dictionaries not allowed')

    def visit_Set(self, node):
        raise Exception('Sets not allowed')

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            return repr(node.value)
        elif isinstance(node.value, bool):
            return '.T.' if node.value else '.F.'
        elif node.value is None:
            return '.NULL.'
        literal_string = self.tokens[(node.lineno, node.col_offset)]
        return literal_string
        node.value = decimal.Decimal(literal_string)
        return node
 

def revert(file):
    with open(file) as fid:
        source = fid.read()
    module_ast = ast.parse(source)
    modified = VFP2PyTransformer(source).visit(module_ast)
    #print(modified)


def main():
    import sys
    logging.basicConfig(level=logging.DEBUG)
    revert(sys.argv[1])


if __name__ == '__main__':
    main()
