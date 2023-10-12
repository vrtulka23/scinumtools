from typing import Union, List
import numpy as np

from .type_number import NumberType
from .type_boolean import BooleanType

class FloatType(NumberType):
    value: Union[float,list]
    precision: int = 64
    dtype = float
        
    def __str__(self):
        if self.unit:
            return f"FloatType({self.value} {self.unit})"
        else:
            return f"FloatType({self.value})"
            
    def __repr__(self):
        if self.unit:
            return f"FloatType({self.value} {self.unit})"
        else:
            return f"FloatType({self.value})"
            
    def __init__(self, value, unit=None, **kwargs):
        if isinstance(value, FloatType):
            kwargs['value'] = value.value
            kwargs['unit'] = value.unit
        else:
            kwargs['value'] = value
            kwargs['unit'] = unit
        if isinstance(kwargs['value'], np.ndarray):
            kwargs['value'] = kwargs['value'].tolist()
        if 'precision' in kwargs:
            self.precision = int(kwargs['precision'])
            del kwargs['precision']
        super().__init__(**kwargs)
