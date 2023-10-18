import numpy as np
from dataclasses import dataclass, field #, fields
from typing import Union

from .fraction import Fraction
from .settings import DIMENSION_LIST
    
@dataclass
class Dimensions:
    
    m:   Fraction = field(default_factory=Fraction)
    g:   Fraction = field(default_factory=Fraction)
    s:   Fraction = field(default_factory=Fraction)
    K:   Fraction = field(default_factory=Fraction)
    C:   Fraction = field(default_factory=Fraction)
    cd:  Fraction = field(default_factory=Fraction)
    mol: Fraction = field(default_factory=Fraction)
    rad: Fraction = field(default_factory=Fraction)
    nodim: bool = field(default=True)
    
    @staticmethod
    def from_list(value: list):
        units = {}
        for n, name in enumerate(DIMENSION_LIST):
            if isinstance(value[n], tuple):
                units[name] = Fraction.from_tuple(value[n])
            else:
                units[name] = Fraction(value[n])
        return Dimensions(**units)
    
    def __post_init__(self):
        # are all dimensions zero?
        for name in DIMENSION_LIST:
            if getattr(self, name).num!=0:
                self.nodim = False

    def __str__(self):
        dimensions = []
        for name in DIMENSION_LIST:
            value = getattr(self, name)
            if value.num not in [0, -0]:
                dimensions.append(f"{name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"

    def __repr__(self):
        dimensions = []
        for name in DIMENSION_LIST:
            value = getattr(self, name)
            if value.num not in [0, -0]:
                dimensions.append(f"{name}={str(value)}")
        dimensions = " ".join(dimensions)
        return f"Dimensions({dimensions})"
                            
    def __add__(self, other):
        dimensions = {}
        for name in DIMENSION_LIST:
            if isinstance(other, Dimensions):
                dimensions[name] = getattr(self, name) + getattr(other, name)
            else:
                dimensions[name] = getattr(self, name) + other
        return Dimensions(**dimensions)
            
    def __sub__(self, other):
        dimensions = {}
        for name in DIMENSION_LIST:
            if isinstance(other, Dimensions):
                dimensions[name] = getattr(self, name) - getattr(other, name)
            else:
                dimensions[name] = getattr(self, name) - other
        return Dimensions(**dimensions)

    def __mul__(self, other):
        dimensions = {}
        for name in DIMENSION_LIST:
            dimensions[name] = getattr(self, name) * other
        return Dimensions(**dimensions)

    def __truediv__(self, other):
        dimensions = {}
        for name in DIMENSION_LIST:
            dimensions[name] = getattr(self, name) / other
        return Dimensions(**dimensions)
    
    def __eq__(self, other):
        for name in DIMENSION_LIST:
            if not getattr(self, name) == getattr(other, name):
                return False
        return True

    def __neg__(self):
        """ Inverse dimensions
        """
        dimensions = {}
        for name in DIMENSION_LIST:
            dimensions[name] = getattr(self, name) * -1
        return Dimensions(**dimensions)

    def value(self, dtype=list):
        if dtype==list:
            dimensions = []
            for name in DIMENSION_LIST:
                dimensions.append( getattr(self, name).value() )
        elif dtype==dict:
            dimensions = {}
            for name in DIMENSION_LIST:
                fraction = getattr(self, name)
                if fraction.num not in [0, -0]:
                    dimensions[name] = fraction.value()
        elif dtype==tuple:
            dimensions = []
            for name in DIMENSION_LIST:
                fraction = getattr(self, name)
                if fraction.num not in [0, -0]:
                    dimensions.append(name)
            dimensions = tuple(dimensions)
        return dimensions
        