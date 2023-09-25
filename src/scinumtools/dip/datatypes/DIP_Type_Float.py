from typing import Union, List
import numpy as np

from .DIP_Type_Number import NumberType

class FloatType(NumberType):
    value: Union[float,list]
    dtype = float
 
    def __str__(self):
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
        super().__init__(**kwargs)
