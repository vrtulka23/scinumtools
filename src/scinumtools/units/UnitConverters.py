import numpy as np

class Converter:

    def __new__(cls, magnitude1, baseunits1, baseunits2):
        obj = object.__new__(cls)
        if method := obj.method(baseunits1, baseunits2):
            if not hasattr(obj,method[0]):
                raise Exception('Conversion method is not implemented:', method[0])
            obj.method = method
            return obj
        else:
            return None

    def __init__(self, magnitude1, baseunits1, baseunits2):
        base1 = baseunits1.base()
        base2 = baseunits2.base()
        self.magnitude = getattr(self,self.method[0])(magnitude1 * base1.magnitude, *self.method[1:]) / base2.magnitude

class StandardConverter(Converter):
    
    def method(self, baseunits1, baseunits2):
        base1 = baseunits1.base()
        base2 = baseunits2.base()
        if base1.dimensions==base2.dimensions:
            return (f"convert_linear",)
        elif -base1.dimensions==base2.dimensions:
            return (f"convert_inversed",)
        else:
            return False
            
    def convert_inversed(self, value):
        return 1/value

    def convert_linear(self, value):
        return value

class SingleUnitConverter(Converter):

    def method(self, baseunits1, baseunits2):
        baseunits1 = baseunits1.value()
        baseunits2 = baseunits2.value()
        convert = False
        for unitid in baseunits1.keys():
            if unitid.split(':')[-1] in self.process:
                convert = True
        for unitid in baseunits2.keys():
            if unitid.split(':')[-1] in self.process:
                convert = True
        if convert:
            if len(baseunits1)!=1 or len(baseunits2)!=1:
                raise Exception("Only simple units can be converted between each other:",
                                baseunits1, baseunits2)
            symbol1 = list(baseunits1.keys())[0].split(':')[-1]
            symbol2 = list(baseunits2.keys())[0].split(':')[-1]
            return (f"convert_{symbol1}_{symbol2}",)
        else:
            return False

class TemperatureConverter(SingleUnitConverter):
    
    process = ['Cel','degF']
    
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
        
        
class LogarithmicConverter(SingleUnitConverter):

    process: list = ['Np','B','Bm','BmW','BW','BV','BuV']
    
    def method(self, baseunits1, baseunits2):
        conversions = {
            # power ratios
            'convert_PR_B':  ("convert_Ratio_B", 1, 1),
            'convert_B_PR':  ("convert_B_Ratio", 1, 1),
            'convert_W_Bm':  ("convert_Ratio_B", 1, 1),
            'convert_W_BmW': ("convert_Ratio_B", 1, 1),
            'convert_Bm_W':  ("convert_B_Ratio", 1, 1),
            'convert_BmW_W': ("convert_B_Ratio", 1, 1),
            'convert_W_BW':  ("convert_Ratio_B", 1, 1e-3),
            'convert_BW_W':  ("convert_B_Ratio", 1, 1e3),
            # amplitude ratios
            'convert_AR_B':  ("convert_Ratio_B", 2, 1),
            'convert_B_AR':  ("convert_B_Ratio", 2, 1),
            'convert_V_BV':  ("convert_Ratio_B", 2, 1e-3),
            'convert_BV_V':  ("convert_B_Ratio", 2, 1e3),
            'convert_V_BuV': ("convert_Ratio_B", 2, 1e3),
            'convert_BuV_V': ("convert_B_Ratio", 2, 1e-3),
        }
        method = super().method(baseunits1, baseunits2)
        if method and method[0] in conversions:
            return conversions[method[0]]
        else:
            return method

    def convert_B_B(self, value):
        return value
        
    def convert_B_Np(self, value):
        return 1.151277918*value
        
    def convert_Np_B(self, value):
        return value/1.151277918
        
    def convert_Ratio_B(self, value, exp, conv):
        return exp*np.log10(value*conv)
        
    def convert_B_Ratio(self, value, exp, conv):
        return np.power(10,value/exp)*conv
        