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
        base2 = unit2.baseunits.base()
        unit2.magnitude = getattr(self,self.method)(unit1.magnitude) / base2.magnitude
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

    def convert_K_Cel(self, mag1):
        return mag1-273.15
        
    def convert_K_degF(self, mag1):
        return (mag1-273.15)*9/5+32
        
    def convert_degR_degF(self, mag1):
        return mag1-459.67
        
    def convert_degR_Cel(self, mag1):
        return (mag1-491.67)*5/9
        
    def convert_Cel_K(self, mag1):
        return mag1+273.15
        
    def convert_Cel_degF(self, mag1):
        return (mag1*9/5)+32
        
    def convert_Cel_degR(self, mag1):
        return ((mag1*9/5)+491.67)*5/9
        
    def convert_degF_K(self, mag1):
        return ((mag1-32)*5/9)+273.15
    
    def convert_degF_Cel(self, mag1):
        return (mag1-32)*5/9
        
    def convert_degF_degR(self, mag1):
        return (mag1+459.67)*5/9
        
        
class LogarithmicConverter(Converter):

    def convert(self, baseunits1, baseunits2):
        process: list = ['B','dBm','dBmW']
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

    def convert_B_B(self, mag1):
        return 1
        
