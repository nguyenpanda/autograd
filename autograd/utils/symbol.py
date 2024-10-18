from typing import Union

from ..core import Variable


def symbol(string: str, split: str = ',') -> Union[Variable, tuple[Variable, ...]]:
    names = string.split(split)
    return tuple(Variable(n) for n in names) if len(names) != 1 else Variable(names[0])
