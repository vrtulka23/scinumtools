import numpy as np
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union

class Magnitude:
    value: Union[int,float,Decimal,np.ndarray]
    error: Union[int,float,Decimal,np.ndarray] = None   # absolute error 

    def __init__(self, value: float, abse: float = None, rele: float = None):
        # set value
        if isinstance(value, (float,int)):
            self.value = float(value)
        elif isinstance(value, Decimal):
            self.value = value
        elif isinstance(value, list):
            self.value = np.array(value, dtype=float)
        elif isinstance(value, np.ndarray):
            self.value = value.astype(float)
        else:
            raise Exception("Magnitude value can be either a number or an list/array of numbers", value)
        # set error
        if abse is not None and rele is not None:
            raise Exception("Magnitude cannot have both absolute and relative errors!", abse, rele)
        elif abse is not None and rele is None:
            self.error = abse
        elif abse is None and rele is not None:
            self.error = self._rel_to_abs(rele)
        # set array of errors if value is an array
        if isinstance(self.value, np.ndarray) and self.error is not None:
            self.error = np.full_like(self.value, self.error)
            
    def _rel_to_abs(self, rele):
        return self.value*rele/100
        
    def _abs_to_rel(self, abse=None):
        if abse is None:
            abse = self.error
        return 100*abse/self.value
        
    @staticmethod
    def parse_string(value, error):
        def formatter(val, err):
            exps = np.floor(np.log10([np.abs(val),err]))
            val = val*10**-exps[0]
            ndec = int(np.abs(exps[0]-exps[1])+1)
            vformat = f".0{ndec}f"
            err = int(np.round(np.round(err*10**(1-exps[1]),decimals=1))) # double round because of values like 0.4999999
            exponent = int(np.abs(np.round(exps[0])))
            sign = "+" if exps[0]>=0  else "-"
            return f"{val:{vformat}}({err:2d})e{sign}{exponent:-02d}"
        if isinstance(value, np.ndarray):
            out = np.empty_like(value, dtype=object)
            for index, x in np.ndenumerate(out):
                out[index] = formatter(value[index],error[index])
            return np.array2string(out, formatter={'all': lambda x: str(x)})
        else:
            return formatter(value,error)
    
    def _str(self):    
        if self.error is None:
            if isinstance(self.value, (list,np.ndarray)):
                with np.printoptions(precision=3, suppress=False, threshold=5):
                    return str(self.value)
            else:
                return f"{self.value:.03e}"
        else:          
            return Magnitude.parse_string(self.value, self.error)
    
    def __str__(self):
        return self._str()
        
    def __repr__(self):
        return self._str()

    def _add(self, left, right):
        if isinstance(left.value, Decimal) or isinstance(right.value, Decimal):
            value = Decimal(left.value) + Decimal(right.value)
        else:
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
        if isinstance(left.value, Decimal) or isinstance(right.value, Decimal):
            value = Decimal(left.value) - Decimal(right.value)
        else:
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
        if isinstance(left.value, Decimal) or isinstance(right.value, Decimal):
            value = Decimal(left.value) * Decimal(right.value)
        else:
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
        if isinstance(left.value, Decimal) or isinstance(right.value, Decimal):
            value = Decimal(left.value) / Decimal(right.value)
        else:
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
        
    def __pow__(self, power: Union[float,int]):
        value = self.value**power
        if self.error is not None:
            error = self._rel_to_abs(self._abs_to_rel()*power)
        else:
            error = None
        return Magnitude(value, error)
        
    def __neg__(self):
        return Magnitude(-self.value, self.error)
        
    def abse(self, abse=None):
        if abse is None:
            return self.error
        else:
            self.error = abse
            return self
        
    def rele(self, rele=None):
        if rele is None:
            return self._abs_to_rel()
        else:
            self.error = self._rel_to_abs(rele)
            return self
            
            