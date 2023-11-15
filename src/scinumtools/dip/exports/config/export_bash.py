import numpy as np

from .export import ExportConfig
from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign, Format
from ...environment import Environment

class ExportConfigBash(ExportConfig):
    
    def __init__(self, env: Environment, **kwargs):
        if 'dtype' not in kwargs:
            kwargs['dtype'] = Format.VALUE
        super().__init__(env, **kwargs)
        
    def parse_value(self, value):
        if isinstance(value, str):
            value = f"\"{value}\""
        elif isinstance(value, bool):
            value = "0" if value else "-1"   # in bash 0 is true and usually 1, -1 for error
        return value
    
    def parse(self, export=True):
        lines = []
        for name, value in self.data.items():
            name = self._rename(name)
            
            if isinstance(value, (list, np.ndarray)):
                value = "\" \"".join([str(self.parse_value(val)) for val in value])
                value = f"(\"{value}\")"
            else:
                value = self.parse_value(value)

            if export:
                lines.append(f"export {name}={value}")
            else:
                lines.append(f"{name}={value}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text