import math
from abc import ABC, abstractmethod
from typing import Union, Optional, Type

from .node import Node, number


class MathObj(ABC):

    @abstractmethod
    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        pass

    def diff(self, var: 'Variable', **kwargs: number) -> number:
        return self.evaluate_and_derive(var, **kwargs).p

    def eval(self, **kwargs: number) -> number:
        return self.evaluate_and_derive(None, **kwargs).v

    def __call__(self, *args, **kwargs):
        return self.eval(**kwargs)

    def __add__(self, other: Union['MathObj', number]) -> 'Plus':
        if isinstance(other, number):
            other = Constant(other)
        return Plus(self, other)

    def __sub__(self, other: Union['MathObj', number]) -> 'Minus':
        if isinstance(other, number):
            other = Constant(other)
        return Minus(self, other)

    def __mul__(self, other: Union['MathObj', number]) -> 'Multiply':
        if isinstance(other, number):
            other = Constant(other)
        return Multiply(self, other)

    def __truediv__(self, other: Union['MathObj', number]) -> 'Divide':
        if isinstance(other, number):
            other = Constant(other)
        return Divide(self, other)

    def __pow__(self, other: Union['MathObj', number]) -> 'Power':
        if isinstance(other, number):
            other = Constant(other)
        return Power(self, other)

    def __xor__(self, other: Union['MathObj', number]) -> 'Power':
        return self.__pow__(other)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__
    __rpow__ = __pow__

    def __str__(self) -> str:
        return self.__class__.__name__


class Operand(MathObj, ABC):

    def __init__(self, value: number):
        assert isinstance(value, Optional[number]), ValueError(f'{value.__class__.__name__}')
        self._value: number = value

    @property
    def value(self) -> number:
        return self._value

    def __str__(self) -> str:
        return str(self.value)


class Constant(Operand):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        return Node(
            self.value,
            0.0,
        )


class Variable(Operand):

    def __init__(self, name: str, value: Optional[number] = None):
        super().__init__(value)
        self._name: str = name

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        variables: dict[str, Variable] = {
            k: Variable(str(k), v) for k, v in kwargs.items()
        }
        kw_var: Variable = variables.get(self.name)
        if kw_var is self.value is None:
            raise ValueError(f'Value of {self} must be predefined!')

        return Node(
            kw_var.value if kw_var else self.value,
            (1.0 if self == var else 0.0) if var else math.inf,
        )

    def __eq__(self, other: Optional['Variable']) -> bool:
        if other is None:
            return False
        return self.name == other.name

    @property
    def name(self) -> str:
        return self._name

    def __str__(self) -> str:
        return self.name


class Operator(MathObj, ABC):

    def __init__(self, lhs: MathObj, rhs: MathObj):
        self._lhs: MathObj = lhs
        self._rhs: MathObj = rhs

    def _return_lhs_rhs_node(self, var: Variable, **kwargs: number) -> tuple[Node, Node]:
        lhs_node: Node = self.lhs.evaluate_and_derive(var, **kwargs)
        rhs_node: Node = self.rhs.evaluate_and_derive(var, **kwargs)
        return lhs_node, rhs_node

    @property
    def lhs(self) -> MathObj:
        return self._lhs

    @property
    def rhs(self) -> MathObj:
        return self._rhs

    def __str__(self) -> str:
        left = self.lhs.__class__.__name__
        obj = self.__class__.__name__
        right = self.rhs.__class__.__name__
        return f'({left})[{obj}]({right})'


class Plus(Operator):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        l, r = self._return_lhs_rhs_node(var, **kwargs)
        return Node(
            l.v + r.v,
            l.p + r.p,
        )


class Minus(Operator):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        l, r = self._return_lhs_rhs_node(var, **kwargs)
        return Node(
            l.v - r.v,
            l.p - r.p,
        )


class Multiply(Operator):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        l, r = self._return_lhs_rhs_node(var, **kwargs)
        return Node(
            l.v * r.v,
            l.p * r.v + l.v * r.p,
        )


class Divide(Operator):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        l, r = self._return_lhs_rhs_node(var, **kwargs)
        try:
            return Node(
                l.v / r.v,
                (l.p * r.v - l.v * r.p) / r.v ** 2,
            )
        except ZeroDivisionError as e:
            raise ValueError() from e


class Power(Operator):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        l, r = self._return_lhs_rhs_node(var, **kwargs)
        if l.v < 0:
            raise ValueError(f'[{l}] ^ [{r}] = {l.v} ^ {r.v} is not valid')

        power: number = l.v ** r.v
        return Node(
            power,
            power * (l.p * r.v / l.v + math.log(l.v) * r.p),
        )


all_operands: dict[str, Type[Operand]] = {
    'Operand': Operand,
    'Constant': Operand,
    'Variable': Operand,
}

all_operators: dict[str, Type[Operator]] = {
    'Operator': Operator,
    'Plus': Plus,
    'Minus': Minus,
    'Multiply': Multiply,
    'Divide': Divide,
    'Power': Power,
}

all_classes: dict[str, Type[MathObj]] = {
    'MathObj': MathObj,
    **all_operands,
    **all_operators,
}
