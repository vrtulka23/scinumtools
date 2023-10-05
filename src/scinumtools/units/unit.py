import numpy as np

from .settings import *
from .quantity import Quantity

class Unit:
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
        
    def __new__(cls, unit=None):
        if unit:
            return Quantity(1, unit)
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
        
        def is_baseunit(symbol, unit):
            if unit['definition'] is None:
                return True
            return False
        
        def is_logarithmic(symbol, unit):
            if symbol in ['AR','PR']:
                return True
            if unit['definition'] == LogarithmicUnitType:
                return True
            return False
        
        def is_temperature(symbol, unit):
            if symbol in ['K','Cel', 'degR', 'degF']:
                return True
            return False
            
        def is_constant(symbol, unit):
            if symbol.startswith('['):
                return True
            return False
        
        sw, uw, dw, pw = 8, 20, 20, 15
        text =  "Units\n"
        text += "\nPrefixes:\n\n"
        text += f"{'Symbol':{sw}s} | {'Prefix':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, prefix in UNIT_PREFIXES.items():
            text += f"{symbol:{sw}s} | {prefix['name']:{uw}s} | {prefix['definition']:{dw}s}\n"
        text += "\nBase units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Prefixes':{pw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*pw+"\n"
        for symbol, unit in UNIT_STANDARD.items():
            if not is_baseunit(symbol, unit): continue
            pref = get_pref(unit['prefixes'])
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {pref:{pw}s}\n"         
        text += "\nDerived units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Prefixes':{pw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*pw+"-+-"+"-"*dw+"\n"
        for symbol, unit in UNIT_STANDARD.items():  
            if is_baseunit(symbol, unit): continue
            if is_constant(symbol, unit): continue
            if is_logarithmic(symbol, unit): continue
            if is_temperature(symbol, unit): continue
            pref = get_pref(unit['prefixes'])
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {pref:{pw}s} | {unit['definition']:{dw}s}\n"
        text += "\nTemperature units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, unit in UNIT_STANDARD.items():
            if not is_temperature(symbol, unit): continue
            defn = unit['definition'] if isinstance(unit['definition'],str) else 'temp()'
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {defn:{dw}s}\n"
        text += "\nLogarithmic units:\n\n"
        text += f"{'Symbol':{sw}s} | {'Unit':{uw}s} | {'Definition':{dw}s}\n"
        text += "-"*sw+"-+-"+"-"*uw+"-+-"+"-"*dw+"\n"
        for symbol, unit in UNIT_STANDARD.items():
            if not is_logarithmic(symbol, unit): continue
            defn = unit['definition'] if isinstance(unit['definition'],str) else 'log()'
            text += f"{symbol:{sw}s} | {unit['name']:{uw}s} | {defn:{dw}s}\n"
        return text
    
    @staticmethod
    def list():
        print(Unit._list())
