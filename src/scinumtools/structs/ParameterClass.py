from dataclasses import dataclass
from typing import Union

@dataclass
class ParameterSettings:
    """ ParameterSettings class contain all settings of a parameter
    """
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass

    def __getitem__(self, key):
        return getattr(self,key)
    
    def __init__(self, settings):
        for key,value in settings.items():
            setattr(self,key,value)

@dataclass
class ParameterList:
    """ ParameterList class collects parameters in a concise form and create a list
    """
    
    _settings: list
    _data: list

    def __init__(self, settings: list, parameters: list=None):
        self._settings = settings
        self._data = []
        if parameters:
            for values in parameters:
                self.append(values)            

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __getitem__(self, key):
        return self._data[key]
    
    def append(self, values: list): 
        if self._data is None:
            self._data = []
        settings = ParameterSettings(dict(zip(self._settings, values)))
        self._data.append( settings )

    def items(self):
        return [(key,value) for key,value in enumerate(self._data)]

@dataclass
class ParameterDict:
    """ ParameterDict class collects parameters in a concise form and create a dictionary
    """
    _keys: list
    _settings: list
    _data: dict

    def __init__(self, settings: list, parameters: dict=None):
        self._settings = settings
        self._data = {}
        self._keys = []
        if parameters:
            for key,values in parameters.items():
                self.append(key, values)            

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __getitem__(self, key):
        if isinstance(key,int):
            return self._data[self._keys[key]]
        else:
            return self._data[key]

    def __setitem__(self, key, values):
        self.append(key, values)

    def keys(self):
        return self._keys
        
    def items(self):
        return self._data.items()

    def append(self, key, values):
        if self._data is None:
            self._data = {}
        settings = ParameterSettings(dict(zip(self._settings, values)))
        self._keys.append(key)
        self._data[key] = settings
        
