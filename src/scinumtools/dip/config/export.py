import numpy as np

from ..settings import Sign, EnvType, Format
from ..datatypes import StringType, BooleanType, NumberType, FloatType, IntegerType
from ..nodes import StringNode, BooleanNode, FloatNode, IntegerNode
from ..environment import Environment

class ExportConfig:
    
    env: Environment
    data: dict
    dtype: Format
    rename: bool
    text: str

    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, env: Environment, **kwargs):
        """ Initialize export
        :param Environment env: DIP environment that should be exported
        :param Format dtype: DIP data format 
        """
        if env.envtype != EnvType.DATA:
            raise Exception("Given environment is not a data environment")
        self.env = env
        self.dtype = kwargs['dtype'] if 'dtype' in kwargs else Format.TYPE
        self.rename = kwargs['rename'] if 'rename' in kwargs else True
        self.data = self.env.data(self.dtype)
    
    def _rename(self, name):
        """ Internal routine that renames parameter names into a proper format
        """
        if self.rename:
            return name.upper().replace(Sign.SEPARATOR,"_")
        else:
            return name
    
    def select(self, query:str=None, tags:list=None):
        """ Select nodes from an environment
        :param str query: Node query string
        :param list tags: List of tag selectors
        """
        self.data = self.env.data(self.dtype, query=query, tags=tags)

    def parse(self):
        """ Default DIP parser
        """
        lines = []
        for name, param in self.data.items():
            value = param.value
            if isinstance(param, StringType):
                dtype = StringNode.keyword
                value = f"\"{value}\""
            elif isinstance(param, BooleanType):
                dtype = BooleanNode.keyword
                value = "true" if value else "false"
            elif isinstance(param, IntegerType):
                dtype = IntegerNode.keyword
                if param.unsigned:
                    dtype = "u"+dtype
                if param.precision!=IntegerType.precision:
                    dtype += str(param.precision)
                value = int(param.value)
            elif isinstance(param, FloatType):
                dtype = FloatNode.keyword
                if param.precision!=FloatType.precision:
                    dtype += str(param.precision)
                value = float(param.value)
            if param.unit:
                lines.append(f"{name} {dtype} = {value} {param.unit}")
            else:
                lines.append(f"{name} {dtype} = {value}")
        self.text = Sign.NEWLINE.join(lines)
        return self.text

    def save(self, file_path: str, mode:str = 'w'):
        """ Save parsed text into a file
        """
        with open(file_path, mode) as f:
            f.write(self.text)