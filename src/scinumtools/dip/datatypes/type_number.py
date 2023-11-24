import numpy as np
from math import isclose

from ...units import Quantity, UnitEnvironment
from .type import Type
from .type_boolean import BooleanType
from ..settings import Numeric

class NumberType(Type):
    dtype = None
    typename: str = 'number'

    def _prepare(self, other):
        if self.dtype not in [int,float,str,bool]:
            # if self node datatype is unknown
            if other is None:
                return self.value, None
            elif other.dtype is None:
                self.value = float(self.value)
            else:
                if other.dtype in [int,float]:
                    self.convert(other.unit)
                self.value = other.dtype(self.value)
        elif other.dtype not in [int,float,str,bool]:
            # if other node datatype is unknown
            if self.dtype in [int,float]:
                other.convert(self.unit)
            other.value = self.dtype(other.value)
        elif type(self)==type(other):
            # if both datatypes are known
            if self.dtype in [int,float]:
                self.convert(other.unit)
        else:                               # throw error if both datatypes are unknown
            raise Exception("Invalid comparison:", expr)
        return self.value, other.value
            
    def __eq__(self, other):
        left, right = self._prepare(other)
        if isinstance(left,str) and isinstance(right,str):
            return left==right
        elif isinstance(left,(list,np.ndarray)) and isinstance(right,(list,np.ndarray)):
            return np.all(np.isclose(left, right, rtol=Numeric.PRECISION))
        elif left is None and right is None:
            return True
        elif left is None or right is None:
            return False
        else:
            # isclose does not work with integers
            return np.isclose(float(left), float(right), rtol=Numeric.PRECISION)
        
    def __ne__(self, other):
        left, right = self._prepare(other)
        return BooleanType(left != right)

    def __lt__(self, other):
        left, right = self._prepare(other)
        return BooleanType(left < right)

    def __gt__(self, other):
        left, right = self._prepare(other)
        return BooleanType(left > right)

    def __le__(self, other):
        left, right = self._prepare(other)
        return BooleanType((left<right)|np.isclose(left, right, rtol=Numeric.PRECISION))

    def __ge__(self, other):
        left, right = self._prepare(other)
        return BooleanType((left>right)|np.isclose(left, right, rtol=Numeric.PRECISION))
        
    def convert(self, unit, env=None):
        """ Convert units of this type
        """
        if unit:
            if self.unit and self.unit!=unit:
                if env is None:
                    self.value = Quantity(float(self.value), self.unit).value(unit)
                else:
                    with UnitEnvironment(env.units):
                        self.value = Quantity(float(self.value), self.unit).value(unit)
                self.unit = unit
        return self
 