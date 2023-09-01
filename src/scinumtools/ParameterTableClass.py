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
class ParameterTable:
    """ ParameterDict class collects parameters in a concise form and create a dictionary
    """
    _settings: list
    _keys: list = None
    _data: Union[dict,list] = None

    def __init__(self, settings: list, parameters: Union[list,dict]=None, keys: bool=False):
        self._settings = settings
        if keys:
            self._keys = []
        self._data = [] if self._keys is None else {}
        if parameters:
            if self._keys is None:
                for values in parameters:
                    self.append(values) 
            else:
                for key,values in parameters.items():
                    self.append(key, values)            

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass
    
    def __getitem__(self, key):
        if self._keys is None:
            return self._data[key]
        else:
            if isinstance(key,int):
                return self._data[self._keys[key]]
            else:
                return self._data[key]

    def __setitem__(self, key, values):
        if self._keys is None:
            raise Exception("Cannot set item using a parameter key.")
        else:
            self.append(key, values)

    def keys(self):
        if self._keys is None:
            raise Exception("Parameters do not have keys.")
        else:
            return self._keys
        
    def items(self):
        if self._keys is None:
            return [(key,value) for key,value in enumerate(self._data)]
        else:
            return self._data.items()

    def append(self, *args):
        if self._keys is None:
            values = args[0]
            settings = ParameterSettings(dict(zip(self._settings, values)))
            self._data.append( settings )
        else:
            key, values = args
            if key not in self._keys:
                self._keys.append(key)
            settings = ParameterSettings(dict(zip(self._settings, values)))
            self._data[key] = settings
        