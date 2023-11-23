from typing import List, Union
from dataclasses import dataclass

from ..datatypes import IntegerType, FloatType, StringType
from ..settings import EnvType

@dataclass
class Option:
    value: Union[IntegerType, FloatType, StringType]
    value_raw: str
    units_raw: str

class SelectNode:
    
    options: List = None

    def __init__(self, *args, **kwargs):
        self.options = []

    def validate_options(self):
        """ Check if current value is in option list
        """
        if self.options:
            for option in self.options:
                if option.value==self.value:
                    return True
            else:
                options = [o.value for o in self.options]
                raise Exception(f"Value '{str(self.value)}' of node '{self.name}' doesn't match with any option:", options)
        else: # if there are no options return true
            return True
    
    def set_option(self, node, env):
        """ Set option using value of a different node
        """
        if self.keyword=='int':
            value = IntegerType(self.cast_value(node.value_raw), node.units_raw)
            if env.envtype == EnvType.DOCS:
                value.convert(self.units_raw, env)
        elif self.keyword=='float':
            value = FloatType(self.cast_value(node.value_raw), node.units_raw)
            if not env.envtype == EnvType.DOCS:
                value.convert(self.units_raw, env)
        elif self.keyword=='str':
            value = StringType(self.cast_value(node.value_raw))
        self.options.append(Option(
            value=value,
            value_raw=node.value_raw,
            units_raw=node.units_raw
        ))
