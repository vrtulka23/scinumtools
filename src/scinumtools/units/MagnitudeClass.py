import numpy as np
from dataclasses import dataclass, field

class Magnitude:
    value: float
    error: float = None   # absolute error 

    def __init__(self, value: float, abse: float = None, rele: float = None):
        self.value = value
        if abse is not None and rele is None:
            self.error = abse
        elif abse is None and rele is not None:
            self.error = self._rel_to_abs(rele)
        if abse is not None and rele is not None:
            raise Exception("Magnitude cannot have both absolute and relative errors!", abse, rele)

    def _rel_to_abs(self, rele):
        return self.value*rele/100
        
    def _to_string(self):
        exps = np.floor(np.log10([np.abs(self.value),self.error]))
        diff = np.abs(exps[0]-exps[1])
        value = self.value*10**-exps[0]
        vformat = f".0{int(diff+1)}f"
        error = int(np.round(np.round(self.error*10**(1-exps[1]),decimals=1))) # double round because of values like 0.4999999
        exponent = int(np.abs(np.round(exps[0])))
        sign = "e+" if exps[0]>=0  else "e-"
        return f"{value:{vformat}}({error:2d}){sign}{exponent:-02d}"
        
    def __str__(self):
        if self.error is None:
            return f"{self.value:.03e}"
        else:          
            return self._to_string()

    def __repr__(self):
        if self.error is None:
            return f"{self.value:.03e}"
        else:          
            return self._to_string()

    def _add(self, left, right):
        value = left.value + right.value
        if left.error is None and right.error is None:
            error = None
        elif left.error is None and right.error is not None:
            error = right.error
        elif left.error is not None and right.error is None:
            error = left.error
        else:
            error = left.error + right.error
        return Magnitude(value, error)
        
    def __add__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._add(self, other)
        
    def __radd__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._add(other, self)
        
    def _sub(self, left, right):
        value = left.value - right.value
        if left.error is None and right.error is None:
            error = None
        elif left.error is None and right.error is not None:
            error = right.error
        elif left.error is not None and right.error is None:
            error = left.error
        else:
            error = left.error + right.error
        return Magnitude(value, error)
        
    def __sub__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._sub(self, other)
        
    def __rsub__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._sub(other, self)
        
    def _mul(self, left, right):
        value = left.value * right.value
        if left.error is None and right.error is None:
            error = None
        elif left.error is None and right.error is not None:
            error = right.error * left.value
        elif left.error is not None and right.error is None:
            error = left.error * right.value
        else:
            maxerror = np.abs((left.value+left.error)*(right.value+right.error) - value)
            minerror = np.abs((left.value-left.error)*(right.value-right.error) - value)
            error = np.max([maxerror,minerror])
        return Magnitude(value, error)
        
    def __mul__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._mul(self, other)
        
    def __rmul__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._mul(other, self)
        
    def _truediv(self, left, right):
        value = left.value / right.value
        if left.error is None and right.error is None:
            error = None
        elif left.error is None and right.error is not None:
            maxerror = np.abs(left.value / (right.value+right.error) - value)
            minerror = np.abs(left.value / (right.value-right.error) - value)
            error = np.max([maxerror,minerror])
        elif left.error is not None and right.error is None:
            error = left.error / right.value
        else:
            maxerror = np.abs((left.value+left.error)/(right.value-right.error) - value)
            minerror = np.abs((left.value-left.error)/(right.value+right.error) - value)
            error = np.max([maxerror,minerror])
        return Magnitude(value, error)
        
    def __truediv__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._truediv(self, other)
        
    def __rtruediv__(self, other):
        if not isinstance(other, Magnitude):
            other = Magnitude(other)
        return self._truediv(other, self)
        