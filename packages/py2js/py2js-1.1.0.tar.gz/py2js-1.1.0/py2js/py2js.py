import ast
from dataclasses import dataclass, field
import enum
import inspect
import re
import types
import typing as t
from functools import reduce

import jsbeautifier
from strbuilder import BaseBuilder, SurroundBuilder

from .visitor import Transformer, Visitor, VisitorContext

transformers: t.List['Transformer'] = []

BOOL_OP_TABLE = {
    ast.Or: '||',
    ast.And: '&&'
}
UNARY_OP_TABLE = {
    ast.Invert: '~',
    ast.Not: '!',
    ast.UAdd: '+',
    ast.USub: '-',
}
COMPARE_OP_TABLE = {
    ast.Eq: '==',
    ast.Is: '===',
    ast.Gt: '>',
    ast.Lt: '<',
    ast.IsNot: '!==',
    ast.NotIn: 'in',
    ast.In: 'in'
}
OPERATOR_OP_TABLE = {
    ast.Add: '+',
    ast.BitAnd: '&',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.Div: '/',
    ast.FloorDiv: '//',
    ast.LShift: '<<',
    ast.Mod: '%',
    ast.Mult: '*',
    ast.Pow: '**',
    ast.RShift: '>>',
    ast.Sub: '-',
}
CONSTANT_TABLE = {
}


class JSScope(enum.Enum):
    MODULE = 0
    CLASS_FIELD = 1
    FUNCTION_FIELD = 2
    ARGUMENT = 3
    F_STRING = 4
    FOR_LOOP = 5


@dataclass
class JSVisitorContext(VisitorContext):
    variables: t.List[str] = field(default_factory=list)
    scope: JSScope = field(default=JSScope.MODULE)
    bool_op_table: t.Dict[type, str] = field(default_factory=BOOL_OP_TABLE.copy)
    unary_op_table: t.Dict[type, str] = field(default_factory=UNARY_OP_TABLE.copy)
    compare_op_table: t.Dict[t.Any, str] = field(default_factory=COMPARE_OP_TABLE.copy)
    operator_op_table: t.Dict[type, str] = field(default_factory=OPERATOR_OP_TABLE.copy)
    constant_table: t.Dict[t.Any, str] = field(default_factory=CONSTANT_TABLE.copy)
    break_suffix: str = field(default='')
    parent: ast.AST = field(default=None)
    node: ast.AST = field(default=None)

    def copy(self, variables: t.Dict[str, t.Any] = None, node: t.Optional[ast.AST] = None, scope: t.Optional[JSScope] = None, break_suffix: t.Optional[str] = None) -> 'JSVisitorContext':
        return JSVisitorContext(
            variables=variables or self.variables,
            scope=scope or self.scope,
            bool_op_table=self.bool_op_table,
            unary_op_table=self.unary_op_table,
            compare_op_table=self.compare_op_table,
            operator_op_table=self.operator_op_table,
            constant_table=self.constant_table,
            break_suffix=self.break_suffix if break_suffix is None else break_suffix,
            parent=self.node,
            node=node or self.node
        )


class CodeGen(Visitor[JSVisitorContext]):
    def __init__(self, python_compatible: bool = False) -> None:
        self.python_compatible = python_compatible
        super().__init__(JSVisitorContext, transformers=transformers)

    def sperator(self, ast: t.Union[t.List[ast.AST], ast.AST], context: t.Optional[JSVisitorContext] = None):
        if context.scope == JSScope.ARGUMENT:
            return ','
        return ';'

    def visit_Module(self, node: ast.Module, ctx: JSVisitorContext):
        return self.visit(node.body, ctx)

    def visit_Import(self, node: ast.Import, ctx: JSVisitorContext):
        return [f'import {x.asname or x.name} from "{x.name}"' for x in node.names]

    def visit_ImportFrom(self, node: ast.ImportFrom, ctx: JSVisitorContext):
        multiple = len(node.names) > 1
        first = node.names[0]
        return BaseBuilder('import')\
            .write_if(multiple,
                      lambda: SurroundBuilder(surround='{}')
                      .write(BaseBuilder(separator=',').write(BaseBuilder(x.name).write_if(x.asname, BaseBuilder('as').write(x.asname)) for x in node.names)),
                      or_else=BaseBuilder(f'* as {node.module}') if first.name == '*' else SurroundBuilder(first.name, surround='{}').write_if(first.asname, BaseBuilder('as').write(first.asname))
                      )\
            .write('from')\
            .write(SurroundBuilder(node.module))\
            .build()

    def visit_ClassDef(self, node: ast.ClassDef, ctx: JSVisitorContext):
        context = ctx.copy(scope=JSScope.CLASS_FIELD)

        body = node.body

        builder = BaseBuilder()\
            .write(f'let {node.name} = class')\
            .write(SurroundBuilder(surround='{}')
                   .write_if(self.python_compatible, '''constructor(...args) {if ('__init__' in this) this.__init__(this, ...args); return new Proxy(this, { apply: (target, self, args) => target.__call__(self, ...args), get: (target, prop, receiver) => {if (target[prop] instanceof Function) {return (...args) => target[prop](target, ...args)} else {return target[prop]}}})}''')
                   .write(self.visit(node.body, context))
                   .write(self.visit(filter(lambda node: not isinstance(node, ast.FunctionDef), body), context)))\
            .write_if(node.bases, (lambda: f'''Object.getOwnPropertyNames({base}.prototype).forEach(name => {{if (name !== 'constructor') {{{node.name}.prototype[name] = {base}.prototype[name];}}}});''' for base in map(lambda base: self.visit(base, ctx), node.bases)))\
            .write(f'{node.name} = new Proxy({node.name}, {{ apply: (clazz, thisValue, args) => new clazz(...args) }});')\
            .write_if(node.decorator_list, (f'{node.name} = ', reduce(lambda value, element: f'{element}({value})', map(lambda decorator: self.visit(decorator, ctx), node.decorator_list), node.name), ';'))

        return builder.build()

    def visit_FunctionDef(self, node: ast.FunctionDef, ctx: JSVisitorContext):
        context = ctx.copy()
        context.scope = JSScope.FUNCTION_FIELD

        if ctx.scope == JSScope.CLASS_FIELD:
            return BaseBuilder()\
                .write(node.name)\
                .write(f'{self.visit(node.args, ctx)}')\
                .write(SurroundBuilder(surround='{}')
                       .write(self.visit(node.body, context)))\
                .build()
        builder = BaseBuilder()\
            .write_if(node.name not in ctx.variables, 'let')\
            .write(node.name)\
            .write('=')\
            .write(f'{self.visit(node.args, ctx)} =>')\
            .write(SurroundBuilder(surround='{}')
                   .write(self.visit(node.body, context)))
        ctx.variables.append(node.name)
        return builder.build()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef, ctx: JSVisitorContext):
        context = ctx.copy(scope=JSScope.FUNCTION_FIELD)

        if ctx.scope == JSScope.CLASS_FIELD:
            return BaseBuilder()\
                .write(node.name)\
                .write(f'{self.visit(node.args, ctx)}')\
                .write(SurroundBuilder(surround='{}')
                       .write(self.visit(node.body, context)))\
                .build()
        return BaseBuilder('let')\
            .write(node.name)\
            .write('=')\
            .write(f'async {self.visit(node.args, ctx)} =>')\
            .write(SurroundBuilder(surround='{}')
                   .write(self.visit(node.body, context)))\
            .build()

    def visit_If(self, node: ast.If, ctx: JSVisitorContext):
        return BaseBuilder('if').write(SurroundBuilder(surround='()').write(self.visit(node.test, ctx))).write(SurroundBuilder(surround='{}').write(self.visit(node.body, ctx))).build()

    def visit_Compare(self, node: ast.Compare, ctx: JSVisitorContext):
        ops = BaseBuilder()
        invert = False
        for op in node.ops:
            op_type = type(op)
            ops.write(ctx.compare_op_table[op_type])
            if op_type == ast.NotIn:
                invert = True
            
        builder = BaseBuilder(self.visit(node.left, ctx))
        comparators = node.comparators
        while comparators:
            builder.write(ops.pop(0))
            builder.write(self.visit(comparators.pop(0)))
        if not invert:
            return builder.build()
        return f'!({builder.build()})'

    def visit_Name(self, node: ast.Name, ctx: JSVisitorContext):
        return node.id

    def visit_Constant(self, node: ast.Constant, ctx: JSVisitorContext):
        if node.value is None:
            return 'null'
        if isinstance(node.value, bool):
            return 'true' if node.value else 'false'
        if node.value in ctx.constant_table:
            return ctx.constant_table[node.value]
        if ctx.scope != JSScope.F_STRING and isinstance(node.value, str):
            return f'`{node.value}`'
        else:
            return f'{node.value}'

    def visit_Assign(self, node: ast.Assign, ctx: JSVisitorContext):
        builder = BaseBuilder(separator=';')

        defines = [target.id for target in node.targets if isinstance(target, ast.Name) and target.id not in ctx.variables]
        ctx.variables.extend(defines)

        if len(node.targets) == len(defines):
            builder.write(f'let {", ".join(defines)} = {self.visit(node.value, ctx)}')
            return builder.build()
        elif defines:
            builder.write(f'let {", ".join(defines)}')
        builder.write(f'{self.visit(node.targets, ctx)} = {self.visit(node.value, ctx)}')
        return builder.build()
        # return BaseBuilder().write_if(node.targets in ctx.variables and ctx.scope != JSScope.CLASS_FIELD and not any(map(lambda target: isinstance(target, ast.Attribute), node.targets)), 'let').write(f'{self.visit(node.targets, ctx)} = {self.visit(node.value, ctx)}').build()

    def visit_Call(self, node: ast.Call, ctx: JSVisitorContext):
        context = ctx.copy(scope=JSScope.ARGUMENT)

        starreds = tuple(filter(lambda arg: isinstance(arg, ast.Starred), node.args))
        args = filter(lambda arg: not isinstance(arg, ast.Starred), node.args)

        return BaseBuilder(f'{self.visit(node.func, ctx)}')\
            .write(SurroundBuilder(surround='()', separator=',')
                   .write_if(args, lambda: self.visit(args, context))
                   .write_if(node.keywords, lambda: SurroundBuilder(surround='{}', separator=',')
                                 .write(self.visit(filter(lambda kw: kw.arg is not None, node.keywords), context))
                                 .write(self.visit(filter(lambda kw: kw.arg is None, node.keywords), context)))
                   .write_if(starreds, lambda: self.visit(starreds, context))
                   ).build()

    def visit_keyword(self, node: ast.keyword, ctx: JSVisitorContext):
        return f'{node.arg}:{self.visit(node.value)}' if node.arg is not None else f'...{self.visit(node.value)}'

    def visit_arguments(self, node: ast.arguments, ctx: JSVisitorContext):
        context = ctx.copy(scope=JSScope.ARGUMENT)

        kwlen = len(node.defaults)
        kwargs = node.args[-kwlen:]
        args = node.args[:len(node.args)-kwlen]
        keywords = dict(zip(kwargs, node.defaults))

        return SurroundBuilder(surround='()')\
            .write(
            BaseBuilder(separator=',')
            .write_if(node.args, self.visit(args, context))
            .write_if(node.kwarg or node.defaults, lambda:
                      SurroundBuilder(surround='{}', separator=',')
                      .write_if(keywords, lambda: (f'{self.visit(k, context)}={self.visit(v, context)}' for k, v in keywords.items()))
                      .write_if(node.kwarg, lambda: f'...{self.visit(node.kwarg, context)}')
                      .build())
            .write_if(node.vararg, lambda: f'...{self.visit(node.vararg, context)}')
            .build()
        ).build()

    def visit_Attribute(self, node: ast.Attribute, ctx: JSVisitorContext):
        return f'{self.visit(node.value, ctx)}.{node.attr}'

    def visit_Expr(self, node: ast.Expr, ctx: JSVisitorContext):
        return self.visit(node.value, ctx)

    def visit_NamedExpr(self, node: ast.NamedExpr, ctx: JSVisitorContext):
        return f'{self.visit(node.target, ctx)}={self.visit(node.value, ctx)}'

    def visit_arg(self, node: ast.arg, ctx: JSVisitorContext):
        return node.arg

    def visit_Return(self, node: ast.Return, ctx: JSVisitorContext):
        return f'return {self.visit(node.value, ctx)}'

    def visit_List(self, node: ast.List, ctx: JSVisitorContext):
        return SurroundBuilder(surround='[]', separator=',').write(map(lambda item: self.visit(item, ctx), node.elts)).build()

    def visit_Tuple(self, *args):
        return f'/*tuple*/{self.visit_List(*args)}'

    def visit_Dict(self, node: ast.Dict, ctx: JSVisitorContext):
        return '{%s}' % ', '.join(f'{self.visit(key, ctx.copy(scope=JSScope.F_STRING))}: {self.visit(value, ctx)}' for key, value in zip(node.keys, node.values))

    def visit_Lambda(self, node: ast.Lambda, ctx: JSVisitorContext):
        return f'{self.visit(node.args, ctx)}=> {{return {self.visit(node.body, ctx)}}}'

    def visit_For(self, node: ast.For, ctx: JSVisitorContext):
        return (
            BaseBuilder()
            .write_if(node.orelse, '_else: {')
            .write(f'for ({self.visit(node.target, ctx)} of {self.visit(node.iter, ctx)})')
            .write(f"{{{self.visit(node.body, ctx.copy(break_suffix='_else' if node.orelse else ''))}}}")
            .write_if(node.orelse, f'{self.visit(node.orelse, ctx)} }}')
        ).build()

    def visit_AsyncFor(self, node: ast.AsyncFor, ctx: JSVisitorContext):
        return (
            BaseBuilder()
            .write_if(node.orelse, '_else: {')
            .write(f'for await ({self.visit(node.target, ctx)} of {self.visit(node.iter, ctx)})')
            .write(f"{{{self.visit(node.body, ctx.copy(break_suffix='_else' if node.orelse else ''))}}}")
            .write_if(node.orelse, f'{self.visit(node.orelse, ctx)} }}')
        ).build()

    def visit_Await(self, node: ast.Await, ctx: JSVisitorContext):
        return f'await {self.visit(node.value, ctx)}'

    def visit_BoolOp(self, node: ast.BoolOp, ctx: JSVisitorContext):
        return ctx.bool_op_table[type(node.op)].join(map(lambda value: self.visit(value, ctx), node.values))

    def visit_UnaryOp(self, node: ast.UnaryOp, ctx: JSVisitorContext):
        return f'{ctx.unary_op_table[type(node.op)]}{self.visit(node.operand, ctx)}'

    def visit_ListComp(self, node: ast.ListComp, ctx: JSVisitorContext):
        return f'{self.visit(node.generators, ctx)}'

    def visit_DictComp(self, node: ast.DictComp, ctx: JSVisitorContext):
        "Object.fromEntries([1,2,3].map(n=>[n,1]))"
        return f'Object.fromEntries({self.visit(node.generators, ctx)})'

    def visit_comprehension(self, node: ast.comprehension, ctx: JSVisitorContext):
        builder = BaseBuilder(f'{self.visit(node.iter, ctx)}')
        builder.write_if(node.ifs, (f'.filter({self.visit(x, ctx)})' for x in node.ifs))

        if isinstance(ctx.parent, ast.DictComp):
            builder.write(f'.map(({self.visit(node.target, ctx)})=>[{self.visit(ctx.parent.key, ctx)}, {self.visit(ctx.parent.value, ctx)}])')
        else:
            builder.write(f'.map(({self.visit(node.target, ctx)})=>{self.visit(ctx.parent.elt, ctx)})')

        return builder.build()

    def visit_IfExp(self, node: ast.IfExp, ctx: JSVisitorContext):
        return f'{self.visit(node.test, ctx)} ? {self.visit(node.body, ctx)} : {self.visit(node.orelse, ctx)}'

    def visit_Starred(self, node: ast.Starred, ctx: JSVisitorContext):
        return f'...{self.visit(node.value, ctx)}'

    def visit_BinOp(self, node: ast.BinOp, ctx: JSVisitorContext):
        return f'{self.visit(node.left, ctx)}{ctx.operator_op_table[type(node.op)]}{self.visit(node.right, ctx)}'

    def visit_AnnAssign(self, node: ast.AnnAssign, ctx: JSVisitorContext):
        if isinstance(node.target, ast.Name):
            ctx.variables.append(node.target.id)
        return BaseBuilder().write_if(not isinstance(node.target, ast.Attribute) and ctx.scope != JSScope.CLASS_FIELD, 'let').write(f'{self.visit(node.target, ctx)}').write_if(node.value is not None, f'={self.visit(node.value, ctx)}').build()

    def visit_Pass(self, node: ast.Pass, ctx: JSVisitorContext):
        return '/* pass */'

    def visit_With(self, node: ast.With, ctx: JSVisitorContext):
        builder = SurroundBuilder(surround='{}', separator=';')
        builder.write(
            BaseBuilder('let')
            .write(SurroundBuilder(surround='[]', separator=',')
                   .write(f'_with_{i}' for i, expr in enumerate(node.items)))
            .write('=')
            .write(SurroundBuilder(surround='[]', separator=',').write(f'{self.visit(expr.context_expr)}' for expr in node.items))
        )\
            .write(BaseBuilder(separator=';').write(BaseBuilder().write_if(expr.optional_vars, f'{self.visit(expr.optional_vars)}=').write(f'_with_{i}.__enter__()') for i, expr in enumerate(node.items)))\
            .write(self.visit(node.body))\
            .write(BaseBuilder(separator=';').write(BaseBuilder().write_if(expr.optional_vars, f'{self.visit(expr.optional_vars)}=').write(f'_with_{i}.__exit__()') for i, expr in enumerate(node.items)))

        return builder.build()

    def visit_JoinedStr(self, node: ast.JoinedStr, ctx: JSVisitorContext):
        context = ctx.copy(scope=JSScope.F_STRING)
        return '`{}`'.format(''.join(map(lambda item: self.visit(item, context), node.values)))

    def visit_FormattedValue(self, node: ast.FormattedValue, ctx: JSVisitorContext):
        return f'${{{self.visit(node.value, ctx)}}}'

    def visit_Delete(self, node: ast.Delete, ctx: JSVisitorContext):
        return ';'.join(map(lambda target: f'delete {self.visit(target, ctx)}', node.targets))

    def visit_AugAssign(self, node: ast.AugAssign, ctx: JSVisitorContext):
        return f'{self.visit(node.target, ctx)} {ctx.operator_op_table[type(node.op)]}= {self.visit(node.value, ctx)}'

    def visit_Subscript(self, node: ast.Subscript, ctx: JSVisitorContext):
        return f'{self.visit(node.value, ctx)}[{self.visit(node.slice, ctx)}]'

    def visit_While(self, node: ast.While, ctx: JSVisitorContext):
        return 'while (%s) {%s}' % (self.visit(node.test, ctx), self.visit(node.body, ctx))

    def visit_Raise(self, node: ast.Raise, ctx: JSVisitorContext):
        return f'throw {self.visit(node.exc, ctx)}'

    def visit_Break(self, node: ast.Break, ctx: JSVisitorContext):
        return f'break {ctx.break_suffix}'

    def visit_Continue(self, node: ast.Continue, ctx: JSVisitorContext):
        return 'continue'

    def visit_Assert(self, node: ast.Assert, ctx: JSVisitorContext):
        return f'console.assert({self.visit(node.test, ctx)})'

    def visit_Try(self, node: ast.Try, ctx: JSVisitorContext):
        return (
            BaseBuilder(separator='')
            .write_if(node.orelse, '_else: {')
            .write(f'try {{{self.visit(node.body, ctx)}}}')
            .write_if(node.handlers, "catch(_err) {%s}" % '\n'.join(
                BaseBuilder()
                .write_if(handler.type, f'if (_err instanceof {self.visit(handler.type, ctx)})')
                .write(SurroundBuilder(surround='{}', separator=';')
                       .write_if(handler.name, f'{handler.name} = _err')
                       .write(self.visit(handler.body, ctx))
                       .write_if(node.orelse, 'break _else')
                       )
                .build()
                for handler in node.handlers
            ))
            .write_if(node.finalbody, BaseBuilder(f'finally {{{self.visit(node.finalbody, ctx)}').write('}'))
            .write_if(node.orelse, f'{self.visit(node.orelse, ctx)}}}')
        ).build()

    def visit_Match(self, node: ast.Match, ctx: JSVisitorContext):
        return '/*@deprecated match not supported */'


space_regex = re.compile('\s+')


def js(func: t.Optional[t.Callable] = None, as_function: bool = False, python_compatible: bool = False) -> str:
    def wrapper(func):
        lines = inspect.getsourcelines(func)[0]

        if not as_function:
            while lines:
                line = lines[0].strip()
                if line.startswith('@'):
                    lines.pop(0)
                elif line.startswith('def'):
                    lines.pop(0)
                    break
                else:
                    break

        if not lines:
            return ''

        match = space_regex.match(lines[0]).group() if lines[0].startswith(' ') else ''
        if match:
            spaces = len(match)
            lines = list(map(lambda line: line[spaces:], lines))

        return convert(''.join(lines), python_compatible=python_compatible)

    if func is None:
        return wrapper

    return wrapper(func)


def convert(
    source: t.Union[str, ast.AST, types.ModuleType, types.FunctionType],
    formatter: t.Optional[t.Callable[[str], str]] = jsbeautifier.beautify,
    code_gen: t.Optional[Visitor] = None,
    python_compatible: bool = False
):
    generator = code_gen or CodeGen(python_compatible=python_compatible)

    if isinstance(source, ast.AST):
        parsed = source
    elif isinstance(source, str):
        parsed = ast.parse(source)
    else:
        parsed = ast.parse(inspect.getsource(source))

    return formatter(generator.visit(parsed))
