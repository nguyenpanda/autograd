import math
from abc import ABC, abstractmethod
from typing import Type, Optional

from .base import Transcendental
from ..core import *
from ..core.node import number, Node


class Trigo(Transcendental, ABC):

    @abstractmethod
    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        pass


class Sin(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        return Node(
            math.sin(_node.v),
            _node.p * math.cos(_node.v),
        )


class Cos(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        return Node(
            math.cos(_node.v),
            - _node.p * math.sin(_node.v),
        )


class Tan(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        sec2 = 1 / math.cos(_node.v) ** 2
        return Node(
            math.tan(_node.v),
            _node.p * sec2
        )


class Cot(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        csc2 = 1 / math.sin(_node.v) ** 2
        return Node(
            1 / math.tan(_node.v),
            -_node.p * csc2
        )


class Csc(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        csc = 1 / math.sin(_node.v)
        cot = 1 / math.tan(_node.v)
        return Node(
            csc,
            -_node.p * csc * cot
        )


class Sec(Trigo):

    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        _node = self.value.evaluate_and_derive(var, **kwargs)
        sec = 1 / math.cos(_node.v)
        tan = math.tan(_node.v)
        return Node(
            sec,
            _node.p * sec * tan
        )


all_classes: dict[str, Type[Trigo]] = {
    'Trigo': Trigo,
    'Sin': Sin,
    'Cos': Cos,
    'Tan': Tan,
}
