from typing import List, Dict, Union
from dataclasses import dataclass, field

from ..settings import Sign
from ...units import Quantity, UnitEnvironment

@dataclass
class UnitList:
    units: Dict   = field(default_factory = dict)  # custom units

    def __len__(self):
        return len(self.units)
    
    def __getitem__(self, key):
        return self.units[key]
    
    def items(self):
        return self.units.items()
    
    def keys(self):
        return self.units.keys()
        
    def append(self, name:str, value:str, units:str, unit:Quantity, source:tuple):
        """ Add a new source

        :param str name: Name of a new unit
        :param Quantity unit: Quantity object
        """
        name = f"[{name}]"
        if name in self.units:
            raise Exception("Reference unit alread exists:", name)
        self.units[name] = {
            'magnitude':  unit.magnitude.value, 
            'dimensions': unit.baseunits.dimensions.value(),
            'value': value, 
            'units': units,
            'source': source,
        } #,'prefixes':['k','M','G']}
        
    def query(self, query:str):
        """ Select units according to a query

        :param str query: unit selection query
        """
        if query==Sign.WILDCARD:   # return all units
            return self.units
        else:                     # return particular unit
            if query not in self.units:
                raise Exception("Requested unit does not exists:", query)
            return {query: self.units[query]}