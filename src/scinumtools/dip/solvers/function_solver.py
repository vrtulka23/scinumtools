import copy

from ..environment import Environment
from ..settings import Format
from ..datatypes import Type

class FunctionSolver:

    env: Environment

    def __init__(self, env:Environment=None, **kwargs):
        if env:
            self.env = env
        else:
            self.env = Environment()
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass

    def solve(self, fn_name:str, in_units=None):
        fn = self.env.functions[fn_name]
        data = copy.deepcopy(self.env.data(format=Format.TYPE))
        result = fn(data)
        if isinstance(result, Type):
            if in_units:
                result.convert(in_units)
            return result.value
        else:
            return result
