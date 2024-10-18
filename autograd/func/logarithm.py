import math
from typing import Type, Optional

from .base import Function
from ..core import *
from ..core.node import number, Node


class Logarithm(Function):

    def __init__(self, value: MathObj, base: Optional[number]):
        super().__init__(value=value)
        self._base: number = base if base else math.e

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        return Node(
            math.log(_node.v, self.base),
            _node.p / (math.log(self.base) * _node.v)
        )

    @property
    def base(self) -> number:
        return self._base

    def __str__(self) -> str:
        return self.__class__.__name__ + f'(x={self.value}, base={self.base})'


class Log(Logarithm):
    pass


class Ln(Logarithm):

    def __init__(self, value: MathObj):
        super().__init__(value=value, base=None)

    def __str__(self) -> str:
        return self.__class__.__name__ + f'(x={self.value})'


class Log2(Logarithm):

    def __init__(self, value: MathObj):
        super().__init__(value=value, base=2)


class Log10(Logarithm):

    def __init__(self, value: MathObj):
        super().__init__(value=value, base=10)


all_classes: dict[str, Type[Logarithm]] = {
    'Logarithm': Logarithm,
    'Log': Logarithm,
    'Ln': Ln,
    'Log2': Log2,
    'Log10': Log10,
}
