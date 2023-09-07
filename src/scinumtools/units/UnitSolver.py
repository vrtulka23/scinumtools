import re

from ..solver import ExpressionSolver, OperatorPar, OperatorMul, OperatorTruediv
from .FractionClass import Fraction
from .UnitList import UnitStandardTable, UnitPrefixesTable

class Atom:
    
    symbol: str = ':'
    
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
                unit = unit.replace(self.symbol,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"Atom({str(self.magnitude):s} {baseunits})"
            
    def __repr__(self):
        baseunits = []
        for unit,exp in self.baseunits.items():
            if exp.num not in [0, -0]:
                unit = unit.replace(self.symbol,"")
                baseunits.append(f"{unit}={str(exp)}")
        baseunits = " ".join(baseunits)
        return f"Atom({str(self.magnitude):s} {baseunits})"


def AtomParser(string=None):
    global unitlist, prefixes
    # parse number
    m = re.match(r'^[-]?([0-9.]+)(e([0-9+-]+)|)$', str(string))
    if m:
        magnitude = float(string)
        return Atom(magnitude, {})
    # parse unit
    string_bak = string
    string = ' '+string
    # parse exponent
    if m := re.search(r"[0-9"+Fraction.symbol+r"+-]+$", string):
        exp = m.group() 
        string = string[:-len(exp)]
        exp = Fraction(exp)
    else:
        exp = Fraction(1)
    # parse unit symbol
    bases = [u for u in unitlist.keys() if string.endswith(u)]
    if bases:
        base = max(bases, key=len)
        string = string[-len(base)-1]
        unitid = f"{base:s}"
    else:
        raise Exception('Unknown unit', string, string_bak)
    # parse unit prefix
    prefkeys = [p for p in prefixes.keys() if string.endswith(p)]
    if prefkeys:
        prefix = max(prefkeys, key=len)
        if isinstance(unitlist[base].prefixes,list) and prefix not in unitlist[base].prefixes:
            raise Exception(f"Unit can have only following prefixes:", unitlist[base].prefixes, prefix)
        elif unitlist[base].prefixes is True and prefix not in prefixes.keys():
            raise Exception(f"Unknown unit prefix:", string_bak)
        elif unitlist[base].prefixes is False:
            raise Exception(f"Unit cannot have any prefixes:", base)
        unitid = f"{prefix:s}{Atom.symbol}{unitid}"
    elif len(string)>1:
        raise Exception("Unknown unit prefix:", string)
    # return quantity
    return Atom(1.0, {unitid: exp})
        
def UnitSolver(expression):
    global unitlist, prefixes
    unitlist = UnitStandardTable()
    prefixes = UnitPrefixesTable()
    with ExpressionSolver(AtomParser, [OperatorPar,OperatorMul,OperatorTruediv]) as es:
        return es.solve(expression)