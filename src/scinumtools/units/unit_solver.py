import re

from .settings import *
from ..solver import ExpressionSolver, OperatorPar, OperatorMul, OperatorTruediv
from .fraction import Fraction

class Atom:
    
    magnitude: float
    baseunits: dict
    
    def __init__(self, magnitude, baseunits):
        self.magnitude = magnitude
        self.baseunits = baseunits

    def __mul__(self, other):
        magnitude = self.magnitude * other.magnitude
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]+exp if unit in baseunits else exp
        return Atom(magnitude, baseunits)
    
    def __truediv__(self, other):
        magnitude = self.magnitude / other.magnitude
        baseunits = dict(self.baseunits)
        for unit,exp in other.baseunits.items():
            baseunits[unit] = baseunits[unit]-exp if unit in baseunits else -exp
        return Atom(magnitude, baseunits)
        
    def __str__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(SYMBOL_UNITID,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        if baseunits:
            return f"Atom({self.magnitude:.3e} {baseunits})"
        else:
            return f"Atom({self.magnitude:.3e})"
            
    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(SYMBOL_UNITID,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        if baseunits:
            return f"Atom({self.magnitude:.3e} {baseunits})"
        else:
            return f"Atom({self.magnitude:.3e})"

def AtomParser(string=None):
    # parse number
    if m := re.match(r'^[-]?([0-9.]+)(e([0-9+-]+)|)$', str(string)):
        magnitude = float(string)
        return Atom(magnitude, {})
    # parse unit
    string_bak = string
    string = ' '+string
    # parse exponent
    if m := re.search(r"[0-9"+SYMBOL_FRACTION+r"+-]+$", string):
        exp = m.group() 
        string = string[:-len(exp)]
        exp = Fraction.from_string(exp)
    else:
        exp = Fraction(1)
    if string.startswith(f" {SYMBOL_SYSTEM_UNIT}"):
        unitid = string[1:]
        return Atom(1.0, {unitid: exp})
    # parse unit symbol
    bases = [u for u in UNIT_STANDARD.keys() if string.endswith(u)]
    if bases:
        base = max(bases, key=len)
        string = string[-len(base)-1]
        unitid = f"{base:s}"
    else:
        raise Exception('Unknown unit', string, string_bak)
    # parse unit prefix
    prefkeys = [p for p in UNIT_PREFIXES.keys() if string.endswith(p)]
    if prefkeys:
        prefix = max(prefkeys, key=len)
        if isinstance(UNIT_STANDARD[base].prefixes,list) and prefix not in UNIT_STANDARD[base].prefixes:
            raise Exception(f"Unit can have only following prefixes:", UNIT_STANDARD[base].prefixes, prefix)
        elif UNIT_STANDARD[base].prefixes is True and prefix not in UNIT_PREFIXES.keys():
            raise Exception(f"Unknown unit prefix:", string_bak)
        elif UNIT_STANDARD[base].prefixes is False:
            raise Exception(f"Unit cannot have any prefixes:", base)
        unitid = f"{prefix:s}{SYMBOL_UNITID}{unitid}"
    elif len(string)>1:
        raise Exception("Unknown unit prefix:", string)
    # return quantity
    return Atom(1.0, {unitid: exp})
        
def UnitSolver(expression):
    operators = {'par':OperatorPar,'mul':OperatorMul,'truediv':OperatorTruediv}
    with ExpressionSolver(AtomParser, operators) as es:
        return es.solve(expression)