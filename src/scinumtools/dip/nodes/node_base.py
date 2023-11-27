import numpy as np
import json
import re

from .node import Node
from ..datatypes import Type, NumberType, IntegerType, FloatType, StringType, BooleanType
from ..environment import Environment
from ..settings import Keyword, Sign, EnvType

class BaseNode(Node):
    
    value: str = None       # Value
    constant: bool = False
    condition: str = None
    branch_id: int = None
    case_id: int = None
    
    def __init__(self, parser=None, *args, **kwargs):
        if parser:
            kwargs['code'] = parser.code
            kwargs['source'] = parser.source
            kwargs['indent'] = parser.indent
            kwargs['name'] = parser.name
            kwargs['dtype_prop'] = parser.dtype_prop
            kwargs['value_raw'] = parser.value_raw
            kwargs['value_ref'] = parser.value_ref
            kwargs['value_slice'] = parser.value_slice
            kwargs['units_raw'] = parser.units_raw
            kwargs['dimension'] = parser.dimension
            kwargs['defined'] = parser.defined
            if parser.keyword:
                kwargs['keyword'] = parser.keyword
            if parser.value_fn:
                kwargs['value_fn'] = parser.value_fn
            if parser.value_expr:
                kwargs['value_expr'] = parser.value_expr
        super().__init__(*args, **kwargs)
    
    def __str__(self):
        class_name = self.__class__.__name__.replace('Node','')
        node_name = (self.name.split('.'))[-1]
        if isinstance(self.value, NumberType) and self.value.unit:
            return f"{class_name}({node_name}: {self.value.value} {self.value.unit})"
        elif isinstance(self.value, Type):
            return f"{class_name}({node_name}: {self.value.value})"
        else:
            return f"{class_name}({node_name}: {self.value})"
    
    def __repr__(self):
        class_name = self.__class__.__name__.replace('Node','')
        node_name = (self.name.split('.'))[-1]
        if isinstance(self.value, NumberType) and self.value.unit:
            return f"{class_name}({node_name}: {self.value.value} {self.value.unit})"
        elif isinstance(self.value, Type):
            return f"{class_name}({node_name}: {self.value.value})"
        else:
            return f"{class_name}({node_name}: {self.value})"

    def parse(self, env):
        return False

    def clean_name(self):
        """ Strip @case and @else from the name
        """
        pattern = f"{Sign.CONDITION}[0-9]+{Sign.SEPARATOR}"
        return re.sub(pattern, '', self.name)

    def cast_value(self, value=None):
        """ Cast (raw-)value as a datatype self, or another node
        """
        if not value:
            if self.value is None:
                value = self.value_raw
            else:
                if isinstance(self.value, (StringType, BooleanType, NumberType)):
                    value = self.value.value
                else:
                    value = self.value
        if np.isscalar(value) and value in [None, Keyword.NONE]:
            value = None
        elif self.dimension or self.value_slice:
            # cast multidimensional values
            if isinstance(value, str):
                value = np.array(json.loads(value), dtype=self.dtype)
            else:
                value = np.array(value, dtype=self.dtype)
            if self.value_slice:
                value = self.slice_value(self.value_slice, value)
            if self.dimension:
                # check if dimensions are correct
                for d,dim in enumerate(self.dimension):
                    shape = value.shape[d]
                    if dim[0] is not None and shape < dim[0]:
                        raise Exception(f"Node '{self.name}' has invalid dimension: dim({d})={shape} < {dim[0]}")
                    if dim[1] is not None and shape > dim[1]:
                        raise Exception(f"Node '{self.name}' has invalid dimension: dim({d})={shape} > {dim[1]}")
            else:
                if not np.isscalar(value):
                    raise Exception("Array value set to scalar node:",self.code,value)
        else:
            # cast scalar values
            if value is not None:
                # casting string as boolean returns true always if string is non-empty
                # that's why we need to convert it expicitely
                if self.keyword=='bool':
                    if isinstance(value, BooleanType):
                        pass
                    elif isinstance(value, (bool,np.bool_)):
                        value = BooleanType(value)
                    elif value==Keyword.TRUE:
                        value = BooleanType(True)
                    elif value==Keyword.FALSE:
                        value = BooleanType(False)
                    else:
                        raise Exception("Could not convert raw value to boolean type:",value)
                else:
                    try:
                        if isinstance(value, FloatType):
                            if self.keyword=='int':
                                value = IntegerType(value.number, value.unit)
                        elif isinstance(value, IntegerType):
                            if self.keyword=='float':
                                value = FloatType(value.number, value.unit)
                        else:
                            value = self.dtype(value)
                    except:
                        raise Exception("Could not convert raw value to type:",self.code,value)
        return value

    def set_value(self, value=None):
        """ Set value using value_raw or arbitrary value
        """
        if value is None and self.value_raw:
            self.value = self.cast_value()
        elif value:
            self.value = value
        else:
            self.value = None
    
    def modify_value(self, node, env):
        """ Modify value taking value of a different node
        """
        if node.keyword!='mod' and node.dtype!=self.dtype:
            raise Exception(f"Datatype {self.dtype} of node '{self.name}' cannot be changed to {node.dtype}")
        if not self.value:  # create a dummy value if none
            self.set_value(node.value_raw)
        # copy value type modify values and units
        value = self.value.copy()
        value.value = self.cast_value(node.value_raw)
        if isinstance(value, (IntegerType, FloatType)):
            value.unit = node.units_raw
            value.convert(self.units_raw, env)
        self.set_value(value.value)

    def slice_value(self, slices, value=None):
        """ Slice part of the value

        :param list slices: List of tuples with slicing
        :param value: Value to be sliced. If none value of current node is taken.
        """
        if value is None:
            value = self.value
        if isinstance(value, Type):
            value = value.value
        smin, smax = slices.pop(0)
        if smin==smax and smin is not None:
            value = value[smin]
        elif smin!=smax:
            value = value[slice(smin,smax)]                  
        if slices:
            if smin==smax and smin is not None:
                return self.slice_value(slices.copy(), value)
            else:
                return np.array([self.slice_value(slices.copy(), val) for val in value])
        else:
            return value

    def inject_value(self, env:Environment, node=None):
        """ Inject value from a remote source

        :param env: Environment object
        :param node: Node object that should be injected
        """
        if not node:
            node = self
        if not node.value_ref:
            return
        if env.envtype==EnvType.DOCS:
            nodes = env.request(node.value_ref, count=[0,1], errsrc=False)
            if len(nodes)==0:
                return
        else:
            nodes = env.request(node.value_ref, count=1)
        if isinstance(nodes, str):   # block import
            node.value_raw = nodes
        else:                        # node import
            node.value_raw = nodes[0].value_raw
            if not node.units_raw:
                node.units_raw = nodes[0].units_raw
        
