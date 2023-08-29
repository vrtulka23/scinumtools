import numpy as np

from .UnitList import UnitStandard
from .QuantityClass import Quantity
from ..ParameterClass import ParameterTable

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

    def __str__(self):
        return Constant._list()
        
    def __rep__(self):
        return Constant._list()

    @staticmethod
    def _list():
        unitlist = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitStandard, keys=True)
        sw, uw, dw = 8, 20, 20
        text = "Constants\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, unit in unitlist.items():
            if symbol.startswith('['):
                text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {unit['definition']:{dw}s}\n"
        return text
        
    @staticmethod
    def list():
        print(Constant._list())
            