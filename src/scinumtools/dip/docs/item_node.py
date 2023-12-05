import numpy as np

from .settings import *
from ..nodes import ModNode, ImportNode, StringNode
from ..settings import Sign, Keyword, EnvType

class NodeItem:
    target: str
    link_source: str
    link_injection: str
    link_import: str
    name: str
    value: str
    unit: str
    dtype: str
    source: tuple
    unsigned: bool
    precision: int
    injection: bool
    imported: tuple
    options: list
    constant: bool
    dformat: str
    tags: list
    description: str
    condition: str
               
    def __init__(self, name, node, node_type):
        self.target = NodeItemTarget(node.name, node.source[0], node.source[1])
        self.link_source = SourceItemTarget(node.source[0], node.source[1])
        self.link_injection = InjectionItemTarget(node.name, node.source[0], node.source[1])
        self.name = name
        self.source = node.source
        self.ntype = node_type.value
        # type specific initialization
        self.value = None
        self.options = None
        self.unsigned = None
        self.precision = None
        getattr(self,f"_init_{node.keyword}")(node)

        # find out units
        self.unit = ''
        if node.keyword != ModNode.keyword and node.value and node.value.unit:
            self.unit = node.value.unit
        elif node.units_raw:
            self.unit = node.units_raw
            
        # data type
        self.dtype = node.keyword
        if self.unsigned:
            self.dtype = f"u{self.dtype}"
        if self.precision:
            self.dtype = f"{self.dtype}{self.precision}"
        
        # references
        self.injection = True if node.value_ref else False
        self.imported = node.isource if isinstance(node.isource,tuple) else False
        if self.imported:
            self.link_import = ImportItemTarget(node.isource[0], node.isource[1])
        
        # node attributes
        self.constant = node.constant
        self.dformat = node.format if node.keyword == StringNode.keyword else None
        if node.keyword == ModNode.keyword or node.tags is None:
            self.tags = []
        else:
            self.tags = node.tags
        self.description = None if node.keyword == ModNode.keyword else node.description
        self.condition = None
        if node.condition:
            self.condition = node.condition
            
    def _init_bool(self, node):
        if node.value:
            self.value = Keyword.TRUE if node.value.value else Keyword.FALSE
            
    def _init_int(self, node):
        if node.value:
            if isinstance(node.value.value, (np.ndarray, list)):
                self.value = str(node.value.value)
            else:
                self.value = str(int(node.value.value))
        if node.units_raw:
            self.options = [f"{option.value.value} {option.value.unit}" for option in node.options]
        else:
            self.options = [f"{option.value.value}" for option in node.options]
        self.unsigned = node.unsigned
        self.precision = node.precision

    def _init_float(self, node):
        if node.value:
            if isinstance(node.value.value, (np.ndarray, list)):
                self.value = str(node.value.value)
            else:
                exp = np.log10(node.value.value)
                if exp<=3 or exp>=-3:
                    self.value = f"{node.value.value:.03f}"
                else:
                    self.value = f"{node.value.value:.03e}"
        if node.units_raw:
            self.options = [f"{option.value.value} {option.value.unit}" for option in node.options]
        else:
            self.options = [f"{option.value.value}" for option in node.options]
        self.precision = node.precision
        
    def _init_str(self, node):
        if node.value:
            self.value = str(node.value.value)
        self.options = [str(option.value.value) for option in node.options]
            
    def _init_mod(self, node):
        self.value = node.value
