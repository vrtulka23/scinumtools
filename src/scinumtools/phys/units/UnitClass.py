from .UnitList import UnitStandard
from .QuantityClass import Quantity

class Unit:
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def __new__(cls, unit=None):
        if unit:
            return Quantity(1,str(unit))
        else:
            return object.__new__(cls)
    
    def __getattr__(self, unit):
        return Quantity(1,str(unit))

class Constant:

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def __new__(cls, unit=None):
        if unit:
            return Quantity(1,f"[{str(unit)}]")
        else:
            return object.__new__(cls)
    
    def __getattr__(self, unit):
        return Quantity(1,f"[{str(unit)}]")
