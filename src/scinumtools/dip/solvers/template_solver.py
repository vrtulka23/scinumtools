import os
from pathlib import Path
import numpy as np
from inspect import getframeinfo, stack

from ..environment import Environment
from ..source import Source
from ..nodes.parser import Parser
from ..datatypes import Type

class TemplateSolver:

    env: Environment
    source: Source

    def __init__(self, env:Environment=None, **kwargs):
        if env:
            self.env = env
        else:
            self.env = Environment()
        if 'source' not in kwargs:
            # determine which file instantiate this class
            caller = getframeinfo(stack()[1][0])
            self.source = Source(lineno=caller.lineno, filename=caller.filename)
        else:
            self.source = kwargs['source']
            
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def solve(self, expr):
        out = ''
        kwargs = {'source':Source(lineno=0, filename='template'), 'keyword':'expr'}
        while len(expr)>0:
            sign, expr = expr[0], expr[1:]
            if sign=='{':
                p = Parser(code=expr, **kwargs)
                p.part_reference()
                p.part_slice()
                p.part_format()
                if p.value_ref and p.ccode[0]=='}':
                    nodes = self.env.request(p.value_ref, count=1)
                    if p.value_slice:
                        value = nodes[0].slice_value(p.value_slice)
                    else:
                        value = nodes[0].value
                    if isinstance(value, Type):
                        value = value.value
                    if p.formating:
                        form = "{0"+p.formating+"}"
                        out += form.format(value)
                    else:
                        out += str(value)
                    expr = p.ccode[1:]
                else:
                    out += sign
            else:
                out += sign
        return out

    def template(self, file_in, file_out=None):
        if not os.path.isabs(file_in):
            # set relative paths with respect to the source script
            parent = Path(self.source.filename).parent
            file_in = parent / file_in
        with open(file_in,'r') as f:
            template = f.read()
        text = self.solve(template)
        if file_out:
            if not os.path.isabs(file_out):
                # set relative paths with respect to the source script
                parent = Path(self.source.filename).parent
                file_out = parent / file_out
            with open(file_out,'w') as f:
                f.write(text)
        return text
            
