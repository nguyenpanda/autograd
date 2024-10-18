from abc import ABC, abstractmethod
from typing import Optional

from ..core import *
from ..core.node import Node, number


class Function(MathObj, ABC):

    def __init__(self, value: MathObj):
        self._value = value

    @abstractmethod
    def evaluate_and_derive(self, var: Optional['Variable'] = None, **kwargs: number) -> Node:
        pass

    @property
    def value(self) -> MathObj:
        return self._value

    def __str__(self) -> str:
        return self.__class__.__name__ + f'({self.value.__class__.__name__})'


class Transcendental(Function, ABC):
    pass
