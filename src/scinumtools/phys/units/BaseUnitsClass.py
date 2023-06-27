import numpy as np
from dataclasses import dataclass, field, fields
from .RatioClass import Ratio

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
