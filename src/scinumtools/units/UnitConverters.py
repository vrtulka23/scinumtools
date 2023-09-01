class Converter:

    def __new__(cls, *args):
        obj = object.__new__(cls)
        if method := obj.convert(args[0].baseunits.value(), args[1].baseunits.value()):
            if not hasattr(obj,method):
                raise Exception('Invalid conversion:', symbol1, symbol2)
            obj.method = method
            return obj
        else:
            return None

    def __init__(self, unit1, unit2):
        factor = getattr(self,self.method)(unit1.magnitude, unit2.magnitude)
        unit2.magnitude = unit1.magnitude/factor
        self.unit1 = unit1
        self.unit2 = unit2

class TemperatureConverter(Converter):
    
    def convert(self, baseunits1, baseunits2):
        process: list = ['Cel','degF']
        convert = False
        for unitid, exponent in baseunits1.items():
            if unitid.split(':')[-1] in process:
                convert = True
        for unitid, exponent in baseunits2.items():
            if unitid.split(':')[-1] in process:
                convert = True
        if convert:
            if len(baseunits1)!=1 or len(baseunits2)!=1:
                raise Exception("Only simple units can be converted between each other:", baseunits1, baseunits2)
            symbol1 = list(baseunits1.keys())[0].split(':')[-1]
            symbol2 = list(baseunits2.keys())[0].split(':')[-1]
            return f"convert_{symbol1}_{symbol2}"
        else:
            return False
        
    def convert_K_Cel(self, mag1, mag2):
        return (mag1-273.15)/mag2
        
    def convert_K_degF(self, mag1, mag2):
        return ((mag1-273.15)*9/5+32)/mag2
        
    def convert_degR_degF(self, mag1, mag2):
        return (mag1*9/5-459.67)/mag2
        
    def convert_degR_Cel(self, mag1, mag2):
        return ((mag1*9/5-491.67)*5/9)/mag2
        
    def convert_Cel_K(self, mag1, mag2):
        return (mag1+273.15)/mag2
        
    def convert_Cel_degF(self, mag1, mag2):
        return ((mag1*9/5)+32)/mag2
        
    def convert_Cel_degR(self, mag1, mag2):
        return ((mag1*9/5)+491.67)/(mag2*9/5)
        
    def convert_degF_K(self, mag1, mag2):
        return (((mag1-32)*5/9)+273.15)/mag2
    
    def convert_degF_Cel(self, mag1, mag2):
        return ((mag1-32)*5/9)/mag2
        
    def convert_degF_degR(self, mag1, mag2):
        return (mag1+459.67)/(mag2*9/5)
        
        
class LogarithmicConverter(Converter):

    process: list = ['dBm','dBmW']
    
    def convert(self, magnitude1, magnitude2):
        if symbol1=='dBm' and symbol2=='W':
            return 234
        else:
            raise Exception('Invalid conversion:', symbol1, symbol2)
