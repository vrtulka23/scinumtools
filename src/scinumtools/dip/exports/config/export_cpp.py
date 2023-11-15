import numpy as np

from .export import ExportConfig
from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign

class ExportConfigCPP(ExportConfig):
    
    def parse(self, guard="CONFIG_H"):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            name = self._rename(name)
            value = str(param.value)
            if isinstance(param, StringType):
                value = f"\"{value}\""
                dtype = "const char*"
            elif isinstance(param, BooleanType):
                value = "true" if param.value else "false"
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
            lines.append(f"constexpr {dtype} {name} = {value};")
        lines.append("")
        lines.append(f"#endif /* {guard} */")
        self.text = Sign.NEWLINE.join(lines)
        return self.text