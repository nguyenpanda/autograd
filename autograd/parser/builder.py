import ast

from ..core import *
from ..func import *
from ..func.logarithm import all_classes as _all_logarithm_classes_
from ..func.trigo import all_classes as _all_trigo_classes_


class ExpressionBuilder:
    _operators_: dict[str, Operator] = {
        ast.Add.__name__: Plus,
        ast.Sub.__name__: Minus,
        ast.Mult.__name__: Multiply,
        ast.Div.__name__: Divide,
        ast.Pow.__name__: Power,
        ast.BitXor.__name__: Power,
    }

    _functions_: dict[str, Function] = {
        **{k.lower(): v for k, v in _all_logarithm_classes_.items()},
        **{k.lower(): v for k, v in _all_trigo_classes_.items()},
    }

    _binary_functions_: dict[str, Function] = {
        'log': Log,  # log(x, base)
        'logarithm': Logarithm,  # log(x, base)
    }

    @classmethod
    def build(cls, parser_tree: ast.Expression) -> MathObj:
        try:
            return cls._build(parser_tree.body)
        except NotImplementedError as e:
            raise e

    @classmethod
    def _build(cls, _node: ast.expr) -> MathObj:
        if isinstance(_node, ast.BinOp):
            left = cls._build(_node.left)
            right = cls._build(_node.right)
            name: str = _node.op.__class__.__name__
            return cls._operators_[name](left, right)
        elif isinstance(_node, ast.Num):
            return Constant(_node.n)
        elif isinstance(_node, ast.Name):
            return Variable(_node.id)
        elif isinstance(_node, ast.Call):
            # noinspection PyUnresolvedReferences
            name: str = _node.func.id.lower()
            arg = cls._build(_node.args[0])
            if name in cls._binary_functions_:
                # noinspection PyUnresolvedReferences
                _base = Constant(_node.args[1].n)
                return cls._functions_[name](arg, _base)
            else:
                return cls._functions_[name](arg)
        else:
            raise NotImplementedError(f'node={_node.__class__.__name__} is not implemented!')


def parser_expression(expression: str) -> MathObj:
    tree: ast.Expression = ast.parse(expression, mode='eval')
    builder = ExpressionBuilder()
    return builder.build(tree)
