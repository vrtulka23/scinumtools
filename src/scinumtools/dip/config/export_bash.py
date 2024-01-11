import numpy as np

from .export import ExportConfig
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..settings import Sign, Format
from ..environment import Environment

class ExportConfigBash(ExportConfig):
    
    def __init__(self, env: Environment, **kwargs):
        if 'dtype' not in kwargs:
            kwargs['dtype'] = Format.VALUE
        super().__init__(env, **kwargs)
        
    def _parse_scalar(self, value):
        if value is None:
            value = ''
        elif isinstance(value, str):
            value = f"\"{value}\""
        elif isinstance(value, bool):
            value = "0" if value else "-1"   # in bash 0 is true and usually 1, -1 for error
        return value
    
    def _parse_array(self, name, values, coord):
        strings = []
        for v, value in enumerate(values):
            if isinstance(value,(np.ndarray,tuple,list)):
                string, shape = self._parse_array(name, value, coord+[v])
            else:
                string, shape = self._parse_scalar(value), None
            strings.append( string )
        if shape is None:
            shape = [len(values)]
            if len(coord):
                dims = ",".join(str(d) for d in coord)
                strings = [f"{name}[{dims},{v}]={val}" for v,val in enumerate(strings)]
        else:
            shape = [len(values)]+shape
        if len(coord)==0 and len(shape)==1:
            return "(" + " ".join(f"\"{val}\"" for val in strings) + ")", shape
        else:
            return "\n".join(str(val) for val in strings), shape
    
    def parse(self, export=True):
        lines = []
        for name, value in self.data.items():
            name = self._rename(name)
            
            if isinstance(value, (list, tuple, np.ndarray)):
                value, size = self._parse_array(name, value, [])
            else:
                value, size = self._parse_scalar(value), None
            export = 'export ' if export else ''
            if size and len(size)>1:
                lines.append(f"declare -A {name}\n{value}")
                if export:
                    lines.append(f"export {name}")
            else:
                lines.append(f"{export}{name}={value}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text