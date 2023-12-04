from .settings import *
from ..settings import ROOT_SOURCE

class SourceItem:
    target: str
    link_source: str
    name: str
    path: str
    parent: tuple
    code: str
            
    def __init__(self, source):
        self.target = SourceItemTarget(source.name, None)
        if source.parent:
            self.link_source = SourceItemTarget(source.parent[0], source.parent[1])
        self.name   = source.name
        self.path   = source.path
        self.parent = source.parent
        self.code   = source.code

