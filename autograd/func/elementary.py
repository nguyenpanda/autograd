import math
from typing import Optional

from ..core import Variable
from ..core.node import Node, number
from .base import Function


class Exp(Function):
    
    def evaluate_and_derive(self, var: Optional[Variable] = None, **kwargs: number) -> Node:
        node = self.value.evaluate_and_derive(var, **kwargs)
        value = math.exp(node.v)
        return Node(
            value, 
            value * node.p 
            if var is not None 
            else math.inf
        )


class Sqrt(Function):
    
    def evaluate_and_derive(self, var: Optional[Variable] = None, **kwargs: number) -> Node:
        node = self.value.evaluate_and_derive(var, **kwargs)
        value = math.sqrt(node.v)
        if var is None:
            return Node(value, math.inf)
        if value == 0:
            raise ValueError('Sqrt is not differentiable at zero')
        return Node(
            value, 
            node.p / (2 * value)
        )


all_classes = {"Exp": Exp, "Sqrt": Sqrt}
