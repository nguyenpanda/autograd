from typing import Union

number = Union[int, float]


class Node:

    def __init__(self, value: number, partial: number):
        assert isinstance(value, number), TypeError(f'Value must be of type int or float, got {value.__class__.__name__}')
        assert isinstance(partial, number), TypeError(f'Partial must be of type int or float, got {partial.__class__.__name__}')
        self._v: number = value
        self._p: number = partial

    @property
    def v(self) -> number:
        return self._v

    @property
    def p(self) -> number:
        return self._p

    def __str__(self) -> str:
        return self.__class__.__name__ + f'(v={self.v}, p={self.p})'
