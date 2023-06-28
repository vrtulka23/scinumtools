import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union
from .RatioClass import Ratio
    
@dataclass
class Dimensions:
    
    m: Union[int,Ratio] = field(default=0)
    g: Union[int,Ratio] = field(default=0)
    s: Union[int,Ratio] = field(default=0)
    K: Union[int,Ratio] = field(default=0)
    C: Union[int,Ratio] = field(default=0)
    cd: Union[int,Ratio] = field(default=0)
    mol: Union[int,Ratio] = field(default=0)
    rad: Union[int,Ratio] = field(default=0)
    
    def __post_init__(self):
        for f in fields(self):
            value = getattr(self, f.name)
            if not isinstance(value, Ratio):
                setattr(self, f.name, Ratio(value))

    def __str__(self):
        dimensions = []
        for f in fields(self):
            value = getattr(self, f.name)
            if value.num not in [0, -0]:
                dimensions.append(f"{f.name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"

    def __repr__(self):
        dimensions = []
        for f in fields(self):
            value = getattr(self, f.name)
            if value.num not in [0, -0]:
                dimensions.append(f"{f.name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"
                            
    def __add__(self, other):
        dimensions = {}
        for f in fields(self):
            if isinstance(other, Dimensions):
                dimensions[f.name] = getattr(self, f.name) + getattr(other, f.name)
            else:
                dimensions[f.name] = getattr(self, f.name) + other
        return Dimensions(**dimensions)
            
    def __sub__(self, other):
        dimensions = {}
        for f in fields(self):
            if isinstance(other, Dimensions):
                dimensions[f.name] = getattr(self, f.name) - getattr(other, f.name)
            else:
                dimensions[f.name] = getattr(self, f.name) - other
        return Dimensions(**dimensions)

    def __mul__(self, power):
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) * power
        return Dimensions(**dimensions)

    def __truediv__(self, div):
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) / div
        return Dimensions(**dimensions)
    
    def __eq__(self, other):
        for f in fields(self):
            if not getattr(self, f.name) == getattr(other, f.name):
                return False
        return True

    def __neg__(self):
        """ Inverse dimensions
        """
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) * -1
        return Dimensions(**dimensions)

    def value(self, dtype=list):
        if dtype==list:
            dimensions = []
            for f in fields(self):
                dimensions.append( getattr(self, f.name).value() )
        elif dtype==dict:
            dimensions = {}
            for f in fields(self):
                ratio = getattr(self, f.name)
                if ratio.num not in [0, -0]:
                    dimensions[f.name] = ratio.value()
        return dimensions
