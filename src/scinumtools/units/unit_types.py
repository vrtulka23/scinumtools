import numpy as np
from decimal import Decimal

from .magnitude import Magnitude

class UnitType:

    def __new__(cls, baseunits1, baseunits2):
        obj = object.__new__(cls)
        obj.baseunits1 = baseunits1
        obj.baseunits2 = baseunits2
        if obj._istype():
            return obj
        else:
            return None
            
    def convert(self, magnitude1):
        if not hasattr(self, self.conversion[0]):
                raise Exception('Conversion method is not implemented:', self.conversion[0])
        if isinstance(magnitude1.value, Decimal) or \
           isinstance(self.baseunits1.magnitude, Decimal) or \
           isinstance(self.baseunits2.magnitude, Decimal):
            magnitude1.value = Decimal(magnitude1.value)
            self.baseunits1.magnitude = Decimal(self.baseunits1.magnitude)
            self.baseunits2.magnitude = Decimal(self.baseunits2.magnitude)
        return Magnitude(
            getattr(self, self.conversion[0])(magnitude1.value * self.baseunits1.magnitude, *self.conversion[1:]) / self.baseunits2.magnitude,
            magnitude1.error
        )
        
    def add(self, unit1, unit2):
        if self.baseunits1.dimensions!=self.baseunits2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        return unit1.magnitude + unit2.to(unit1.baseunits).magnitude

    def sub(self, unit1, unit2):
        if self.baseunits1.dimensions!=self.baseunits2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        return unit1.magnitude - unit2.to(unit1.baseunits).magnitude

class StandardUnitType(UnitType):

    def _istype(self):
        if self.baseunits1.dimensions==self.baseunits2.dimensions:
            self.conversion = (f"_convert_linear",)
        elif -self.baseunits1.dimensions==self.baseunits2.dimensions:
            self.conversion = (f"_convert_inversed",)
        elif self.baseunits1.nobase and self.baseunits2.units==['rad']:
            self.conversion = (f"_convert_linear",)
        else:
            return False
        return True

    def _convert_inversed(self, value):
        return 1/value

    def _convert_linear(self, value):
        return value

class TemperatureUnitType(UnitType):
    
    process = ['Cel','degF']
    
    def _istype(self):
        if np.any(np.in1d(self.baseunits1.units+self.baseunits2.units, self.process)):
            if len(self.baseunits1.units)!=1 or len(self.baseunits2.units)!=1:
                raise Exception("Only simple units can be converted between each other:",
                                self.baseunits1.units, self.baseunits2.units)
            self.conversion = (f"_convert_{self.baseunits1.units[0]}_{self.baseunits2.units[0]}",)
        else:
            return False
        return True
    
    def _convert_K_Cel(self, value):
        return value-273.15
        
    def _convert_K_degF(self, value):
        return (value-273.15)*9/5+32
        
    def _convert_degR_degF(self, value):
        return value*9/5-459.67
        
    def _convert_degR_Cel(self, value):
        return (value*9/5-491.67)*5/9
        
    def _convert_Cel_K(self, value):
        return value+273.15
        
    def _convert_Cel_degF(self, value):
        return (value*9/5)+32
        
    def _convert_Cel_degR(self, value):
        return ((value*9/5)+491.67)*5/9
        
    def _convert_degF_K(self, value):
        return ((value-32)*5/9)+273.15
    
    def _convert_degF_Cel(self, value):
        return (value-32)*5/9
        
    def _convert_degF_degR(self, value):
        return (value+459.67)*5/9
        
        
class LogarithmicUnitType(UnitType):

    process: list = ['Np','B','Bm','BmW','BW','BV','BuV','BA','BuA','BOhm','BSPL','BSIL','BSWL']
    conversions: dict = {
        # power ratios
        'PR_Np':    ("_convert_Ratio_Np",  0.5, 1),    # Nepers
        'Np_PR':    ("_convert_Np_Ratio",  0.5, 1),
        'PR_B':     ("_convert_Ratio_B",   1,   1),    # Bel
        'B_PR':     ("_convert_B_Ratio",   1,   1),
        'W_Bm':     ("_convert_Ratio_B",   1,   1),
        'W_BmW':    ("_convert_Ratio_B",   1,   1),
        'Bm_W':     ("_convert_B_Ratio",   1,   1),
        'BmW_W':    ("_convert_B_Ratio",   1,   1),
        'W_BW':     ("_convert_Ratio_B",   1,   1e-3),
        'BW_W':     ("_convert_B_Ratio",   1,   1e3),
        'W_BSIL':   ("_convert_Ratio_B",   1,   1e9),  # W/m2
        'BSIL_W':   ("_convert_B_Ratio",   1,   1e-9),
        'W_BSWL':   ("_convert_Ratio_B",   1,   1e9),  # W
        'BSWL_W':   ("_convert_B_Ratio",   1,   1e-9),
        # amplitude ratios
        'AR_Np':    ("_convert_Ratio_Np",  1,   1),    # Nepers
        'Np_AR':    ("_convert_Np_Ratio",  1,   1),
        'AR_B':     ("_convert_Ratio_B",   2,   1),    # Bel
        'B_AR':     ("_convert_B_Ratio",   2,   1),
        'V_BV':     ("_convert_Ratio_B",   2,   1e-3),
        'BV_V':     ("_convert_B_Ratio",   2,   1e3),
        'V_BuV':    ("_convert_Ratio_B",   2,   1e3),
        'BuV_V':    ("_convert_B_Ratio",   2,   1e-3),
        'A_BA':     ("_convert_Ratio_B",   2,   1),
        'BA_A':     ("_convert_B_Ratio",   2,   1),
        'A_BuA':    ("_convert_Ratio_B",   2,   1e6),
        'BuA_A':    ("_convert_B_Ratio",   2,   1e-6),
        'Ohm_BOhm': ("_convert_Ratio_B",   2,   1e-3),
        'BOhm_Ohm': ("_convert_B_Ratio",   2,   1e3),
        'Pa_BSPL':  ("_convert_Ratio_B",   2,   50),
        'BSPL_Pa':  ("_convert_B_Ratio",   2,   0.02),
        # same decibel conversions
        'Bm_Bm':    ("_convert_B_B",       0),
        'BW_BW':    ("_convert_B_B",       0),
        'BmW_BmW':  ("_convert_B_B",       0),
        'BV_BV':    ("_convert_B_B",       0),
        'BuV_BuV':  ("_convert_B_B",       0),
        'BA_BA':    ("_convert_B_B",       0),
        'BuA_BuA':  ("_convert_B_B",       0),
        'BOhm_BOhm':("_convert_B_B",       0),
        'BSPL_BSPL':("_convert_B_B",       0),
        'BSIL_BSIL':("_convert_B_B",       0),
        'BSWL_BSWL':("_convert_B_B",       0),
        # different decibel conversions
        'BW_Bm':    ("_convert_B_B",       3),
        'Bm_BW':    ("_convert_B_B",      -3),
        'BW_BmW':   ("_convert_B_B",       3),
        'BmW_BW':   ("_convert_B_B",      -3),
        'Bm_BmW':   ("_convert_B_B",       0),
        'BmW_Bm':   ("_convert_B_B",       0),
        'BV_BuV':   ("_convert_B_B",       12),
        'BuV_BV':   ("_convert_B_B",      -12),
    }
    
    def _istype(self):
        if np.any(np.in1d(self.baseunits1.units+self.baseunits2.units, self.process)):
            if len(self.baseunits1.units) not in [1,2] or len(self.baseunits2.units) not in [1,2]:
                raise Exception("Only simple and fraction units can be converted between each other:",
                                self.baseunits1.units, self.baseunits2.units)
            conversion = f"{self.baseunits1.units[0]}_{self.baseunits2.units[0]}"
            if conversion in self.conversions:
                self.conversion = self.conversions[conversion]
            else:
                self.conversion = (f"_convert_{conversion}",)
        else:
            return False
        return True
    
    def _convert_B_B(self, value, exp=0):
        return value + exp
        
    def _convert_B_Np(self, value):
        return 1.151277918*value
        
    def _convert_Np_B(self, value):
        return value/1.151277918
        
    def _convert_Ratio_B(self, value, exp, conv):
        return exp*np.log10(value*conv)
        
    def _convert_B_Ratio(self, value, exp, conv):
        return np.power(10,value/exp)*conv
        
    def _convert_Ratio_Np(self, value, exp, conv):
        return exp*np.log(value*conv)
        
    def _convert_Np_Ratio(self, value, exp, conv):
        return np.exp(value/exp)*conv
        
    def add(self, unit1, unit2):
        if self.baseunits1.dimensions!=self.baseunits2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        if self.baseunits1.units!=self.baseunits2.units:
            raise Exception('Only the same units can be added', unit1, unit2)
        mag1 = unit1.magnitude
        mag2 = unit2.to(unit1.baseunits).magnitude
        mag1.value = np.power(10,mag1.value*unit1.baseunits.magnitude)
        mag2.value = np.power(10,mag2.value*unit2.baseunits.magnitude)
        mag = mag1 + mag2
        mag.value = np.log10(mag.value)/unit1.baseunits.magnitude
        return mag

    def sub(self, unit1, unit2):
        if self.baseunits1.dimensions!=self.baseunits2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        if self.baseunits1.units!=self.baseunits2.units:
            raise Exception('Only the same units can be substracted', unit1, unit2)
        mag1 = unit1.magnitude
        mag2 = unit2.to(unit1.baseunits).magnitude
        mag1.value = np.power(10,mag1.value*unit1.baseunits.magnitude)
        mag2.value = np.power(10,mag2.value*unit2.baseunits.magnitude)
        mag = mag1 - mag2
        mag.value = np.log10(mag.value)/unit1.baseunits.magnitude
        return mag
