from typing import List
import numpy as np
import re
from typing import Union

from ...structs.ParameterClass import ParameterDict
from ...math.solver import ExpressionSolver, AtomBase, OperatorPar, OperatorMul, OperatorTruediv
from .UnitList import *
from .UnitConverters import *
from .DimensionsClass import Dimensions
from .BaseUnitsClass import BaseUnits
from .RatioClass import Ratio

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
            self.dimensions = Dimensions()
            self.baseunits = BaseUnits()
        elif isinstance(dimensions, (str, dict, BaseUnits)):
            if isinstance(dimensions, dict):
                dimensions = BaseUnits(dimensions).expression()
            elif isinstance(dimensions, BaseUnits):
                dimensions = dimensions.expression()
            with ExpressionSolver(self._atom_parser, [OperatorPar,OperatorMul,OperatorTruediv]) as es:
                unit = es.solve(dimensions)
            self.magnitude *= unit.magnitude
            self.dimensions = unit.dimensions
            self.baseunits = unit.baseunits
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
                print(self.dimensions)
                self.baseunits = BaseUnits({UnitBase[d]:dim for d,dim in enumerate(self.dimensions.value()) if dim!=0})
        else:
            raise Exception("Insufficient quantity definition", magnitude, dimensions, baseunits)

    def _add(self, left, right):
        if not isinstance(left, Quantity):
            left = Quantity(left)
        if not isinstance(right, Quantity):
            right = Quantity(right)
        magnitude = left.magnitude + right.magnitude
        if not left.dimensions == right.dimensions:
            raise Exception('Dimension does not match:', left.dimensions, right.dimensions)
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
        magnitude = left.magnitude - right.magnitude
        if not left.dimensions == right.dimensions:
            raise Exception('Dimension does not match:', left.dimensions, right.dimensions)
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
    
    def __pow__(self, power):
        magnitude = self.magnitude**power
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

    def __array__(self):
        return self.magnitude

    def __array_wrap__(self, out_arr, context=None):
        dimensions = self.dimensions
        baseunits = self.baseunits
        if context:
            if context[0]==np.sqrt:
                dimensions /= 2
                baseunits /= 2
            elif context[0]==np.cbrt:
                dimensions /= 3
                baseunits /= 3
            elif context[0]==np.power:
                dimensions *= context[1][1]
                baseunits *= context[1][1]
        return Quantity(out_arr, dimensions, baseunits)
    
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
            if not re.match('^[0-9'+Ratio.symbol+'+-]{1}$', symbol):
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
            unitid = f"{prefix:s}{BaseUnits.symbol}{unitid}"
        # apply exponent
        if exp and Ratio.symbol in exp:
            exp = exp.split(Ratio.symbol)
            exprat = Ratio(int(exp[0]), int(exp[1]))
            magnitude = magnitude**(int(exp[0])/int(exp[1]))
            dimensions = [exprat*dim for dim in dimensions]
            baseunits = {unitid: exprat}
        elif exp:
            exp = int(exp)
            magnitude = magnitude**exp
            dimensions = [dim*exp for dim in dimensions]
            baseunits = {unitid: exp}            
        else:
            baseunits = {unitid: 1}
        return Quantity(magnitude, dimensions, baseunits)
    
    def value(self):
        baseunits = self.baseunits.expression()
        if baseunits:
            unit = self/Quantity(1,baseunits)
            return unit.magnitude
        else:
            return self.magnitude

    def units(self):
        return self.baseunits.expression()

    def to(self, units):
        if isinstance(units,str):
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
        else:
            raise Exception("Invalid units format:", units)
