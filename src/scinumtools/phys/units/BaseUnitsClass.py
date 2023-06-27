import numpy as np
from dataclasses import dataclass, field, fields
from .RatioClass import Ratio

@dataclass
class BaseUnits:

    baseunits: dict = field(default_factory=dict)

    def __post_init__(self):
        for unit,exp in self.baseunits.items():
            if not isinstance(exp, Ratio):
                self.baseunits[unit] = Ratio(exp)
        # remove zero dimensions
        for unit in list(self.baseunits.keys()):
            if self.baseunits[unit].num==0:
                del self.baseunits[unit]

    def __str__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(":","")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(":","")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"BaseUnits({baseunits})"

    def __mul__(self, other):
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]+exp if unit in baseunits else exp
        return BaseUnits(baseunits)
    
    def __truediv__(self, other):
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]-exp if unit in baseunits else -exp
        return BaseUnits(baseunits)

    def __pow__(self, power):
        baseunits = dict(self.baseunits)
        for unit,exp in self.baseunits.items():
            baseunits[unit] *= power
        return BaseUnits(baseunits)

    def expression(self):
        units = []
        for unit,exp in self.baseunits.items():
            symbol = unit.replace(':','')
            if exp.num==1 and exp.den==1:
                units.append(symbol)
            else:
                units.append(f"{symbol}{exp}")
        return "*".join(units)
    
    def value(self):
        baseunits = {}
        for unit,exp in self.baseunits.items():
            baseunits[unit] = exp.value()
        return baseunits
