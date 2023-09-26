import numpy as np
from dataclasses import dataclass, field #, fields
from typing import Union

from .fraction import Fraction
    
@dataclass
class Dimensions:
    
    m: Union[int,Fraction] = field(default=0)
    g: Union[int,Fraction] = field(default=0)
    s: Union[int,Fraction] = field(default=0)
    K: Union[int,Fraction] = field(default=0)
    C: Union[int,Fraction] = field(default=0)
    cd: Union[int,Fraction] = field(default=0)
    mol: Union[int,Fraction] = field(default=0)
    rad: Union[int,Fraction] = field(default=0)
    _fields: list = field(default_factory=list)
    nodim: bool = field(default=True)
    
    def __post_init__(self):
        self._fields = ['m','g','s','K','C','cd','mol','rad']
        for name in self._fields:
            value = getattr(self, name)
            if not isinstance(value, Fraction):
                setattr(self, name, Fraction(value))
            if getattr(self, name).num!=0:
                self.nodim = False

    def __str__(self):
        dimensions = []
        for name in self._fields:
            value = getattr(self, name)
            if value.num not in [0, -0]:
                dimensions.append(f"{name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"

    def __repr__(self):
        dimensions = []
        for name in self._fields:
            value = getattr(self, name)
            if value.num not in [0, -0]:
                dimensions.append(f"{name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"
                            
    def __add__(self, other):
        dimensions = {}
        for name in self._fields:
            if isinstance(other, Dimensions):
                dimensions[name] = getattr(self, name) + getattr(other, name)
            else:
                dimensions[name] = getattr(self, name) + other
        return Dimensions(**dimensions)
            
    def __sub__(self, other):
        dimensions = {}
        for name in self._fields:
            if isinstance(other, Dimensions):
                dimensions[name] = getattr(self, name) - getattr(other, name)
            else:
                dimensions[name] = getattr(self, name) - other
        return Dimensions(**dimensions)

    def __mul__(self, other):
        dimensions = {}
        for name in self._fields:
            dimensions[name] = getattr(self, name) * other
        return Dimensions(**dimensions)

    def __truediv__(self, other):
        dimensions = {}
        for name in self._fields:
            dimensions[name] = getattr(self, name) / other
        return Dimensions(**dimensions)
    
    def __eq__(self, other):
        for name in self._fields:
            if not getattr(self, name) == getattr(other, name):
                return False
        return True

    def __neg__(self):
        """ Inverse dimensions
        """
        dimensions = {}
        for name in self._fields:
            dimensions[name] = getattr(self, name) * -1
        return Dimensions(**dimensions)

    def value(self, dtype=list):
        if dtype==list:
            dimensions = []
            for name in self._fields:
                dimensions.append( getattr(self, name).value() )
        elif dtype==dict:
            dimensions = {}
            for name in self._fields:
                fraction = getattr(self, name)
                if fraction.num not in [0, -0]:
                    dimensions[name] = fraction.value()
        elif dtype==tuple:
            dimensions = []
            for name in self._fields:
                fraction = getattr(self, name)
                if fraction.num not in [0, -0]:
                    dimensions.append(name)
            dimensions = tuple(dimensions)
        return dimensions
        