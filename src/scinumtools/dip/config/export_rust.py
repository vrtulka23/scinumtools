import numpy as np

from .export import ExportConfig
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..settings import Sign

class ExportConfigRust(ExportConfig):
    
    def _parse_dtype(self, param, value):
        if isinstance(param, StringType):
            dtype = "&str"
        elif isinstance(param, BooleanType):
            dtype = "bool"
        elif isinstance(param, IntegerType):
            if param.unsigned:
                if param.precision==8:    dtype = "u8"
                elif param.precision==16: dtype = "u16"
                elif param.precision==32: dtype = "u32"
                elif param.precision==64: dtype = "u64"
            else:
                if param.precision==8:    dtype = "i8"
                elif param.precision==16: dtype = "i16"
                elif param.precision==32: dtype = "i32"
                elif param.precision==64: dtype = "i64"
        elif isinstance(param, FloatType):
            if param.precision==32:    dtype = "f32"
            elif param.precision==64:  dtype = "f64"
            elif param.precision==128: dtype = "f64"  # f128 is not supported yet
        return dtype
    
    def _parse_scalar(self, param, value):
        if isinstance(param, StringType):
            value = f"\"{value}\""
        elif isinstance(param, BooleanType):
            value = "true" if value else "false"
        elif isinstance(param, IntegerType):
            value = str(value)
        elif isinstance(param, FloatType):
            value = str(value)
        return value
    
    def _parse_array(self, param, values):
        strings = []
        for v, value in enumerate(values):
            if isinstance(value,(np.ndarray,tuple,list)):
                string, shape = self._parse_array(param, value)
            else:
                string, shape = self._parse_scalar(param, value), None
            strings.append( string )
        if shape is None:
            shape = [len(values)]
        else:
            shape = [len(values)]+shape
        return "[" + ", ".join(strings) + "]", shape
        
    def _parse_value(self, param, value):
        if isinstance(value,(np.ndarray,tuple,list)):
            return self._parse_array(param, value)
        else:
            return self._parse_scalar(param, value), None
            
    def parse(self):
        lines = []
        for name, param in self.data.items():
            name = self._rename(name)
            value, size = self._parse_value(param, param.value)
            dtype = self._parse_dtype(param, param.value)
            if size is not None:
                size.reverse()
                for dim in size:
                    dtype = f"[{dtype}; {dim}]"
            lines.append(f"pub const {name}: {dtype} = {value};")
        self.text = Sign.NEWLINE.join(lines)
        return self.text
