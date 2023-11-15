import numpy as np

from .export import ExportConfig
from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign

class ExportConfigFortran(ExportConfig):

    def parse(self, module:str="ConfigurationModule"):
        lines = []
        lines.append(f"module {module}")
        lines.append("  implicit none")
        lines.append("")
        for name, param in self.data.items():
            name = self._rename(name)
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
                elif param.precision==128:  dtype = "real(kind=16)"
            lines.append(f"  {dtype}, parameter :: {name} = {value};")
        lines.append("")
        lines.append(f"end module {module}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text