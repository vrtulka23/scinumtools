import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass, field
import copy

from .settings import *
from .item_parameter import ParameterItem, ParType
from .item_injection import InjectionItem
from .item_import import ImportItem
from .item_unit import UnitItem
from .item_source import SourceItem
from ..environment import Environment
from ..nodes import ModNode, ImportNode, StringNode
from ..settings import Sign, Keyword, EnvType

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
        if self.env.envtype != EnvType.DOCS:
            raise Exception("Given environment is not a documentation environment")
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