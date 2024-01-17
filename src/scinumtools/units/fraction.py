import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union
from math import isclose

from .settings import *

class Fraction:
    __slots__ = ("num","den")

    num: int    # numerator
    den: int    # denominator
    
    @staticmethod
    def from_string(value: str):
        if SYMBOL_FRACTION in value:
            num, den = value.split(SYMBOL_FRACTION)
            return Fraction(int(num), int(den))
        else:
            return Fraction(int(value), 1)

    @staticmethod
    def from_tuple(value: tuple):
        return Fraction(value[0],value[1])

    @staticmethod
    def from_fraction(value: 'Fraction'):
        return Fraction(value.num, value.den)

    def __init__(self, num: int = 0, den: int = 1):
        # ensure whole numbers
        self.num = int(num)
        self.den = int(den)

    def __eq__(self, other):
        return isclose(
            self.num*other.den, 
            other.num*self.den, 
            abs_tol=MAGNITUDE_PRECISION
        )

    def __str__(self):
        self.rebase()
        if self.num==0 or self.den==1:
            return str(self.num)
        else:
            return f"{self.num}{SYMBOL_FRACTION}{self.den}"

    def __repr__(self):
        self.rebase()
        if self.num==0 or self.den==1:
            return str(self.num)
        else:
            return f"{self.num}{SYMBOL_FRACTION}{self.den}"        
        
    def __add__(self, other):
        if isinstance(other, tuple):
            other = Fraction.from_tuple(other) 
        elif isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.num*other.den+other.num*self.den, self.den*other.den)
            
    def __sub__(self, other):
        if isinstance(other, tuple):
            other = Fraction.from_tuple(other) 
        elif isinstance(other, int):
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

    def rebase(self):
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
    
    def value(self, dtype=tuple):
        if self.num==0 or self.den==1:
            return self.num
        elif dtype==tuple:
            self.rebase()
            return (self.num,self.den)
        elif dtype==float:
            return self.num/self.den
