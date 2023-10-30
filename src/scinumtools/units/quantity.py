from typing import List
import numpy as np
from decimal import Decimal
import re
from typing import Union

from .settings import *
from .unit_types import *
from .magnitude import Magnitude
from .dimensions import Dimensions
from .base_units import BaseUnits, get_unit_base
from .fraction import Fraction
from .unit_solver import UnitSolver

HANDLED_FUNCTIONS = {}

class Quantity:
    
    magnitude: Magnitude      # magnitude
    baseunits: BaseUnits      # base units

    def __init__(
        self, 
        magnitude: Union[int,float,Decimal,list,np.ndarray,Magnitude],
        baseunits: Union[str,list,np.ndarray,Dimensions,dict,BaseUnits] = None,
        abse: Union[int,float] = None,
        rele: Union[int,float] = None
    ):
        # Set magnitude
        if isinstance(magnitude, (int,float,Decimal,list,np.ndarray)):
            self.magnitude = Magnitude(magnitude, abse=abse, rele=rele)
        elif isinstance(magnitude, Magnitude):
            if abse is not None:
                magnitude.abse(abse)
            elif rele is not None:
                magnitude.rele(rele)
            self.magnitude = magnitude
        else:
            raise Exception("Magnitude can be either a number or an list/array of numbers", magnitude)
        # Set base units
        if baseunits is None or isinstance(baseunits, (dict,Dimensions,list,np.ndarray)):
            self.baseunits = BaseUnits(baseunits)
        elif isinstance(baseunits, BaseUnits):
            self.baseunits = baseunits
        elif isinstance(baseunits, (SI,CGS,AU)):
            self.baseunits = BaseUnits(baseunits)
        elif isinstance(baseunits, str):
            atom = UnitSolver(baseunits)
            self.magnitude *= atom.magnitude
            self.baseunits = BaseUnits(atom.baseunits)
        elif isinstance(baseunits, Quantity):
            self.magnitude *= baseunits.magnitude
            self.baseunits = baseunits.baseunits
        else:
            raise Exception("Insufficient quantity definition", magnitude, baseunits)
        # rebase if dimensions are zero
        if self.baseunits.dimensions.nodim:
            baseunits = {}
            for unitid, exp in self.baseunits.baseunits.items():
                base = get_unit_base(unitid, exp)
                if base.dimensions.nodim:
                    baseunits[unitid] = exp
                    continue
                else:
                    self.magnitude *= base.magnitude
            self.baseunits = BaseUnits(baseunits)

    def _add(self, left, right):
        for utype in UNIT_TYPES:
            if c := utype(left.baseunits, right.baseunits):
                magnitude = c.add(left, right)
                baseunits = left.baseunits
                return Quantity(magnitude, baseunits)
        else:
            raise Exception("Unsupported addition between units:", left, right)

    def __add__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._add(self, other)
    
    def __radd__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._add(other, self)

    def _sub(self, left, right):
        for utype in UNIT_TYPES: 
            if c := utype(left.baseunits, right.baseunits):
                magnitude = c.sub(left, right)
                baseunits = left.baseunits
                return Quantity(magnitude, baseunits)
        else:
            raise Exception("Unsupported subtraction between units:", left, right)

    def __sub__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._sub(self, other)

    def __rsub__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._sub(other, self)
    
    def _mul(self, left, right):
        magnitude = left.magnitude * right.magnitude
        baseunits = left.baseunits + right.baseunits
        return Quantity(magnitude, baseunits)

    def __mul__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._mul(self, other)

    def __rmul__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._mul(other, self)
    
    def _truediv(self, left, right):
        magnitude = left.magnitude / right.magnitude
        baseunits = left.baseunits - right.baseunits
        return Quantity(magnitude, baseunits)

    def __truediv__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
        return self._truediv(self, other)
    
    def __rtruediv__(self, other):
        if not isinstance(other, Quantity):
            other = Quantity(other)
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
        if isinstance(other, (int, float)):
            other = Quantity(other)
        if np.all(other.magnitude.value!=0):
            other.to(self.units())
        if not np.allclose(self.magnitude.value, other.magnitude.value, rtol=MAGNITUDE_PRECISION):
            return False
        if not self.baseunits==other.baseunits:
            return False
        return True
    
    def __str__(self):
        magnitude = str(self.magnitude)
        baseunits = self.baseunits.expression
        if baseunits:
            return f"Quantity({magnitude:s} {baseunits})"
        else:
            return f"Quantity({magnitude:s})"
            
    def __repr__(self):
        magnitude = str(self.magnitude)
        baseunits = self.baseunits.expression
        if baseunits:
            return f"Quantity({magnitude:s} {baseunits})"
        else:
            return f"Quantity({magnitude:s})"

    def __getitem__(self, key):
        return Quantity(self.magnitude.value[key], self.baseunits)
        
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if ufunc==np.sqrt:
            return Quantity(ufunc(inputs[0].magnitude.value), inputs[0].baseunits/2)
        elif ufunc==np.cbrt:
            return Quantity(ufunc(inputs[0].magnitude.value), inputs[0].baseunits/3)
        elif ufunc==np.power:
            return Quantity(ufunc(inputs[0].magnitude.value,inputs[1]), inputs[0].baseunits*inputs[1])
        elif ufunc in [np.sin, np.cos, np.tan]:
            return Quantity(ufunc(inputs[0].to('rad').magnitude.value))
        elif ufunc in [np.arcsin, np.arccos, np.arctan]:
            return Quantity(ufunc(inputs[0].to(None).magnitude.value),'rad')
        elif ufunc in [np.isnan, np.isnat]:
            return ufunc(inputs[0].magnitude.value)
        else:
            return Quantity(ufunc(inputs[0].magnitude.value), inputs[0].baseunits)
    
    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            raise NotImplementedError()
        return HANDLED_FUNCTIONS[func](*args, **kwargs)
    
    def _convert(self, magnitude1, baseunits1, baseunits2):
        for utype in UNIT_TYPES:
            if c := utype(baseunits1, baseunits2):
                return c.convert(magnitude1)
        else:
            raise Exception("Unsupported conversion between units:", baseunits1.expression, baseunits2.expression)

    def value(self, expression=None, dtype=None):
        if expression:
            value = self._convert(self.magnitude, self.baseunits, BaseUnits(expression)).value
        else:
            value = self.magnitude.value
        if dtype:
            return value.astype(dtype) if isinstance(value, np.ndarray) else dtype(value)
        else:
            return value

    def units(self):
        return self.baseunits.expression

    def to(self, units: Union[str,list,np.ndarray,Dimensions,dict,BaseUnits]):
        if isinstance(units, Quantity):
            baseunits = units.baseunits
            self.magnitude = self._convert(self.magnitude, self.baseunits, baseunits) / units.magnitude
        else:
            baseunits = BaseUnits(units)
            self.magnitude = self._convert(self.magnitude, self.baseunits, baseunits)
        self.baseunits = baseunits
        return self
        
    def abse(self, error: Union[int,float] = None):
        if error is None:
            return self.magnitude.abse()
        else:
            self.magnitude.abse(error)
            return self
        
    def rele(self, error: Union[int,float] = None):
        if error is None:
            return self.magnitude.rele()
        else:
            self.magnitude.rele(error)
            return self
    
    def rebase(self):
        factor = 1
        baseunits = {}
        for unitid1,exp1 in self.baseunits.baseunits.items():
            # find base units
            base1 = get_unit_base(unitid1)
            dim1 = str(base1.dimensions.value(dtype=tuple))
            if dim1 in baseunits:
                # exists: convert units
                base0 = get_unit_base(baseunits[dim1][0])
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
    return Quantity(np.linspace(a.magnitude.value, b.magnitude.value, c, **kwargs), a.baseunits)

@implements(np.logspace)
def logspace(a, b, c, **kwargs):
    if isinstance(a,Quantity):
        b = b.to(a.baseunits) if isinstance(b,Quantity) else Quantity(b, a.baseunits)
    else:
        a = a.to(b.baseunits) if isinstance(a,Quantity) else Quantity(a, b.baseunits)
    return Quantity(np.logspace(a.magnitude.value, b.magnitude.value, c, **kwargs), a.baseunits)

@implements(np.absolute)
def absolute(a, **kwargs):
    return Quantity(np.absolute(a.magnitude.value), a.baseunits)

@implements(np.abs)
def abs(a, **kwargs):
    return Quantity(np.abs(a.magnitude.value), a.baseunits)

@implements(np.round)
def round(a, **kwargs):
    return Quantity(np.round(a.magnitude.value), a.baseunits)

@implements(np.floor)
def floor(a, **kwargs):
    return Quantity(np.floor(a.magnitude.value), a.baseunits)

@implements(np.ceil)
def ceil(a, **kwargs):
    return Quantity(np.ceil(a.magnitude.value), a.baseunits)
    
@implements(np.iscomplexobj)
def iscomplexobj(a, **kwargs):
    return False
