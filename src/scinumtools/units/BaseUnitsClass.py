import numpy as np
from dataclasses import dataclass, field, fields

from .FractionClass import Fraction
from .DimensionsClass import Dimensions
from .UnitList import UnitStandardTable, UnitPrefixesTable

@dataclass
class Base:
    
    magnitude: float
    dimensions: Dimensions

@dataclass
class BaseUnits:

    baseunits: dict = field(default_factory=dict)
    symbol: str = ':'

    def __post_init__(self):
        self.unitlist = UnitStandardTable()
        self.prefixes = UnitPrefixesTable()
        # convert units exponents to fractions
        for unit,exp in self.baseunits.items():
            if not isinstance(exp, Fraction):
                self.baseunits[unit] = Fraction(exp)
        # remove units with zero exponents
        for unit in list(self.baseunits.keys()):
            if self.baseunits[unit].num==0:
                del self.baseunits[unit]
        # remove units with nonzero dimensions if total dimension is zero
        base = self.base()
        if base.dimensions == Dimensions():
            zerodim = Dimensions().value()
            for unitid in list(self.baseunits.keys()):
                symbol = unitid.split(":")[-1] if ":" in unitid else unitid
                if self.unitlist[symbol].dimensions != zerodim:
                    del self.baseunits[unitid]

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
    
    def base(self, unitid=None):
        def unit_base(unitid):
            exp = self.baseunits[unitid]
            if ":" in unitid:
                prefix, base = unitid.split(":")
                magnitude  = (self.prefixes[prefix].magnitude*self.unitlist[base].magnitude) ** exp.value(dtype=float)
            else:
                prefix, base = '', unitid
                magnitude  = self.unitlist[base].magnitude ** exp.value(dtype=float)
            dimensions = Dimensions(*self.unitlist[base].dimensions)*exp
            return magnitude, dimensions
        if unitid:
            magnitude, dimensions = unit_base(unitid)
        else:
            magnitude = 1
            dimensions = Dimensions()
            for unitid in self.baseunits.keys():
                mag, dim = unit_base(unitid)
                magnitude *= mag
                dimensions += dim
        return Base(magnitude, dimensions)
    
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
