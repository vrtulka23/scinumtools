import numpy as np

from .export import ExportConfig
from ...datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ...settings import Sign

class ExportConfigC(ExportConfig):
    
    def parse(self, guard:str="CONFIG_H"):
        lines = []
        lines.append(f"#ifndef {guard}")
        lines.append(f"#define {guard}")
        lines.append("")
        for name, param in self.data.items():
            name = self._rename(name)
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
    