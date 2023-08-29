import numpy as np

from .UnitList import UnitStandard, UnitPrefixes
from .QuantityClass import Quantity
from ..ParameterClass import ParameterTable

class Unit:
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def __new__(cls, unit=None):
        if unit:
            return Quantity(1,str(unit))
        else:
            return object.__new__(cls)
    
    def __getattr__(self, unit):
        return Quantity(1,str(unit))
        
    def __str__(self):
        return Unit._list()

    def __rep__(self):
        return Unit._list()

    @staticmethod
    def _list():
        def get_pref(prefixes):
            if isinstance(prefixes,list):
                return ", ".join(prefixes)
            elif prefixes is True:
                return 'all'
            else:
                return ''
        
        unitlist = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitStandard, keys=True)
        prefixes = ParameterTable(['magnitude','dimensions','definition','name','prefixes'], UnitPrefixes, keys=True)
        sw, uw, dw, pw = 8, 20, 20, 15
        text =  "Units\n"
        text += "\nPrefixes:\n\n"
        text += f"{'Symbol':{sw}s} | {'Prefix':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, prefix in prefixes.items():
            text += f"{symbol:{sw}s} | {prefix['name']:{uw}s} | {prefix['definition']:{dw}s}\n"
        text += "\nBase units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Prefixes':{pw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*pw+"\n"
        for symbol, unit in unitlist.items():
            if not symbol.startswith('[') and unit['definition'] is None:
                pref = get_pref(unit['prefixes'])
                text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {pref:{pw}s}\n"         
        text += "\nDerived units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Prefixes':{pw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*pw+"-+-"+"-"*dw+"\n"
        for symbol, unit in unitlist.items():
            if symbol.startswith('['): continue
            if not isinstance(unit['definition'], str): continue
            if symbol=='degR': continue
            pref = get_pref(unit['prefixes'])
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {pref:{pw}s} | {unit['definition']:{dw}s}\n"
        text += "\nTemperature units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, unit in unitlist.items():
            if symbol not in ['Cel', 'degR', 'degF']:
                continue
            defn = unit['definition'] if isinstance(unit['definition'],str) else 'fn(K)'
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {defn:{dw}s}\n"
        return text
    
    @staticmethod
    def list():
        print(Unit._list())
