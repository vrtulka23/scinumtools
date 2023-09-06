import numpy as np

class Converter:

    def __new__(cls, *args):
        obj = object.__new__(cls)
        if method := obj.convert(args[0].baseunits.value(), args[1].baseunits.value()):
            if not hasattr(obj,method[0]):
                raise Exception('Conversion method is not implemented:', method[0])
            obj.method = method
            return obj
        else:
            return None

    def __init__(self, unit1, unit2):
        base1 = unit1.baseunits.base()
        base2 = unit2.baseunits.base()
        unit2.magnitude = getattr(self,self.method[0])(unit1.magnitude * base1.magnitude, *self.method[1:]) / base2.magnitude
        self.unit = unit2

class TemperatureConverter(Converter):
    
    def convert(self, baseunits1, baseunits2):
        process: list = ['Cel','degF']
        convert = False
        for unitid in baseunits1.keys():
            if unitid.split(':')[-1] in process:
                convert = True
        for unitid in baseunits2.keys():
            if unitid.split(':')[-1] in process:
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
        
        
class LogarithmicConverter(Converter):

    def convert(self, baseunits1, baseunits2):
        process: list = ['Np','B','Bm','BmW','BW','BV','BuV']
        convert = False
        for unitid, exponent in baseunits1.items():
            if unitid.split(':')[-1] in process:
                convert = True
        for unitid, exponent in baseunits2.items():
            if unitid.split(':')[-1] in process:
                convert = True
        if convert:
            if len(baseunits1)!=1 or len(baseunits2)!=1:
                raise Exception("Only simple units can be converted between each other:",
                                baseunits1, baseunits2)
            symbol1 = list(baseunits1.keys())[0].split(':')[-1]
            symbol2 = list(baseunits2.keys())[0].split(':')[-1]
            convert = f"{symbol1}_{symbol2}"
            conversions = {
                # power ratios
                'PR_B':  ("convert_Ratio_B", 1, 1),
                'B_PR':  ("convert_B_Ratio", 1, 1),
                'W_Bm':  ("convert_Ratio_B", 1, 1),
                'W_BmW': ("convert_Ratio_B", 1, 1),
                'Bm_W':  ("convert_B_Ratio", 1, 1),
                'BmW_W': ("convert_B_Ratio", 1, 1),
                'W_BW':  ("convert_Ratio_B", 1, 1e-3),
                'BW_W':  ("convert_B_Ratio", 1, 1e3),
                # amplitude ratios
                'AR_B':  ("convert_Ratio_B", 2, 1),
                'B_AR':  ("convert_B_Ratio", 2, 1),
                'V_BV':  ("convert_Ratio_B", 2, 1e-3),
                'BV_V':  ("convert_B_Ratio", 2, 1e3),
                'V_BuV': ("convert_Ratio_B", 2, 1e3),
                'BuV_V': ("convert_B_Ratio", 2, 1e-3),
            }
            if convert in conversions:
                return conversions[convert]
            else:
                return (f"convert_{convert}",)
        else:
            return False

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
        