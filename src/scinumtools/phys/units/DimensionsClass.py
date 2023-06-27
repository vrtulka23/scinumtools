import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union

@dataclass
class Ratio:
    
    numerator: Union[int, tuple]
    denominator: int = field(default=1)

    def __post_init__(self):
        # initialize from a tuple
        if isinstance(self.numerator, tuple):
            value = self.numerator
            self.numerator = value[0]
            self.denominator = value[1]
        # enforce whole numbers
        if self.numerator%1!=0 or self.denominator%1!=0:
            raise Exception("Ratio excepts only whole numbers:", self.numerator, self.denominator)
        else:
            self.numerator = int(self.numerator)
            self.denominator = int(self.denominator)
        # reset zero values
        if self.numerator in [0, -0]:
            self.numerator = 0
            self.denominator = 1
        # keep minus sign always on the top
        if self.numerator>=0 and self.denominator<0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        elif self.numerator<0 and self.denominator<0:
            self.numerator = -self.numerator
            self.denominator = -self.denominator
        # remove common divisors
        def reduce(numerator: int, denominator:int):
            gcd=np.gcd(numerator, denominator)
            if gcd>1:
                return reduce(int(numerator/gcd), int(denominator/gcd))
            return int(numerator), int(denominator)
        self.numerator, self.denominator = reduce(self.numerator, self.denominator)
    
    def __str__(self):
        if self.numerator==0 or self.denominator==1:
            return str(self.numerator)
        else:
            return f"Ratio({self.numerator},{self.denominator})"

    def __repr__(self):
        if self.numerator==0 or self.denominator==1:
            return str(self.numerator)
        else:
            return f"Ratio({self.numerator},{self.denominator})"

    def __add__(self, other):
        return Ratio(
            self.numerator*other.denominator+other.numerator*self.denominator,
            self.denominator*other.denominator,
        )
            
    def __sub__(self, other):
        return Ratio(
            self.numerator*other.denominator-other.numerator*self.denominator,
            self.denominator*other.denominator,
        )

    def __mul__(self, power):
        return Ratio(
            self.numerator*power,
            self.denominator
        )
    
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
            if value.numerator not in [0, -0]:
                dimensions.append(f"{f.name}={str(value)}")
        dimensions = ", ".join(dimensions)
        return f"Dimensions({dimensions})"

    def __repr__(self):
        dimensions = []
        for f in fields(self):
            value = getattr(self, f.name)
            if value.numerator not in [0, -0]:
                dimensions.append(f"{f.name}={str(value)}")
        dimensions = ", ".join(dimensions)
        return f"Dimensions({dimensions})"
        
    def __add__(self, other):
        dimensions = {}
        for f in fields(self):
            if getattr(self, f.name) != getattr(other, f.name):
                raise Exception('Dimension does not match:', f.name, getattr(self, f.name), getattr(other, f.name))
        return self
            
    def __sub__(self, other):
        dimensions = {}
        for f in fields(self):
            if getattr(self, f.name) != getattr(other, f.name):
                raise Exception('Dimension does not match:', f.name, getattr(self, f.name), getattr(other, f.name))
        return self

    def __mul__(self, other):
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) + getattr(other, f.name)
        return Dimensions(**dimensions)
            
    def __truediv__(self, other):
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) - getattr(other, f.name)
        return Dimensions(**dimensions)

    def __pow__(self, power):
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) * power
        return Dimensions(**dimensions)

    def __eq__(self, other):
        for f in fields(self):
            if not getattr(self, f.name) == getattr(other, f.name):
                return False
        return True
    
@dataclass
class BaseUnits:
    pass
