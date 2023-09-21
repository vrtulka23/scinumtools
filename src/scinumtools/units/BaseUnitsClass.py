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
    units: str
    expression: str

def get_unit_base(unitid: str, exp: Fraction = None):
    if exp is None:
        exp = Fraction(1)
    if SYMBOL_UNITID in unitid:
        prefix, base = unitid.split(SYMBOL_UNITID)
        magnitude  = (UNIT_PREFIXES[prefix].magnitude*UNIT_STANDARD[base].magnitude) ** exp.value(dtype=float)
    else:
        prefix, base = '', unitid
        magnitude  = UNIT_STANDARD[base].magnitude ** exp.value(dtype=float)
    dimensions = Dimensions(*UNIT_STANDARD[base].dimensions)*exp
    if exp.num==1 and exp.den==1:
        expression = f"{prefix}{base}"
    else:
        expression = f"{prefix}{base}{exp}"
    return Base(magnitude, dimensions, base, expression)

class BaseUnits:

    baseunits: dict
    magnitude: float
    dimensions: Dimensions
    units: Union[str,list]
    expression: Union[str,list]

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
        # calculate total base
        self.magnitude = 1
        self.dimensions = Dimensions()
        self.units = []
        self.expression = []
        for unitid in list(self.baseunits.keys()):
            if not isinstance(self.baseunits[unitid], Fraction):
                self.baseunits[unitid] = Fraction(self.baseunits[unitid])
            if self.baseunits[unitid].num==0:
                del self.baseunits[unitid]
                continue
            ubase = get_unit_base(unitid, self.baseunits[unitid])
            self.magnitude *= ubase.magnitude
            self.dimensions += ubase.dimensions
            self.units.append(ubase.units)
            self.expression.append(ubase.expression)
        self.expression = SYMBOL_MULTIPLY.join(self.expression) if self.expression else None

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
    
    def value(self):
        """ Return base units as a plain dictionary
        """
        baseunits = {}
        for unitid,exp in self.baseunits.items():
            baseunits[unitid] = exp.value()
        return baseunits
