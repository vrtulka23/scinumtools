from typing import List
import numpy as np
import re
from typing import Union

from ..ParameterClass import ParameterTable
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
    dimensions: Dimensions    # quantity dimensions
    baseunits: BaseUnits      # base units

    precision: float = 1e-7

    def __init__(
            self, magnitude:float,
            dimensions: Union[str,list,np.ndarray,Dimensions,dict,BaseUnits] = None,
            baseunits: Union[dict,BaseUnits] = None
    ):
        # Initialize settings
        self.unitlist = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitStandard, keys=True)
        self.prefixes = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitPrefixes, keys=True)
        # Set magnitude
        if isinstance(magnitude, (int,float)):
            self.magnitude = float(magnitude)
        elif isinstance(magnitude, list):
            self.magnitude = np.array(magnitude, dtype=float)
        elif isinstance(magnitude, np.ndarray):
            self.magnitude = magnitude.astype(float)
        else:
            raise Exception("Magnitude can be either a number or an list/array of numbers")
        # Set quantity
        if dimensions is None:
            self.dimensions = Dimensions()
            self.baseunits = BaseUnits()
        elif isinstance(dimensions, (str, dict, BaseUnits)):
            if isinstance(dimensions, dict):
                dimensions = BaseUnits(dimensions).expression()
            elif isinstance(dimensions, BaseUnits):
                dimensions = dimensions.expression()
            if dimensions is None:
                unit = Quantity(1)
            else:
                with ExpressionSolver(self._atom_parser, [OperatorPar,OperatorMul,OperatorTruediv]) as es:
                    unit = es.solve(dimensions)
            self.magnitude *= unit.magnitude
            self.dimensions = unit.dimensions
            self.baseunits = unit.baseunits
        elif isinstance(dimensions, Quantity):
            self.magnitude *= dimensions.magnitude
            self.dimensions = dimensions.dimensions
            self.baseunits = dimensions.baseunits
        elif isinstance(dimensions, (list, np.ndarray, Dimensions)):
            if isinstance(dimensions, Dimensions):
                self.dimensions = dimensions
            else:
                self.dimensions = Dimensions(*dimensions)
            if isinstance(baseunits, dict):
                self.baseunits = BaseUnits(baseunits)
            elif isinstance(baseunits, BaseUnits):
                self.baseunits = baseunits
            else:
                self.baseunits = BaseUnits(self.dimensions.value(dtype=dict))
        else:
            raise Exception("Insufficient quantity definition", magnitude, dimensions, baseunits)
        if self.dimensions == Dimensions():
            self.baseunits = BaseUnits()

    def _add(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        if not left.dimensions == right.dimensions:
            raise Exception('Dimension does not match:', left.dimensions, right.dimensions)
        magnitude = left.magnitude + right.to(left.baseunits).magnitude 
        dimensions = left.dimensions
        baseunits = left.baseunits
        return Quantity(magnitude, dimensions, baseunits)

    def __add__(self, other):
        return self._add(self, other)
    
    def __radd__(self, other):
        return self._add(other, self)

    def _sub(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        if not left.dimensions == right.dimensions:
            raise Exception('Dimension does not match:', left.dimensions, right.dimensions)
        magnitude = left.magnitude - right.to(left.baseunits).magnitude
        dimensions = left.dimensions
        baseunits = left.baseunits
        return Quantity(magnitude, dimensions, baseunits)

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
        dimensions = left.dimensions + right.dimensions
        baseunits = left.baseunits + right.baseunits
        return Quantity(magnitude, dimensions, baseunits)

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
        dimensions = left.dimensions - right.dimensions
        baseunits = left.baseunits - right.baseunits
        return Quantity(magnitude, dimensions, baseunits)

    def __truediv__(self, other):
        return self._truediv(self, other)
    
    def __rtruediv__(self, other):
        return self._truediv(other, self)
    
    def __pow__(self, power: Union[float,int,tuple,Fraction]):
        if isinstance(power, tuple):
            exp = power[0]/power[1]
        elif isinstance(power, Fraction):
            exp = power.num/power.den
        else:
            exp = power
        magnitude = self.magnitude**exp
        dimensions = self.dimensions*power
        baseunits = self.baseunits*power
        return Quantity(magnitude, dimensions, baseunits)

    def __neg__(self):
        return Quantity(-self.magnitude, self.dimensions, self.baseunits)
    
    def __eq__(self, other):
        if not np.allclose(self.magnitude, other.magnitude, rtol=self.precision):
            return False
        if not self.dimensions==other.dimensions:
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
        return Quantity(self.magnitude[key], self.dimensions, self.baseunits)
        
    def __array__(self):
        return np.array(self.magnitude)
    
    def __array_prepare__(self, array, context=None):
        if context:
            if context[0] in [np.sin, np.cos, np.tan]:
                return np.array(context[1][0].to('rad'))
        return array
    
    def __array_wrap__(self, out_arr, context=None):
        if out_arr.ndim==0:
            out_arr = float(out_arr)
        dimensions = self.dimensions
        baseunits = self.baseunits
        if context:
            fn = context[0]
            if fn==np.sqrt:
                return Quantity(out_arr, dimensions/2, baseunits/2)
            elif fn==np.cbrt:
                return Quantity(out_arr, dimensions/3, baseunits/3)
            elif fn==np.power:
                return Quantity(out_arr, dimensions*context[1][1], baseunits*context[1][1])
            elif fn in [np.sin, np.cos, np.tan]:
                return Quantity(out_arr)
            elif fn in [np.arcsin, np.arccos, np.arctan]:
                return Quantity(out_arr, 'rad')
        return Quantity(out_arr, dimensions, baseunits)
    
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
        exp, base, prefix = '', '', ''
        symbol, string = string[-1], ' '+string[:-1]
        # parse exponent
        while len(string):
            if not re.match('^[0-9'+Fraction.symbol+'+-]{1}$', symbol):
                break
            exp = symbol+exp
            symbol, string = string[-1], string[:-1]
        # parse unit symbol
        unitkeys = self.unitlist.keys()
        while len(string):
            nbase = len(base)+1
            ukeys = [key[-nbase:] for key in unitkeys]
            if symbol+base not in ukeys:
                break
            base = symbol+base
            symbol, string = string[-1], string[:-1]
        unitid = f"{base:s}"
        if base not in self.unitlist.keys():
            raise Exception('Unknown unit', base, string_bak)
        magnitude = self.unitlist[base].magnitude
        dimensions = self.unitlist[base].dimensions
        # parse unit prefix
        while len(string):
            prefix = symbol+prefix
            symbol, string = string[-1], string[:-1]
            if symbol==' ':
                break
        if prefix:
            if isinstance(self.unitlist[base].prefixes,list) and prefix not in self.unitlist[base].prefixes:
                raise Exception(f"Unit can have only following prefixes:", self.unitlist[base].prefixes)
            elif self.unitlist[base].prefixes is True and prefix not in self.prefixes.keys():
                raise Exception(f"Unknown unit prefix:", string_bak)
            elif self.unitlist[base].prefixes is False:
                raise Exception(f"Unit cannot have any prefixes:", base)
            magnitude *= self.prefixes[prefix].magnitude
            unitid = f"{prefix:s}{BaseUnits.symbol}{unitid}"
        # apply exponent
        if exp:
            if Fraction.symbol in exp:
                exp = exp.split(Fraction.symbol)
                magnitude = magnitude**(int(exp[0])/int(exp[1]))
                exp = Fraction(int(exp[0]), int(exp[1]))
            else:
                exp = int(exp)
                magnitude = magnitude**exp
            dimensions = [exp*dim for dim in dimensions]
        else:
            exp = 1
        baseunits = {unitid: exp}
        return Quantity(magnitude, dimensions, baseunits)
    
    def value(self, expression=None, dtype=None):
        if expression:
            value = self.to(expression).value()
        elif expr:=self.baseunits.expression():
            value = (self/Quantity(1, expr)).magnitude
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
        if not unit1.dimensions==unit2.dimensions:
            # Check if inverted unit can be converted
            if -unit1.dimensions==unit2.dimensions:
                unit1 = Quantity(1)/self
            else:
                raise Exception("Converting units with different dimensions:",
                                unit1.dimensions, unit2.dimensions)
        with TemperatureConverter(unit1.baseunits.value(), unit2.baseunits.value()) as tc:
            if tc.convertable:
                unit2.magnitude = unit1.magnitude/tc.convert(unit1.magnitude, unit2.magnitude)
        unit = unit1/unit2
        return Quantity(unit.magnitude, units)

    def rebase(self):
        factor = 1
        baseunits = {}
        for unitid,exp in self.baseunits.baseunits.items():
            if ":" in unitid:
                prefix, base = unitid.split(":")
            else:
                prefix, base = '', unitid
            _, dimensions, _, _, _ = UnitStandard[base]
            dims = str(dimensions)
            if dims in baseunits:
                quant = Quantity(1, prefix+base).to(baseunits[dims][1]+baseunits[dims][2])
                factor *= quant.value()**(exp.num/exp.den)
                baseunits[dims][3] += exp
            else:
                baseunits[dims] = [unitid,prefix,base,exp]
        self.baseunits = BaseUnits({unitid:exp for unitid,prefix,base,exp in baseunits.values()})
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
