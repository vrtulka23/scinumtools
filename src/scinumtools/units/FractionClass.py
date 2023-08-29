import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union

@dataclass
class Fraction:

    num: Union[int, tuple]        # numerator
    den: int = field(default=1)   # denominator
    symbol: str = ':'             # fraction symbol

    def __post_init__(self):
        # initialize from a tuple
        if isinstance(self.num, tuple):
            value = self.num
            self.num = value[0]
            self.den = value[1]
        elif isinstance(self.num, Fraction):
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
            raise Exception("Fraction excepts only whole numbers:", self.num, self.den)
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
            return f"Fraction({self.num},{self.den})"        
        
    def __add__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction(self.num*other.den+other.num*self.den, self.den*other.den)
            
    def __sub__(self, other):
        if not isinstance(other, Fraction):
            other = Fraction(other)
        return Fraction(self.num*other.den-other.num*self.den, self.den*other.den)

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num*other.num, self.den*other.den)
        elif isinstance(other, tuple):
            return Fraction(self.num*other[0], self.den*other[1])
        else:
            return Fraction(self.num*other, self.den)

    def __truediv__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num*other.den, self.den*other.num)
        elif isinstance(other, tuple):
            return Fraction(self.num*other[1], self.den*other[0])
        else:
            return Fraction(self.num, self.den*other)
    
    def __neg__(self):
        return Fraction(-self.num, self.den)
    
    def value(self):
        if self.num==0 or self.den==1:
            return self.num
        else:
            return (self.num,self.den)
