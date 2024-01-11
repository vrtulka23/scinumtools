import numpy as np

from .export_c import ExportConfigC
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..settings import Sign

class ExportConfigCPP(ExportConfigC):
    
    def _parse_dtype(self, param):
        if isinstance(param, StringType):
            dtype = "char*"
        elif isinstance(param, BooleanType):
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

    def parse_constexpr(self, name, param):
        name = self._rename(name)
        dtype = self._parse_dtype(param)
        value, shape = self._parse_value(param)
        if shape is None:
            return f"constexpr {dtype} {name} = {value};"
        else:
            shape = "[" + "][".join(str(s) for s in shape) + "]"
            return f"constexpr {dtype} {name}{shape} = {value};"
            
    def parse(self, guard:str="CONFIG_H", define:tuple=None, const:tuple=None):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            if define and name in define:
                lines.append(self.parse_define(name, param))
            elif const and name in const:
                lines.append(self.parse_const(name, param))
            else:
                lines.append(self.parse_constexpr(name, param))
        lines.append("")
        lines.append(f"#endif /* {guard} */")
        if self.includes:
            lines.insert(3,"")
            for inc in self.includes:
                lines.insert(3,f"#include {inc}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text
    