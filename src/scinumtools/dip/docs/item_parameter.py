from enum import Enum, auto

from .settings import *
from .item_node import NodeItem

class ParType(Enum):
    DEC    = 0    # declaration
    DEF    = 1    # definition
    DCM    = 2    # declaration or modification
    DFM    = 3    # definition or modification
    MOD    = 4    # modification
    INJ    = 5    # injection
    IMP    = 6    # import
    
class ParameterItem:
    target: str
    name: str
    counts: list
    nodes: list
        
    def __init__(self, name, node):
        self.target = ParameterItemTarget(name)
        self.name    = name
        self.counts  = [0]*len(ParType)
        self.nodes   = []
        self.add(name, node)
        
    def add(self, name, node):
        # update node type counters
        if DocsType.DECLARATION|DocsType.MODIFICATION in node.docs_type:
            node_type = ParType.DCM
        elif DocsType.DEFINITION|DocsType.MODIFICATION in node.docs_type:
            node_type = ParType.DFM
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
