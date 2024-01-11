import numpy as np

from .export import ExportConfig
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..settings import Sign

class ExportConfigFortran(ExportConfig):

    def _parse_dtype(self, param, value):
        if isinstance(param, StringType):
            dtype = f"character(len={len(value):d})"
        elif isinstance(param, BooleanType):
            dtype = "logical"
        elif isinstance(param, IntegerType):
            if param.precision==16: dtype = "integer(kind=2)"
            elif param.precision==32: dtype = "integer"
            elif param.precision==64: dtype = "integer(kind=8)"
        elif isinstance(param, FloatType):
            if param.precision==32:    dtype = "real"
            elif param.precision==64:  dtype = "real(kind=8)"
            elif param.precision==128:  dtype = "real(kind=16)"
        return dtype

    def _parse_scalar(self, param, value):
        if isinstance(param, StringType):
            value = f"\"{str(value)}\""
        elif isinstance(param, BooleanType):
            value = ".true." if value else ".false."
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
        return ", ".join(strings), shape
        
    def _parse_value(self, param, value):
        if isinstance(value,(np.ndarray,tuple,list)):
            return self._parse_array(param, value)
        else:
            return self._parse_scalar(param, value), None

    def parse(self, module:str="ConfigurationModule"):
        lines = []
        lines.append(f"module {module}")
        lines.append("  implicit none")
        lines.append("")
        for name, param in self.data.items():
            name = self._rename(name)
            value, shape = self._parse_value(param, param.value)
            dtype = self._parse_dtype(param, value)
            if shape is None:
                lines.append(f"  {dtype}, parameter :: {name} = {value};")
            else:
                if len(shape)>1:
                    dims = ",".join(str(s) for s in shape)
                    lines.append(f"  {dtype}, dimension ({dims}), parameter :: {name} = reshape([{value}],[{dims}])")
                else:
                    shape = ",".join(str(s) for s in shape)
                    lines.append(f"  {dtype}, dimension ({shape}) :: {name} = [{value}];")
        lines.append("")
        lines.append(f"end module {module}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text