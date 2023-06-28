import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union

@dataclass
class Ratio:

    num: Union[int, tuple]        # numerator
    den: int = field(default=1)   # denominator
    symbol: str = ':'             # ratio symbol

    def __post_init__(self):
        # initialize from a tuple
        if isinstance(self.num, tuple):
            value = self.num
            self.num = value[0]
            self.den = value[1]
        elif isinstance(self.num, Ratio):
            value = self.num
            self.num = value.num
            self.den = value.den
        # ensure correct type
        if isinstance(self.num, (int,float)) and isinstance(self.den, (int,float)):
            self.num = int(self.num)
            self.den = int(self.den)
        else:
            raise Exception("Incorrect input values:", type(self.num), type(self.den))
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
            return f"{self.num}{self.symbol}{self.den}"

    def __repr__(self):
        if self.num==0 or self.den==1:
            return str(self.num)
        else:
            return f"Ratio({self.num},{self.den})"        
        
    def __add__(self, other):
        if not isinstance(other, Ratio):
            other = Ratio(other)
        return Ratio(
            self.num*other.den+other.num*self.den,
            self.den*other.den,
        )
            
    def __sub__(self, other):
        if not isinstance(other, Ratio):
            other = Ratio(other)
        return Ratio(
            self.num*other.den-other.num*self.den,
            self.den*other.den,
        )

    def __mul__(self, power):
        return Ratio(
            self.num*power,
            self.den
        )

    def __truediv__(self, div):
        return Ratio(
            self.num,
            self.den*div
        )
    
    def __neg__(self):
        return Ratio(
            -self.num,
            self.den
        )
    
    def value(self):
        if self.num==0 or self.den==1:
            return self.num
        else:
            return (self.num,self.den)
