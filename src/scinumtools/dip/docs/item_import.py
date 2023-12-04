from .settings import *
from dataclasses import dataclass, field

@dataclass
class ImportItemNode:
    name: str
    source: tuple
    link_node: str = None
    link_source: str = None

    def __post_init__(self):
        self.link_node = NodeItemTarget(self.name, self.source[0], self.source[1])
        self.link_source = SourceItemTarget(self.source[0], self.source[1])
        
class ImportItem:
    target: str
    link_source: str
    name: str
    reference: str
    source: tuple
    idata: list
    
    def __init__(self, node, nodes):
        self.target = ImportItemTarget(node.source[0], node.source[1])
        self.link_source = SourceItemTarget(node.source[0], node.source[1])
        self.name = node.clean_name().split('.{')[0]
        self.source = node.source
        self.reference = node.value_ref
        self.idata = []
        for inode in nodes:
            if inode.isource==node.source:
                self.idata.append(ImportItemNode(inode.name,inode.source))
    