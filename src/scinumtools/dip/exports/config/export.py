import numpy as np

from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign, EnvType, Format
from ...environment import Environment

class ExportConfig:
    
    env: Environment
    data: dict
    text: str

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, env: Environment, **kwargs):
        if env.envtype != EnvType.DATA:
            raise Exception("Given environment is not a data environment")
        self.env = env
        self.data = self.env.data(Format.TYPE)
    
    def select(self, query:str=None, tags:list=None):
        self.data = self.env.data(Format.TYPE, query=query, tags=tags)
        
    def build_c(self, guard:str="CONFIG_H"):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            name = name.upper().replace(Sign.SEPARATOR,"_")
            value = str(param.value)
            if isinstance(param, StringType):
                value = f"\"{value}\""
            elif isinstance(param, BooleanType):
                value = "1" if param.value else "0"
            lines.append(f"#define {name} {value}")
        lines.append("")
        lines.append(f"#endif /* {guard} */")
        self.text = Sign.NEWLINE.join(lines)
        return self.text
    
    def build_cpp(self, guard="CONFIG_H"):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            name = name.upper().replace(Sign.SEPARATOR,"_")
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
    
    def build_rust(self):
        lines = []
        for name, param in self.data.items():
            name = name.upper().replace(Sign.SEPARATOR,"_")
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

    def build_fortran(self, module:str="ConfigurationModule"):
        lines = []
        lines.append(f"module {module}")
        lines.append("  implicit none")
        lines.append("")
        for name, param in self.data.items():
            name = name.upper().replace(Sign.SEPARATOR,"_")
            value = str(param.value)
            if isinstance(param, StringType):
                value = f"\"{value}\""
                dtype = f"character(len={len(value):d})"
            elif isinstance(param, BooleanType):
                value = ".true." if param.value else ".false."
                dtype = "logical"
            elif isinstance(param, IntegerType):
                if param.precision==16: dtype = "integer(kind=2)"
                elif param.precision==32: dtype = "integer"
                elif param.precision==64: dtype = "integer(kind=8)"
            elif isinstance(param, FloatType):
                if param.precision==32:    dtype = "real"
                elif param.precision==64:  dtype = "real(kind=8)"
            lines.append(f"  {dtype}, parameter :: {name} = {value};")
        lines.append("")
        lines.append(f"end module {module}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text

    def save(self, file_path: str, mode:str = 'w'):
        with open(file_path, mode) as f:
            f.write(self.text)