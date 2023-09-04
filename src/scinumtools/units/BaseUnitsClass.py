import numpy as np
from dataclasses import dataclass, field, fields

from .FractionClass import Fraction
from .DimensionsClass import Dimensions
from .UnitList import UnitStandardTable, UnitPrefixesTable

@dataclass
class BaseUnits:

    baseunits: dict = field(default_factory=dict)
    symbol: str = ':'

    def __post_init__(self):
        self.unitlist = UnitStandardTable()
        self.prefixes = UnitPrefixesTable()
        for unit,exp in self.baseunits.items():
            if not isinstance(exp, Fraction):
                self.baseunits[unit] = Fraction(exp)
        # remove zero dimensions
        for unit in list(self.baseunits.keys()):
            if self.baseunits[unit].num==0:
                del self.baseunits[unit]

    def __str__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(self.symbol,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(self.symbol,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __add__(self, other):
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]+exp if unit in baseunits else exp
        return BaseUnits(baseunits)
    
    def __sub__(self, other):
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]-exp if unit in baseunits else -exp
        return BaseUnits(baseunits)

    def __mul__(self, other):
        baseunits = dict(self.baseunits)
        for unit,exp in self.baseunits.items():
            baseunits[unit] *= other
        return BaseUnits(baseunits)

    def __truediv__(self, div):
        baseunits = dict(self.baseunits)
        for unit,exp in self.baseunits.items():
            baseunits[unit] /= div
        return BaseUnits(baseunits)
    
    def base(self):
        magnitude = 1
        dimensions = Dimensions()
        for unitid,exp in self.baseunits.items():
            if ":" in unitid:
                prefix, base = unitid.split(":")
                magnitude  *= (self.prefixes[prefix].magnitude*self.unitlist[base].magnitude) ** (exp.num/exp.den)
            else:
                prefix, base = '', unitid
                magnitude  *= self.unitlist[base].magnitude ** (exp.num/exp.den)
            dimensions += Dimensions(*self.unitlist[base].dimensions)*exp
        return magnitude, dimensions
    
    def expression(self):
        units = []
        for unitid,exp in self.baseunits.items():
            symbol = unitid.replace(self.symbol,'')
            if exp.num==1 and exp.den==1:
                units.append(symbol)
            else:
                units.append(f"{symbol}{exp}")
        if units:
            return "*".join(units)
        else:
            return None
        
    def value(self):
        baseunits = {}
        for unit,exp in self.baseunits.items():
            baseunits[unit] = exp.value()
        return baseunits
