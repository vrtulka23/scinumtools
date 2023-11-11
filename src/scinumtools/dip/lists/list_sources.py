from typing import List, Dict, Union
from dataclasses import dataclass, field
import copy

from ..settings import Sign
from .list_nodes import NodeList

@dataclass
class EnvSource:
    name: str            # this source name
    path: str            # source filename
    code: str            # source code
    parent_name: str = None     # parent source name
    parent_lineno: int = None   # parent source line number
    nodes: NodeList = None      # list of nodes (only for remote sources)
    sources: 'SourceList' = None  # list of sources (only for remote sources)
    
@dataclass
class SourceList:
    sources: Dict   = field(default_factory = dict)  # custom reference sources
    
    def __len__(self):
        return len(self.sources)
    
    def __getitem__(self, name: str):
        return self.sources[name]

    def __setitem__(self, name: str, source: EnvSource):
        self.sources[name] = source

    def __contains__(self, item):
        return item in self.sources
    
    def items(self):
        return self.sources.items()
    
    def keys(self):
        return self.sources.keys()
    
    def copy(self):
        """ Copy a new object from self
        """
        return copy.deepcopy(self)
        
    def append(self, name:str, path:str, code:str, parent_name:str = None, parent_lineno:int = None):
        """ Append a new source

        :param str name: Name of a new source
        :param source: Source can be either a DIP object or a text
        :param str path: Source path
        """
        if name in self.sources:
            raise Exception("Reference source alread exists:", name)
        self.sources[name] = EnvSource(name, str(path), code,  parent_name, parent_lineno)

    def query(self, query:str):
        """ Select sources according to a query

        :param str query: Source selection query
        """
        if query==Sign.WILDCARD:   # return all sources
            return self.sources
        else:                     # return particular source
            if query not in self.sources:
                raise Exception("Requested source does not exists:", query)
            return {query: self.sources[query]}