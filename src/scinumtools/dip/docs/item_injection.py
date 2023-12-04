from .settings import *
from ..nodes import ModNode, ImportNode, StringNode
from ..settings import Sign, Keyword, EnvType

class InjectionItem:
    target: str
    link_source: str
    link_node: str
    link_isource: str
    name: str               
    reference: str          
    source: tuple           
    isource: tuple = None   
    ivalue: str = None
    iunit: str = None
    
    def __init__(self, node, env):
        self.target = InjectionItemTarget(node.name, node.source[0], node.source[1])
        self.link_source = SourceItemTarget(node.source[0], node.source[1])
        self.link_node = NodeItemTarget(node.name, node.source[0], node.source[1])
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
            self.link_isource = SourceItemTarget(inode.source[0], inode.source[1])
