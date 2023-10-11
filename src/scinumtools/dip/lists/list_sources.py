from typing import List, Dict, Union
from dataclasses import dataclass, field

from ..settings import Sign

@dataclass
class EnvSource:
    source: Union[str] # can be also DIP
    path: str
    name: str
    
@dataclass
class SourceList:
    sources: Dict   = field(default_factory = dict)  # custom reference sources
    
    def __len__(self):
        return len(self.sources)
    
    def __getitem__(self, key):
        return self.sources[key]
    
    def items(self):
        return self.sources.items()
    
    def append(self, name:str, source:str, path:str):
        """ Append a new source

        :param str name: Name of a new source
        :param source: Source can be either a DIP object or a text
        :param str path: Source path
        """
        if name in self.sources:
            raise Exception("Reference source alread exists:", name)
        self.sources[name] = EnvSource(source=source, path=str(path), name=name)

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