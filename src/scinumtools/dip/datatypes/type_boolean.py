from typing import Union, List
import numpy as np

from .type import Type

class BooleanType(Type):
    value: Union[bool,list]
    dtype = bool

    def __str__(self):
        return f"BooleanType({self.value})"
    
    def __repr__(self):
        return f"BooleanType({self.value})"
        
    def __init__(self, value, **kwargs):
        if isinstance(value, BooleanType):
            kwargs['value'] = value.value
        else:
            kwargs['value'] = value
        if isinstance(kwargs['value'], np.ndarray):
            kwargs['value'] = kwargs['value'].tolist()
        super().__init__(**kwargs)

    def __eq__(self, other):
        if isinstance(other, bool):
            return self.value == other
        else:
            return self.value == other.value
        
    def logical_and(self, other):
        return BooleanType(self.value and other.value)
        
    def logical_or(self, other):
        return BooleanType(self.value or other.value)
        
    def logical_not(self):
        return BooleanType(not self.value)
        