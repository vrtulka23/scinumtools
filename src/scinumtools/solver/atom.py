from typing import Union
import numpy as np

class AtomBase:
    
    value: Union[float,bool]

    def __init__(self, value:Union[str,float,bool]):
        if isinstance(value,str):
            self.value = float(value.strip())
        else:
            self.value = value
            
    def __repr__(self):
        return f"Atom({self.value})"
    
    def __add__(self, other):
        return AtomBase(self.value + other.value)
    
    def __sub__(self, other):
        return AtomBase(self.value - other.value)
    
    def __mul__(self, other):
        return AtomBase(self.value * other.value)
    
    def __truediv__(self, other):
        return AtomBase(self.value / other.value)

    def __pow__(self, other):
        return AtomBase(self.value ** other.value)
    
    def __neg__(self):
        return AtomBase(-self.value)

    def log(self):
        return AtomBase(np.log(self.value))

    def log10(self):
        return AtomBase(np.log10(self.value))

    def sqrt(self):
        return AtomBase(np.sqrt(self.value))

    def sin(self):
        return AtomBase(np.sin(self.value))

    def cos(self):
        return AtomBase(np.cos(self.value))

    def tan(self):
        return AtomBase(np.tan(self.value))

    def logical_and(self, other):
        return AtomBase(self.value and other.value)

    def logical_or(self, other):
        return AtomBase(self.value or other.value)

    def logical_not(self):
        return AtomBase(not bool(self.value))

    def __eq__(self, other):
        return AtomBase(self.value == other.value)

    def __ne__(self, other):
        return AtomBase(self.value != other.value)

    def __le__(self, other):
        return AtomBase(self.value <= other.value)

    def __ge__(self, other):
        return AtomBase(self.value >= other.value)

    def __lt__(self, other):
        return AtomBase(self.value < other.value)

    def __gt__(self, other):
        return AtomBase(self.value > other.value)

    
