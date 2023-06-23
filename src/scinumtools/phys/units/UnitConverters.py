class TemperatureConverter:
    convertable: bool = False
    unit1: dict = None
    unit2: dict = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, baseunits1, baseunits2):
        convertable = ['Cel','[degF]']
        for unitid, exponent in baseunits1.items():
            if unitid.split(':')[-1] in convertable:
                self.convertable = True
        for unitid, exponent in baseunits2.items():
            if unitid.split(':')[-1] in convertable:
                self.convertable = True
        if self.convertable:
            if len(baseunits1)!=1 or len(baseunits2)!=1:
                raise Exception("Only direct temperatures can be converted between each other:", baseunits1, baseunits2)
            else:
                self.unit1 = list(baseunits1.keys())[0].split(':')[-1]
                self.unit2 = list(baseunits2.keys())[0].split(':')[-1]
                
    def convert(self, magnitude1, magnitude2):
        if self.unit1=='K' and self.unit2=='Cel':
            return (magnitude1-273.15)/magnitude2
        elif self.unit1=='K' and self.unit2=='[degF]':
            return ((magnitude1-273.15)*9/5+32)/magnitude2
        elif self.unit1=='[degR]' and self.unit2=='[degF]':
            return (magnitude1*9/5-459.67)/magnitude2
        elif self.unit1=='[degR]' and self.unit2=='Cel':
            return ((magnitude1*9/5-491.67)*5/9)/magnitude2
        elif self.unit1=='Cel' and self.unit2=='K':
            return (magnitude1+273.15)/magnitude2
        elif self.unit1=='Cel' and self.unit2=='[degF]':
            return ((magnitude1*9/5)+32)/magnitude2
        elif self.unit1=='Cel' and self.unit2=='[degR]':
            return ((magnitude1*9/5)+491.67)/(magnitude2*9/5)
        elif self.unit1=='[degF]' and self.unit2=='K':
            return (((magnitude1-32)*5/9)+273.15)/magnitude2
        elif self.unit1=='[degF]' and self.unit2=='Cel':
            return ((magnitude1-32)*5/9)/magnitude2
        elif self.unit1=='[degF]' and self.unit2=='[degR]':
            return (magnitude1+459.67)/(magnitude2*9/5)
