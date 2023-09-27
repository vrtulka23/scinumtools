from .settings import *
from .quantity import Quantity

def check_unique_symbols():   
    units = list(UNIT_STANDARD.keys())
    for symbol, unit in UNIT_STANDARD.items():
        if isinstance(unit.prefixes, list):
            for prefix in unit.prefixes:
                assert prefix in UNIT_PREFIXES
                units.append(f"{prefix}{symbol}")
        elif unit.prefixes is True:
            for prefix in UNIT_PREFIXES.keys():
                units.append(f"{prefix}{symbol}")
    #print(units)
    #exit(1)
    units.sort()
    seen = set()
    dupes = [x for x in units if x in seen or seen.add(x)]    
    if len(dupes)==0:
        return True
    else:
        raise Exception("Following unit symbols are duplicated:", dupes)
    
class UnitEnvironment:
    
    new_units: list
    new_types: list
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
    
    def __init__(self, units):
        self.new_units = []
        self.new_types = []
        for symbol, unit in units.items():
            if isinstance(unit, Quantity):
                unit = {'magnitude':unit.magnitude.value*unit.baseunits.magnitude, 'dimensions':unit.baseunits.dimensions.value(dtype=list)}
            if symbol in UNIT_STANDARD:
                raise Exception("Unit with this symbol already exists:", symbol)
            if 'name' not in unit:
                unit['name'] = symbol
            if 'definition' not in unit:
                unit['definition']=None
            elif unit['definition'] is not None:
                if not isinstance(unit['definition'], str) and unit['definition'] not in UNIT_TYPES:
                    UNIT_TYPES.insert(0, unit['definition'])
                    self.new_types.append(unit['definition'])
            if 'prefixes' not in unit:
                unit['prefixes'] = False
            UNIT_STANDARD.append(symbol, (unit['magnitude'], unit['dimensions'], unit['definition'], unit['name'], unit['prefixes']))
            self.new_units.append(symbol)
        check_unique_symbols()
        
    def close(self):
        for unit in self.new_units:
            del UNIT_STANDARD[unit]
        for utype in self.new_types:
            UNIT_TYPES.remove(utype)
        
        
    