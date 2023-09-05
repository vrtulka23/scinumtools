import numpy as np

class Converter:

    def __new__(cls, *args):
        obj = object.__new__(cls)
        if method := obj.convert(args[0].baseunits.value(), args[1].baseunits.value()):
            if not hasattr(obj,method):
                raise Exception('Conversion method is not implemented:', method)
            obj.method = method
            return obj
        else:
            return None

    def __init__(self, unit1, unit2):
        base1 = unit1.baseunits.base()
        base2 = unit2.baseunits.base()
        unit2.magnitude = getattr(self,self.method)(unit1.magnitude * base1.magnitude) / base2.magnitude 
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
            return f"convert_{symbol1}_{symbol2}"
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
        process: list = ['Np','B','Bm','BmW']
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
            return f"convert_{symbol1}_{symbol2}"
        else:
            return False

    def convert_B_B(self, value):
        return value
        
    def convert_B_Np(self, value):
        return 1.151277918*value
        
    def convert_Np_B(self, value):
        return value/1.151277918
        
    def convert_AR_B(self, value):
        return 2*np.log10(value)
        
    def convert_B_AR(self, value):
        return np.power(10,value/2)
        
    def convert_PR_B(self, value):
        return np.log10(value)
        
    def convert_B_PR(self, value):
        return np.power(10,value)
        
    def convert_W_Bm(self, value):
        print(value)
        return np.log10(value*1e-3)