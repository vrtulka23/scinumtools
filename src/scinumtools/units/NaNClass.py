import numpy as np

from .QuantityClass import Quantity

class NaN:

    def __new__(cls, unit=None):
        if unit:
            return Quantity(np.nan,str(unit))
        else:
            return Quantity(np.nan)
    