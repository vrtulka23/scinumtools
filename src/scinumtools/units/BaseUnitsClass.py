import numpy as np
from dataclasses import dataclass, field, fields
from typing import Union

from .settings import *
from .FractionClass import Fraction
from .DimensionsClass import Dimensions
from .UnitSolver import UnitSolver

@dataclass
class Base:
    
    magnitude: float
    dimensions: Dimensions

class BaseUnits:

    baseunits: dict

    def __init__(self, baseunits: Union[str,list,dict,Dimensions]=None):
        if baseunits is None:
            self.baseunits = {}
        elif isinstance(baseunits, dict):
            self.baseunits = baseunits
        elif isinstance(baseunits, Dimensions):
            self.baseunits = baseunits.value(dtype=dict)
        elif isinstance(baseunits, (list, np.ndarray)):
            self.baseunits = Dimensions(*baseunits).value(dtype=dict)
        elif isinstance(baseunits, BaseUnits):
            self.baseunits = baseunits.baseunits
        elif isinstance(baseunits, str):
            self.baseunits = UnitSolver(baseunits).baseunits
        else:
            raise Exception("Cannot initialize BaseUnits with given argument:", baseunits)
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
                symbol = unitid.split(SYMBOL_UNITID)[-1] if SYMBOL_UNITID in unitid else unitid
                if UNIT_STANDARD[symbol].dimensions != zerodim:
                    del self.baseunits[unitid]

    def __str__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(SYMBOL_UNITID,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(SYMBOL_UNITID,"")
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
    
    def __eq__(self, other):
        if len(self.baseunits) != len(other.baseunits):
            return False
        for unit,exp in self.baseunits.items():
            if unit not in other.baseunits:
                return False
            elif not other.baseunits[unit] == exp:
                return False
        return True
    
    def base(self, unitid=None):
        def unit_base(unitid):
            exp = self.baseunits[unitid]
            if SYMBOL_UNITID in unitid:
                prefix, base = unitid.split(SYMBOL_UNITID)
                magnitude  = (UNIT_PREFIXES[prefix].magnitude*UNIT_STANDARD[base].magnitude) ** exp.value(dtype=float)
            else:
                prefix, base = '', unitid
                magnitude  = UNIT_STANDARD[base].magnitude ** exp.value(dtype=float)
            dimensions = Dimensions(*UNIT_STANDARD[base].dimensions)*exp
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
            symbol = unitid.replace(SYMBOL_UNITID,'')
            if exp.num==1 and exp.den==1:
                units.append(symbol)
            else:
                units.append(f"{symbol}{exp}")
        if units:
            return SYMBOL_MULTIPLY.join(units)
        else:
            return None
        
    def value(self):
        baseunits = {}
        for unit,exp in self.baseunits.items():
            baseunits[unit] = exp.value()
        return baseunits
