from .UnitList import UnitStandard
from .QuantityClass import Quantity

class Unit:

    def __new__(cls, unit=None):
        if unit:
            return Quantity(1,str(unit))
        else:
            return object.__new__(cls)
    
    def __getattr__(self, unit):
        return Quantity(1,str(unit))

class Constant:

    def __new__(cls, unit=None):
        if unit:
            return Quantity(1,f"[{str(unit)}]")
        else:
            return object.__new__(cls)
    
    def __getattr__(self, unit):
        return Quantity(1,f"[{str(unit)}]")
