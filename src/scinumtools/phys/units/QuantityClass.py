from typing import List
import numpy as np
import re
from typing import Union

from ...structs.ParameterClass import ParameterDict
from ...math.solver import ExpressionSolver, AtomBase, OperatorPar, OperatorMul, OperatorTruediv
from .UnitList import *
from .UnitConverters import *
#from .DimensionsClass import *

class Quantity:
    prefixes: dict            # list of prefixes 
    unitlist: dict            # list of units
    
    magnitude: float          # quantity magnitude
    dimensions: List[int]     # quantity dimensions
    baseunits: dict           # base units

    precision: float = 1e-7

    def __init__(
            self, magnitude:float,
            dimensions = None,
            baseunits = {}
    ):
        # Initialize settings
        self.unitlist = ParameterDict(['magnitude','dimensions','definition','name'], UnitStandard)
        self.prefixes = ParameterDict(['magnitude','dimensions','definition','name'], UnitPrefixes)
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
            self.dimensions = [0]*len(UnitBase)
            self.baseunits = {}
        elif isinstance(dimensions, str):
            with ExpressionSolver(self._atom_parser, [OperatorPar,OperatorMul,OperatorTruediv]) as es:
                unit = es.solve(dimensions)
            self.magnitude *= unit.magnitude
            self.dimensions = list(unit.dimensions)
            self.baseunits = dict(unit.baseunits)
        elif isinstance(dimensions, (list, np.ndarray)):
            self.dimensions = list(dimensions)
            if baseunits:
                self.baseunits = baseunits
            else:
                self.baseunits = {UnitBase[d]:dim for d,dim in enumerate(self.dimensions) if dim!=0}
        else:
            raise Exception("Insufficient quantity definition", magnitude, dimensions, baseunits)
        # Remove zero base units
        for unit in list(self.baseunits.keys()):
            if self.baseunits[unit]==0:
                del self.baseunits[unit]

    def _add(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        if not left.dimensions==right.dimensions:
            raise Exception('Addition of two units with different dimensions:', self, right)
        magnitude = left.magnitude + right.magnitude
        dimensions = list(left.dimensions)
        baseunits = dict(left.baseunits)
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
        if not left.dimensions==right.dimensions:
            raise Exception('Substraction of two units with different dimensions:', self, right)
        magnitude = left.magnitude - right.magnitude
        dimensions = list(left.dimensions)
        baseunits = dict(left.baseunits)
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
        dimensions = [left.dimensions[i]+right.dimensions[i] for i in range(len(UnitBase))]
        baseunits = dict(left.baseunits)
        for unit,exp in right.baseunits.items():
            baseunits[unit] = baseunits[unit]+exp if unit in baseunits else exp
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
        dimensions = [left.dimensions[i]-right.dimensions[i] for i in range(len(UnitBase))]
        baseunits = dict(left.baseunits)
        for unit,exp in right.baseunits.items():
            baseunits[unit] = baseunits[unit]-exp if unit in baseunits else -exp
        return Quantity(magnitude, dimensions, baseunits)

    def __truediv__(self, other):
        return self._truediv(self, other)
    
    def __rtruediv__(self, other):
        return self._truediv(other, self)
    
    def __pow__(self, power):
        magnitude = self.magnitude**power
        dimensions = [self.dimensions[i]*power for i in range(len(UnitBase))]
        baseunits = {unit:exp*power for unit,exp in self.baseunits.items()}
        return Quantity(magnitude, dimensions, baseunits)

    def __neg__(self):
        return Quantity(-self.magnitude, self.dimensions, self.baseunits)
    
    def __eq__(self, other):
        if not np.allclose(self.magnitude, other.magnitude, rtol=self.precision):
            return False
        if self.dimensions!=other.dimensions:
            return False
        return True
    
    def __str__(self):
        magnitude = self.value()
        if isinstance(magnitude, np.ndarray):
            with np.printoptions(precision=3, suppress=False, threshold=5):
                magnitude = f"{str(magnitude):s}"
        else:
            magnitude = f"{magnitude:.03e}"
        if self.baseunits:
            return f"Quantity({magnitude:s} {self.units()})"
        else:
            return f"Quantity({magnitude:s})"
            
    def __repr__(self):
        magnitude = self.value()
        if isinstance(magnitude, np.ndarray):
            with np.printoptions(precision=3, suppress=False, threshold=5):
                magnitude = f"{str(magnitude):s}"
        else:
            magnitude = f"{magnitude:.03e}"
        if self.baseunits:
            return f"Quantity({magnitude:s} {self.units()})"
        else:
            return f"Quantity({magnitude:s})"

    def __array__(self):
        return self.magnitude

    def __array_wrap__(self, out_arr, context=None):
        """
        if context[0]==np.sqrt:
            dimensions = []
            for d in range(len(UnitBase)):
                dimensions.append( self.dimensions[d] )
                if dimensions[d]==0:
                    continue
                elif isinstance(dimensions[d], int):
                    dimensions[d] = Ratio(dimensions[d], 2)
                elif isinstance(dimensions[d], Ratio):
                    dimensions[d] = Ratio(dimensions[d][0], dimensions[d][1]+2)
            print(dimensions)
        """
        return Quantity(out_arr, self.dimensions, self.baseunits)
    
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
            if not re.match('^[0-9+-]{1}$', symbol):
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
        magnitude = self.unitlist[base].magnitude
        dimensions = self.unitlist[base].dimensions
        # parse unit prefix
        while len(string):
            prefix = symbol+prefix
            symbol, string = string[-1], string[:-1]
            if symbol==' ':
                break
        if prefix:
            if prefix not in self.prefixes.keys():
                raise Exception(f"Unknown unit prefix:", string_bak)
            magnitude *= self.prefixes[prefix].magnitude
            unitid = f"{prefix:s}:{unitid}"
        # apply exponent
        if exp:
            exp = int(exp)
            magnitude = magnitude**exp
            dimensions = [dim*exp for dim in dimensions]
            baseunits = {unitid: exp}
        else:
            baseunits = {unitid: 1}
        return Quantity(magnitude, dimensions, baseunits)
    
    def value(self):
        if self.baseunits:
            unit = self/Quantity(1,self.units(self.baseunits))
        else:
            return self.magnitude
        return unit.magnitude

    def units(self, baseunits=None):
        if baseunits is None:
            baseunits = self.baseunits
        units = []
        for unitid,exponent in baseunits.items():
            symbol = unitid.replace(':','')
            units.append(f"{symbol}" if exponent==1 else f"{symbol}{exponent}")
        return "*".join(units)

    def to(self, units):
        if isinstance(units,str):
            unit1 = self
            unit2 = Quantity(1,units)
            # Check if units can be directly converted
            if unit1.dimensions!=unit2.dimensions:
                # Check if inverted unit can be converted
                if np.all([-unit1.dimensions[d]==unit2.dimensions[d] for d in range(len(UnitBase))]):
                    unit1 = Quantity(1)/self
                else:
                    raise Exception("Converting units with different dimensions:",
                                    unit1.dimensions, unit2.dimensions)
            with TemperatureConverter(unit1.baseunits, unit2.baseunits) as tc:
                if tc.convertable:
                    unit2.magnitude = unit1.magnitude/tc.convert(unit1.magnitude, unit2.magnitude)
                    #return Quantity(tc.convert(unit1.magnitude, unit2.magnitude), units)
            unit = unit1/unit2
            return Quantity(unit.magnitude, units)
        else:
            raise Exception("Invalid units format:", units)
