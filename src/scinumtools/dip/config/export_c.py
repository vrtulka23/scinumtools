import numpy as np

from .export import ExportConfig
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..settings import Sign

class ExportConfigC(ExportConfig):
    
    imports: list
    
    def __init__(self, *args, **kwargs):
        self.includes = []
        super().__init__(*args, **kwargs)

    def include(self, library):
        if library not in self.includes:
            self.includes.append(library)
    
    def _parse_dtype(self, param):
        if isinstance(param, StringType):
            dtype = "char*"
        elif isinstance(param, BooleanType):
            self.include("<stdbool.h>")
            dtype = "bool"
        elif isinstance(param, IntegerType):
            if param.unsigned:
                if param.precision==16:   dtype = "unsigned short int"
                elif param.precision==32: dtype = "unsigned int"
                elif param.precision==64: dtype = "unsigned long long int"
            else:
                if param.precision==8:    dtype = "signed char"
                elif param.precision==16: dtype = "short int"
                elif param.precision==32: dtype = "int"
                elif param.precision==64: dtype = "long long int"
        elif isinstance(param, FloatType):
            if param.precision==32: dtype = "float"
            elif param.precision==64: dtype = "double"
            elif param.precision in [80,96,128]: dtype = "long double"
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
        for value in values:
            if isinstance(value,(np.ndarray,tuple,list)):
                string, shape = self._parse_array(param, value)
            else:
                string, shape = self._parse_scalar(param, value), None
            strings.append( string )
        if shape is None:
            shape = [len(values)]
        else:
            shape = [len(values)]+shape
        return "{" + ", ".join(strings) + "}", shape
        
    def _parse_value(self, param):
        if isinstance(param.value,(np.ndarray,tuple,list)):
            return self._parse_array(param, param.value)
        else:
            return self._parse_scalar(param, param.value), None
    
    def parse_define(self, name, param):
        name = self._rename(name)
        if param.value is None:
            value = ''
        elif isinstance(param, StringType):
            value = "\""+str(param.value)+"\""
        elif isinstance(param, BooleanType):
            value = 1 if param.value else 0
        else:
            value = str(param.value)
        return f"#define {name} {value}"
    
    def parse_const(self, name, param):
        name = self._rename(name)
        dtype = self._parse_dtype(param)
        value, shape = self._parse_value(param)
        if shape is None:
            return f"const {dtype} {name} = {value};"
        else:
            shape = "[" + "][".join(str(s) for s in shape) + "]"
            return f"const {dtype} {name}{shape} = {value};"
    
    def parse(self, guard:str="CONFIG_H", define:tuple=None):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            if define and name in define:
                lines.append(self.parse_define(name, param))
            else:
                lines.append(self.parse_const(name, param))
        lines.append("")
        lines.append(f"#endif /* {guard} */")
        if self.includes:
            lines.insert(3,"")
            for inc in self.includes:
                lines.insert(3,f"#include {inc}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text
    