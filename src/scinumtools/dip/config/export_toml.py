import numpy as np
import toml

from .export import ExportConfig
from ..settings import Format
from ..environment import Environment

class ExportConfigTOML(ExportConfig):

    def __init__(self, env: Environment, **kwargs):
        if 'dtype' not in kwargs:
            kwargs['dtype'] = Format.TUPLE
        super().__init__(env, **kwargs)

    def parse(self, units:bool = True, **kwargs):
        data = self.data
        for key in self.data.keys():
            if isinstance(data[key], tuple):
                if units:
                    data[key] = {'value': data[key][0], 'unit':data[key][1]}
                else:
                    data[key] = data[key][0]
        self.text = toml.dumps(data, **kwargs).strip()
        return self.text