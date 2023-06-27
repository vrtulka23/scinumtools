import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union

@dataclass
class Ratio:
    
    num: Union[int, tuple]        # numerator
    den: int = field(default=1)   # denominator

    def __post_init__(self):
        # initialize from a tuple
        if isinstance(self.num, tuple):
            value = self.num
            self.num = value[0]
            self.den = value[1]
        # enforce whole numbers
        if np.mod(self.num,1)!=0 or np.mod(self.den,1)!=0:
            raise Exception("Ratio excepts only whole numbers:", self.num, self.den)
        else:
            self.num = int(self.num)
            self.den = int(self.den)
        # reset zero values
        if self.num in [0, -0]:
            self.num = 0
            self.den = 1
        # keep minus sign always on the top
        if self.num>=0 and self.den<0:
            self.num = -self.num
            self.den = -self.den
        elif self.num<0 and self.den<0:
            self.num = -self.num
            self.den = -self.den
        # remove common divisors
        def reduce(num: int, den:int):
            gcd=np.gcd(num, den)
            if gcd>1:
                return reduce(int(num/gcd), int(den/gcd))
            return int(num), int(den)
        self.num, self.den = reduce(self.num, self.den)
    
    def __str__(self):
        if self.num==0 or self.den==1:
            return str(self.num)
        else:
            return f"{self.num}/{self.den}"

    def __repr__(self):
        if self.num==0 or self.den==1:
            return str(self.num)
        else:
            return f"Ratio({self.num},{self.den})"        
        
    def __add__(self, other):
        return Ratio(
            self.num*other.den+other.num*self.den,
            self.den*other.den,
        )
            
    def __sub__(self, other):
        return Ratio(
            self.num*other.den-other.num*self.den,
            self.den*other.den,
        )

    def __mul__(self, power):
        return Ratio(
            self.num*power,
            self.den
        )

    def value(self):
        if self.num==0 or self.den==1:
            return self.num
        else:
            return (self.num,self.den)
    
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
        dimensions = ", ".join(dimensions)
        return f"Dimensions({dimensions})"

    def __repr__(self):
        dimensions = []
        for f in fields(self):
            value = getattr(self, f.name)
            if value.num not in [0, -0]:
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

    def __neg__(self):
        """ Inverse dimensions
        """
        dimensions = {}
        for f in fields(self):
            dimensions[f.name] = getattr(self, f.name) * -1
        return Dimensions(**dimensions)
    
    def value(self):
        dimensions = []
        for f in fields(self):
            dimensions.append( getattr(self, f.name).value() )
        return dimensions
    
@dataclass
class BaseUnits:

    baseunits: dict

    def __post_init__(self):
        for unit,exp in self.baseunits.items():
            if not isinstance(exp, Ratio):
                self.baseunits[unit] = Ratio(exp)

    def __str__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = ", ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = ", ".join(baseunits)
        return f"BaseUnits({baseunits})"
    
    def value(self):
        baseunits = {}
        for unit,exp in self.baseunits.items():
            baseunits[unit] = exp.value()
        return baseunits
