import numpy as np

from .export import ExportConfig
from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign

class ExportConfigRust(ExportConfig):
    
    def parse(self):
        lines = []
        for name, param in self.data.items():
            name = self._rename(name)
            value = str(param.value)
            if isinstance(param, StringType):
                value = f"\"{value}\""
                dtype = "&str"
            elif isinstance(param, BooleanType):
                value = "true" if param.value else "false"
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
                elif param.precision==128: dtype = "f128"
            lines.append(f"pub const {name}: {dtype} = {value};")
        self.text = Sign.NEWLINE.join(lines)
        return self.text
