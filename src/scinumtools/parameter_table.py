from dataclasses import dataclass, field
import pandas as pd
from typing import Union

class ParameterSettings:
    """ ParameterSettings class contain all settings of a parameter
    """
    
    _keys: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, tb):
        pass

    def __getitem__(self, key):
        return getattr(self,key)
    
    def __init__(self, settings):
        self._keys = []
        for key,value in settings.items():
            self._keys.append(key)
            setattr(self,key,value)
            
    def _to_string(self):
        settings = []
        for key in self._keys:
            value = str(getattr(self, key))
            settings.append(f"{key}={value}")
        settings = " ".join(settings)
        return f"ParameterSettings({settings})"
    def __str__(self):
        return self._to_string()
    def __repr__(self):
        return self._to_string()
    def keys(self):
        return self._keys
    def items(self):
        settings = []
        for key in self._keys:
            yield key, getattr(self, key)
    def data(self):
        return {k:v for k,v in self.items()}        

@dataclass
class ParameterTable:
    """ ParameterDict class collects parameters in a concise form and create a dictionary
    """
    _settings: list
    _keys: list = None
    _keyname: str = None
    _data: Union[dict,list] = None

    def __init__(self, settings: list, parameters: Union[list,dict]=None, keys: bool=False, keyname: str="#"):
        self._settings = settings
        if keys:
            self._keys = []
            self._keyname = keyname
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

    def __getattr__(self, key):
        if self._keys is None:
            raise Exception("Cannot access parameters using a parameter key.")
        else:   
            return self._data[key]

    def __delitem__(self, index):
        if self._keys is None:
            del self._data[index]
        else:
            self._keys.remove(index)
            del self._data[index]
        
    def __len__(self):
        return len(self._data)
        
    def __contains__(self, item):
        if self._keys is None:
            raise Exception("Parameter table does not have string keys")
        else:
            return item in self._keys

    def shape(self):
        return (len(self._data), len(self._settings))
    
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
        
    def data(self):
        if self._keys is None:
            return [v.data() for k,v in self.items()]
        else:
            return {k:v.data() for k,v in self.items()}
            
    def to_dataframe(self):
        if self._keys is None:
            df = pd.DataFrame(columns=self._settings)
            for v in self.data():
                df.loc[len(df.index)] = v.values()
        else:
            df = pd.DataFrame(columns=[self._keyname]+self._settings)
            for k,v in self.data().items():
                df.loc[len(df.index)] = [k]+list(v.values())
        return df
        
    def to_text(self, **kwargs):
        return self.to_dataframe().to_string(**kwargs)
