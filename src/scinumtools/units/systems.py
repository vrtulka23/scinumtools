from .settings import *
from .quantity import Quantity 

class SystemOfUnits:
    def __init__(self, prefix):
        self.prefix = prefix
        self.names = list(QUANTITY_LIST.name)
        self.symbols = list(QUANTITY_LIST.symbol)
    def __getattr__(self, quantity):
        idx = self.names.index(quantity)
        symbol = self.symbols[idx]
        def system(x=1):
            unit = f"{SYMBOL_SYSTEM_UNIT}{self.prefix}{symbol}"
            return Quantity(x, unit)
        return system
    def __getitem__(self, quantity):
        idx = self.names.index(quantity)
        symbol = self.symbols[idx]
        unit = f"{SYMBOL_SYSTEM_UNIT}{self.prefix}{symbol}"
        return unit

SI    = SystemOfUnits('S')
AU    = SystemOfUnits('A')
CGS   = SystemOfUnits('C')
