import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass, field
import copy
from enum import Enum, auto

from .environment import Environment
from .nodes import ModNode, ImportNode, StringNode
from .settings import Sign, DocsType, Keyword, ROOT_SOURCE

# Parameter types

class ParType(Enum):
    DEC    = 0    # declaration
    DEF    = 1    # definition
    DECMOD = 2    # declaration or modification
    DEFMOD = 3    # definition or modification
    MOD    = 4    # modification
    INJ    = 5    # injection
    IMP    = 6    # import
    
# Injections

class InjectionItem:
    key: str
    name: str               
    reference: str          
    source: tuple           
    isource: tuple = None   
    ivalue: str = None
    iunit: str = None
    
    @staticmethod        
    def key(name:str, source:str, lineno:int):
        return f"INJECT_{name}_{source}_{lineno}"
    
    def __init__(self, node, env):
        self.key = InjectionItem.key(node.name, node.source[0], node.source[1])
        self.name = node.name
        self.reference = node.value_ref
        self.source = node.source
        ref_source, ref_node = node.value_ref.split(Sign.QUERY)
        if ref_source in env.sources:
            inode = env.request(node.value_ref)[0]
            if inode.keyword==ModNode.keyword:
                self.ivalue = inode.value
                if inode.units_raw:
                    self.iunit = inode.units_raw
            else:
                if inode.value.value:
                    self.ivalue = str(inode.value.value)
                if inode.value.unit:
                    self.iunit = inode.value.unit
            self.isource = inode.source

# Imports

@dataclass
class ImportItemNode:
    name: str
    source: tuple
    link_node: str = None

    def __post_init__(self):
        self.link_node = NodeItem.key(self.name, self.source[0], self.source[1])
        
class ImportItem:
    key: str
    name: str
    reference: str
    source: tuple
    idata: list
    
    @staticmethod        
    def key(source:str, lineno:int):
        return f"IMPORT_{source}_{lineno}"
        
    def __init__(self, node, nodes):
        self.key = ImportItem.key(node.source[0], node.source[1])
        self.name = node.clean_name().split('.{')[0]
        self.source = node.source
        self.reference = node.value_ref
        self.idata = []
        for inode in nodes:
            if inode.isource==node.source:
                self.idata.append(ImportItemNode(inode.name,inode.source))
    
# Sources

class SourceItem:
    key: str
    link_source: str
    name: str
    path: str
    parent: tuple
    code: str
    
    @staticmethod        
    def key(source:str, lineno:int=None):
        if ROOT_SOURCE in source or lineno is None:
            return f"SOURCE_{source}"
        else:
            return f"SOURCE_{source}_{lineno}"
            
    def __init__(self, source):
        self.key = SourceItem.key(source.name, None)
        if source.parent:
            self.link_source = SourceItem.key(source.parent[0], source.parent[1])
        self.name   = source.name
        self.path   = source.path
        self.parent = source.parent
        self.code   = source.code

# Units

class UnitItem:
    key: str
    link_source: str
    name: str
    value: str
    units: str
    source: tuple
    
    @staticmethod        
    def key(name: str):
        return f"UNIT_{name}"

    def __init__(self, name, unit):
        self.key = UnitItem.key(name)
        self.link_source = SourceItem.key(unit['source'][0],unit['source'][1])
        self.name   = name
        self.value  = unit['value']
        self.units  = unit['units']
        self.source = unit['source']

# Parameters

class NodeItem:
    key: str
    name: str
    value: str
    unit: str
    dtype: str
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
               
    @staticmethod        
    def key(name:str, source:str, lineno:int):
        return f"NODE_{name}_{source}_{lineno}"
        
    def __init__(self, name, node, node_type):
        self.key = NodeItem.key(node.name, node.source[0], node.source[1])
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

class ParameterItem:
    key: str
    name: str
    types: dict
    counts: list
    nodes: list
    
    @staticmethod        
    def key(name: str):
        return f"PARAM_{name}"
        
    def __init__(self, name, node):
        self.key = ParameterItem.key(name)
        self.name    = name
        self.counts  = [0]*len(ParType)
        self.nodes   = []
        self.add(name, node)
        
    def add(self, name, node):
        # update node type counters
        if DocsType.DECLARATION|DocsType.MODIFICATION in node.docs_type:
            node_type = ParType.DECMOD
        elif DocsType.DEFINITION|DocsType.MODIFICATION in node.docs_type:
            node_type = ParType.DEFMOD
        elif DocsType.DECLARATION in node.docs_type:
            node_type = ParType.DEC
        elif DocsType.DEFINITION in node.docs_type:
            node_type = ParType.DEF
        elif DocsType.MODIFICATION in node.docs_type:
            node_type = ParType.MOD
        self.counts[node_type.value] += 1
        # update reference counters
        if node.value_ref:
            self.counts[ParType.INJ.value] += 1
        if node.isource:
            self.counts[ParType.IMP.value] += 1
        # add node to the list
        self.nodes.append(NodeItem(name, node, node_type))

@dataclass
class Documentation:
    
    env: Environment
    types: dict      = field(default_factory=dict)
    parameters: dict = field(default_factory=dict)
    imports: list    = field(default_factory=list)
    injections: list = field(default_factory=list)
    units: list      = field(default_factory=list)
    sources: list    = field(default_factory=list)
    
    def __post_init__(self):
        # group nodes according to their names
        nodes = self.env.nodes.query("*")
        
        # populate sources
        self.sources = []
        for name,source in self.env.sources.items():
            self.sources.append(SourceItem(source))
        
        # populate units
        self.units = []
        for name,unit in self.env.units.items():
            self.units.append(UnitItem(name, unit))
        
        # populate nodes, parameters, injections and imports
        self.parameters = {}
        self.injections = []
        self.imports = []
        for node in nodes:
            if node.keyword==ImportNode.keyword:
                self.imports.append(ImportItem(node, nodes))
            else:
                name = node.clean_name()
                if name in self.parameters:
                    self.parameters[name].add(name, node)
                else:
                    self.parameters[name] = ParameterItem(name, node)
                if node.value_ref:
                    self.injections.append(InjectionItem(node,self.env))
                    
        # populate node types
        self.types = [t.value for t in ParType]
    
    def copy(self):
        """ Copy a new object from self
        """
        return copy.deepcopy(self)