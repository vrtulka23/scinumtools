import numpy as np

from .MagnitudeClass import Magnitude

class UnitType:

    def __new__(cls, base1, base2):
        obj = object.__new__(cls)
        obj.base1 = base1
        obj.base2 = base2
        if obj._istype():
            return obj
        else:
            return None
            
    def convert(self, magnitude1):
        if not hasattr(self, self.conversion[0]):
                raise Exception('Conversion method is not implemented:', self.conversion[0])
        return Magnitude(
            getattr(self, self.conversion[0])(magnitude1.value * self.base1.magnitude, *self.conversion[1:]) / self.base2.magnitude,
            magnitude1.error
        )
        
    def add(self, unit1, unit2):
        if self.base1.dimensions!=self.base2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        return unit1.magnitude + unit2.to(unit1.baseunits).magnitude

    def substract(self, unit1, unit2):
        if self.base1.dimensions!=self.base2.dimensions:
            raise Exception('Only units with the same dimension can added together', unit1, unit2)
        return unit1.magnitude - unit2.to(unit1.baseunits).magnitude

class StandardUnitType(UnitType):

    def _istype(self):
        if self.base1.dimensions==self.base2.dimensions:
            self.conversion = (f"convert_linear",)
        elif -self.base1.dimensions==self.base2.dimensions:
            self.conversion = (f"convert_inversed",)
        else:
            return False
        return True

    def convert_inversed(self, value):
        return 1/value

    def convert_linear(self, value):
        return value

class TemperatureUnitType(UnitType):
    
    process = ['Cel','degF']
    
    def _istype(self):
        if np.any(np.in1d(self.base1.units+self.base2.units, self.process)):
            if len(self.base1.units)!=1 or len(self.base2.units)!=1:
                raise Exception("Only simple units can be converted between each other:",
                                self.base1.units, self.base2.units)
            self.conversion = (f"convert_{self.base1.units[0]}_{self.base2.units[0]}",)
        else:
            return False
        return True
    
    def convert_K_Cel(self, value):
        return value-273.15
        
    def convert_K_degF(self, value):
        return (value-273.15)*9/5+32
        
    def convert_degR_degF(self, value):
        return value*9/5-459.67
        
    def convert_degR_Cel(self, value):
        return (value*9/5-491.67)*5/9
        
    def convert_Cel_K(self, value):
        return value+273.15
        
    def convert_Cel_degF(self, value):
        return (value*9/5)+32
        
    def convert_Cel_degR(self, value):
        return ((value*9/5)+491.67)*5/9
        
    def convert_degF_K(self, value):
        return ((value-32)*5/9)+273.15
    
    def convert_degF_Cel(self, value):
        return (value-32)*5/9
        
    def convert_degF_degR(self, value):
        return (value+459.67)*5/9
        
        
class LogarithmicUnitType(UnitType):

    process: list = ['Np','B','Bm','BmW','BW','BV','BuV','BuA','BOhm','BSPL','BSIL','BSWL']
    conversions: dict = {
        # power ratios
        'PR_Np':    ("convert_Ratio_Np",  0.5, 1),    # Nepers
        'Np_PR':    ("convert_Np_Ratio",  0.5, 1),
        'PR_B':     ("convert_Ratio_B",   1,   1),    # Bel
        'B_PR':     ("convert_B_Ratio",   1,   1),
        'W_Bm':     ("convert_Ratio_B",   1,   1),
        'W_BmW':    ("convert_Ratio_B",   1,   1),
        'Bm_W':     ("convert_B_Ratio",   1,   1),
        'BmW_W':    ("convert_B_Ratio",   1,   1),
        'W_BW':     ("convert_Ratio_B",   1,   1e-3),
        'BW_W':     ("convert_B_Ratio",   1,   1e3),
        'W_BSIL':   ("convert_Ratio_B",   1,   1e9),  # W/m2
        'BSIL_W':   ("convert_B_Ratio",   1,   1e-9),
        'W_BSWL':   ("convert_Ratio_B",   1,   1e9),  # W
        'BSWL_W':   ("convert_B_Ratio",   1,   1e-9),
        # amplitude ratios
        'AR_Np':    ("convert_Ratio_Np",  1,   1),    # Nepers
        'Np_AR':    ("convert_Np_Ratio",  1,   1),
        'AR_B':     ("convert_Ratio_B",   2,   1),    # Bel
        'B_AR':     ("convert_B_Ratio",   2,   1),
        'V_BV':     ("convert_Ratio_B",   2,   1e-3),
        'BV_V':     ("convert_B_Ratio",   2,   1e3),
        'V_BuV':    ("convert_Ratio_B",   2,   1e3),
        'BuV_V':    ("convert_B_Ratio",   2,   1e-3),
        'A_BuA':    ("convert_Ratio_B",   2,   1e6),
        'BuA_A':    ("convert_B_Ratio",   2,   1e-6),
        'Ohm_BOhm': ("convert_Ratio_B",   2,   1e-3),
        'BOhm_Ohm': ("convert_B_Ratio",   2,   1e3),
        'Pa_BSPL':  ("convert_Ratio_B",   2,   50),
        'BSPL_Pa':  ("convert_B_Ratio",   2,   0.02),
        # decibel conversions
        'BW_Bm':    ("convert_B_B",       3),
        'Bm_BW':    ("convert_B_B",      -3),
        'BW_BmW':   ("convert_B_B",       3),
        'BmW_BW':   ("convert_B_B",      -3),
        'Bm_BmW':   ("convert_B_B",       0),
        'BmW_Bm':   ("convert_B_B",       0),
        'BV_BuV':   ("convert_B_B",       12),
        'BuV_BV':   ("convert_B_B",      -12),
    }
    
    def _istype(self):
        if np.any(np.in1d(self.base1.units+self.base2.units, self.process)):
            if len(self.base1.units) not in [1,2] or len(self.base2.units) not in [1,2]:
                raise Exception("Only simple and fraction units can be converted between each other:",
                                self.base1.units, self.base2.units)
            conversion = f"{self.base1.units[0]}_{self.base2.units[0]}"
            if conversion in self.conversions:
                self.conversion = self.conversions[conversion]
            else:
                self.conversion = (f"convert_{conversion}",)
        else:
            return False
        return True
    
    def convert_B_B(self, value, exp=0):
        return value + exp
        
    def convert_B_Np(self, value):
        return 1.151277918*value
        
    def convert_Np_B(self, value):
        return value/1.151277918
        
    def convert_Ratio_B(self, value, exp, conv):
        return exp*np.log10(value*conv)
        
    def convert_B_Ratio(self, value, exp, conv):
        return np.power(10,value/exp)*conv
        
    def convert_Ratio_Np(self, value, exp, conv):
        return exp*np.log(value*conv)
        
    def convert_Np_Ratio(self, value, exp, conv):
        return np.exp(value/exp)*conv
        