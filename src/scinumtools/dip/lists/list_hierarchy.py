from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np

from ..settings import Sign

@dataclass
class Parent:
    indent: int 
    name: str   
    
@dataclass
class HierarchyList:
    parents: List[Parent] = field(default_factory = list)
    
    def register(self, node, excluded):
        """ Register new node to the hierarchy

        :param node: Node that should be added
        :param list excluded: List of node keywords that should be excluded from the parents
        """
        if node.name is not None and node.keyword not in excluded:
            while self.parents and node.indent<=self.parents[-1].indent:
                self.parents.pop()
            self.parents.append(Parent(node.indent, node.name))
            node.name = Sign.SEPARATOR.join([parent.name for parent in self.parents])