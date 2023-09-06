from typing import List
import numpy as np
import re
from typing import Union

from ..solver import ExpressionSolver, AtomBase, OperatorPar, OperatorMul, OperatorTruediv
from .UnitList import *
from .UnitConverters import *
from .DimensionsClass import Dimensions
from .BaseUnitsClass import BaseUnits
from .FractionClass import Fraction

HANDLED_FUNCTIONS = {}

class Quantity:
    prefixes: dict            # list of prefixes 
    unitlist: dict            # list of units
    
    magnitude: float          # quantity magnitude
    baseunits: BaseUnits      # base units

    precision: float = 1e-7

    def __init__(
            self, magnitude:float,
            baseunits: Union[str,list,np.ndarray,Dimensions,dict,BaseUnits] = None
    ):
        # Initialize settings
        self.unitlist = UnitStandardTable()
        self.prefixes = UnitPrefixesTable()
        # Set magnitude
        if isinstance(magnitude, (int,float)):
            self.magnitude = float(magnitude)
        elif isinstance(magnitude, list):
            self.magnitude = np.array(magnitude, dtype=float)
        elif isinstance(magnitude, np.ndarray):
            self.magnitude = magnitude.astype(float)
        else:
            raise Exception("Magnitude can be either a number or an list/array of numbers")
        # Set base units
        if baseunits is None:
            self.baseunits = BaseUnits()
        elif isinstance(baseunits, dict):
            self.baseunits = BaseUnits(baseunits)
        elif isinstance(baseunits, BaseUnits):
            self.baseunits = baseunits
        elif isinstance(baseunits, str):
            with ExpressionSolver(self._atom_parser, [OperatorPar,OperatorMul,OperatorTruediv]) as es:
                unit = es.solve(baseunits)
            self.magnitude *= unit.magnitude
            self.baseunits = unit.baseunits
        elif isinstance(baseunits, Quantity):
            self.magnitude *= baseunits.magnitude
            self.baseunits = baseunits.baseunits
        elif isinstance(baseunits, Dimensions):
            self.baseunits = BaseUnits(baseunits.value(dtype=dict))
        elif isinstance(baseunits, (list, np.ndarray)):
            self.baseunits = BaseUnits(Dimensions(*baseunits).value(dtype=dict))
        else:
            raise Exception("Insufficient quantity definition", magnitude, baseunits)

    def _add(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        left_dim = left.baseunits.base().dimensions
        right_dim = right.baseunits.base().dimensions
        if not left_dim == right_dim:
            raise Exception('Dimension does not match:', left_dim, right_dim)
        magnitude = left.magnitude + right.to(left.baseunits).magnitude 
        baseunits = left.baseunits
        return Quantity(magnitude, baseunits)

    def __add__(self, other):
        return self._add(self, other)
    
    def __radd__(self, other):
        return self._add(other, self)

    def _sub(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        left_dim = left.baseunits.base().dimensions
        right_dim = right.baseunits.base().dimensions
        if not left_dim == right_dim:
            raise Exception('Dimension does not match:', left_dim, right_dim)
        magnitude = left.magnitude - right.to(left.baseunits).magnitude
        baseunits = left.baseunits
        return Quantity(magnitude, baseunits)

    def __sub__(self, other):
        return self._sub(self, other)

    def __rsub__(self, other):
        return self._sub(other, self)
    
    def _mul(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        magnitude = left.magnitude * right.magnitude
        baseunits = left.baseunits + right.baseunits
        return Quantity(magnitude, baseunits)

    def __mul__(self, other):
        return self._mul(self, other)

    def __rmul__(self, other):
        return self._mul(other, self)
    
    def _truediv(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        magnitude = left.magnitude / right.magnitude
        baseunits = left.baseunits - right.baseunits
        return Quantity(magnitude, baseunits)

    def __truediv__(self, other):
        return self._truediv(self, other)
    
    def __rtruediv__(self, other):
        return self._truediv(other, self)
    
    def __pow__(self, power: Union[float,int,tuple,Fraction]):
        if isinstance(power, tuple):
            exp = power[0]/power[1]
        elif isinstance(power, Fraction):
            exp = power.value(dtype=float)
        else:
            exp = power
        magnitude = self.magnitude**exp
        baseunits = self.baseunits*power
        return Quantity(magnitude, baseunits)

    def __neg__(self):
        return Quantity(-self.magnitude, self.baseunits)
    
    def __eq__(self, other):
        if not np.allclose(self.magnitude, other.magnitude, rtol=self.precision):
            return False
        if not self.baseunits==other.baseunits:
            return False
        return True
    
    def __str__(self):
        magnitude = self.value()
        if isinstance(magnitude, np.ndarray):
            with np.printoptions(precision=3, suppress=False, threshold=5):
                magnitude = f"{str(magnitude):s}"
        else:
            magnitude = f"{magnitude:.03e}"
        baseunits = self.baseunits.expression()
        if baseunits:
            return f"Quantity({magnitude:s} {baseunits})"
        else:
            return f"Quantity({magnitude:s})"
            
    def __repr__(self):
        magnitude = self.value()
        if isinstance(magnitude, np.ndarray):
            with np.printoptions(precision=3, suppress=False, threshold=5):
                magnitude = f"{str(magnitude):s}"
        else:
            magnitude = f"{magnitude:.03e}"
        baseunits = self.baseunits.expression()
        if baseunits:
            return f"Quantity({magnitude:s} {baseunits})"
        else:
            return f"Quantity({magnitude:s})"

    def __getitem__(self, key):
        return Quantity(self.magnitude[key], self.baseunits)
        
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if ufunc==np.sqrt:
            return Quantity(ufunc(inputs[0].magnitude), inputs[0].baseunits/2)
        elif ufunc==np.cbrt:
            return Quantity(ufunc(inputs[0].magnitude), inputs[0].baseunits/3)
        elif ufunc==np.power:
            return Quantity(ufunc(inputs[0].magnitude,inputs[1]), inputs[0].baseunits*inputs[1])
        elif ufunc in [np.sin, np.cos, np.tan]:
            return Quantity(ufunc(inputs[0].to('rad').magnitude))
        elif ufunc in [np.arcsin, np.arccos, np.arctan]:
            return Quantity(ufunc(inputs[0].to(None).magnitude),'rad')
        else:
            return Quantity(ufunc(inputs[0].magnitude), inputs[0].baseunits)
    
    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            raise NotImplementedError()
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    def _atom_parser(self, string=None):
        # parse number
        m = re.match(r'^[-]?([0-9.]+)(e([0-9+-]+)|)$', str(string))
        if m:
            magnitude = float(string)
            return Quantity(magnitude)
        # parse unit
        string_bak = string
        string = ' '+string
        # parse exponent
        if m := re.search(r"[0-9"+Fraction.symbol+r"+-]+$", string):
            exp = m.group() 
            string = string[:-len(exp)]
            exp = Fraction(exp)
        else:
            exp = 1
        # parse unit symbol
        bases = [u for u in self.unitlist.keys() if string.endswith(u)]
        if bases:
            base = max(bases, key=len)
            string = string[-len(base)-1]
            unitid = f"{base:s}"
        else:
            raise Exception('Unknown unit', string, string_bak)
        # parse unit prefix
        prefixes = [p for p in self.prefixes.keys() if string.endswith(p)]
        if prefixes:
            prefix = max(prefixes, key=len)
            if isinstance(self.unitlist[base].prefixes,list) and prefix not in self.unitlist[base].prefixes:
                raise Exception(f"Unit can have only following prefixes:", self.unitlist[base].prefixes, prefix)
            elif self.unitlist[base].prefixes is True and prefix not in self.prefixes.keys():
                raise Exception(f"Unknown unit prefix:", string_bak)
            elif self.unitlist[base].prefixes is False:
                raise Exception(f"Unit cannot have any prefixes:", base)
            unitid = f"{prefix:s}{BaseUnits.symbol}{unitid}"
        elif len(string)>1:
            raise Exception("Unknown unit prefix:", string)
        # return quantity
        return Quantity(1.0, {unitid: exp})
    
    def value(self, expression=None, dtype=None):
        if expression:
            value = self.to(expression).value()
        else:
            value = self.magnitude
        if dtype:
            return value.astype(dtype) if isinstance(value, np.ndarray) else dtype(value)
        else:
            return value

    def units(self):
        return self.baseunits.expression()

    def to(self, units: Union[str,list,np.ndarray,Dimensions,dict,BaseUnits]):
        unit1 = self
        unit2 = Quantity(1,units)
        # Check if units can be directly converted
        base1 = unit1.baseunits.base()
        base2 = unit2.baseunits.base()
        if not base1.dimensions==base2.dimensions:
            # Check if inverted unit can be converted
            if -base1.dimensions==base2.dimensions:
                unit1 = 1/unit1
                base1 = unit1.baseunits.base()
            else:
                raise Exception("Converting units with different dimensions:",
                                base1.dimensions, base2.dimensions)
        if c := TemperatureConverter(unit1, unit2):
            unit2 = c.unit
        elif c := LogarithmicConverter(unit1, unit2):
            unit2 = c.unit
        else:
            unit2.magnitude = unit1.magnitude*base1.magnitude/base2.magnitude
        return unit2

    def rebase(self):
        factor = 1
        baseunits = {}
        for unitid1,exp1 in self.baseunits.baseunits.items():
            # find base units
            base1 = self.baseunits.base(unitid1)
            dim1 = str(base1.dimensions.value(dtype=tuple))
            if dim1 in baseunits:
                # exists: convert units
                base0 = self.baseunits.base(baseunits[dim1][0])
                factor *= (base1.magnitude/base0.magnitude)**exp1.value(dtype=float)
                baseunits[dim1][1] += exp1
            else:
                # does not exist: register new
                baseunits[dim1] = [unitid1,exp1] 
        # construct new base units
        self.magnitude *= factor
        self.baseunits = BaseUnits({unitid:exp for unitid,exp in baseunits.values()})
        return self

def implements(np_function):
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func
    return decorator

@implements(np.linspace)
def linspace(a, b, c, **kwargs):
    if isinstance(a,Quantity):
        b = b.to(a.baseunits) if isinstance(b,Quantity) else Quantity(b, a.baseunits)
    else:
        a = a.to(b.baseunits) if isinstance(a,Quantity) else Quantity(a, b.baseunits)
    return Quantity(np.linspace(a.value(), b.value(), c, **kwargs), a.baseunits)

@implements(np.logspace)
def logspace(a, b, c, **kwargs):
    if isinstance(a,Quantity):
        b = b.to(a.baseunits) if isinstance(b,Quantity) else Quantity(b, a.baseunits)
    else:
        a = a.to(b.baseunits) if isinstance(a,Quantity) else Quantity(a, b.baseunits)
    return Quantity(np.logspace(a.value(), b.value(), c, **kwargs), a.baseunits)

@implements(np.absolute)
def absolute(a, **kwargs):
    return Quantity(np.absolute(a.value()), a.baseunits)

@implements(np.abs)
def abs(a, **kwargs):
    return Quantity(np.abs(a.value()), a.baseunits)

@implements(np.round)
def round(a, **kwargs):
    return Quantity(np.round(a.value()), a.baseunits)

@implements(np.floor)
def round(a, **kwargs):
    return Quantity(np.floor(a.value()), a.baseunits)

@implements(np.ceil)
def round(a, **kwargs):
    return Quantity(np.ceil(a.value()), a.baseunits)
