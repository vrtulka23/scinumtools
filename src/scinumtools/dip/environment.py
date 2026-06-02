import numpy as np
from dataclasses import dataclass, field
import re
import copy

from ..units import Quantity
from .datatypes import NumberType
from .settings import *
from .lists import *
    
@dataclass
class Environment:
    # Environment variables lists
    nodes: NodeList          = field(default_factory = NodeList)       # nodes
    units: UnitList          = field(default_factory = UnitList)       # list of cutom units
    sources: SourceList      = field(default_factory = SourceList)     # list of reference sources
    functions: FunctionList  = field(default_factory = FunctionList)   # custom native functions

    # State variable lists
    hierarchy: HierarchyList = field(default_factory = HierarchyList)  # node name hierarchy
    branching: BranchingList = field(default_factory = BranchingList)  # code branching

    # Special mode flags
    autoref: str     = None          # Reference on the current node
    envtype: EnvType = EnvType.DATA  # Documentation mode
    
    def copy(self):
        """ Copy a new object from self
        """
        return copy.deepcopy(self)

    def request(self, path:str, count:int=None, namespace:Namespace=Namespace.NODES, tags:list=None, errsrc:bool=True):
        """ Request nodes from a path

        :param str path: Request path
        :param int count: Number of nodes that should be selected
        :param str namespace: Query namespace (nodes, sources, or units)
        :param list tags: List of tags
        :param bool errsrc: If 'False', missing sources will not throw errors
        """
        if self.autoref and path == Sign.QUERY:     # reference type {?}
            source, query = '', self.autoref
        elif Sign.QUERY in path:                    # reference type {source?query}
            source, query = path.split(Sign.QUERY)
        else:                                       # reference type {source}
            source, query = path,None
        if source:  # use external source to parse the values
            if source not in self.sources and errsrc is False:
                nodes = []
            elif query is None:   # import block
                return self.sources[source].code
            elif namespace == Namespace.NODES:
                nodes = self.sources[source].nodes.query(query, tags=tags)
            elif namespace == Namespace.SOURCES:
                nodes = self.sources[source].sources.query(query)
            elif namespace == Namespace.UNITS:
                nodes = self.sources[source].units.query(query)
            else:
                nodes = self.sources[source].query(query, namespace, tags=tags)
        else:         # use values parsed in the current file
            if not self.nodes:
                raise Exception("Local nodes are not available for DIP import:", path)
            nodes = self.nodes.query(query, tags=tags)
        if count:
            if isinstance(count, list) and len(nodes) not in count:
                raise Exception("Path returned invalid number of nodes:", path, count, len(nodes))
            elif np.isscalar(count) and len(nodes)!=count:
                raise Exception("Path returned invalid number of nodes:", path, count, len(nodes))
        return nodes

    def data(self, format:Format=Format.VALUE, verbose:bool=False, query:str=None, tags:list=None):
        """ Return parsed values as a dictionary

        :param bool verbose: Display node values
        :param str format: Return data as values only, DIP datatypes, or tuples
        :param str query: Node selection query
        :param list tags: List of tags
        """
        data = {}
        if query is not None:
            nodes = self.nodes.query(query, tags=tags)
        elif tags is not None:
            nodes = self.nodes.query("*", tags=tags)
        else:
            nodes = self.nodes
        for node in nodes:
            if format==Format.VALUE:
                value = node.value.value
            elif format==Format.TYPE:
                value = node.value
            elif format==Format.TUPLE:
                if isinstance(node.value, NumberType) and node.value.unit is not None:
                    value = (node.value.value, node.value.unit)
                else:
                    value = node.value.value
            elif format==Format.QUANTITY:
                if isinstance(node.value, NumberType):
                    value = Quantity(node.value.value, node.value.unit)
                else:
                    value = node.value.value
            elif format==Format.NODE:
                value = node
            else:
                raise Exception("Data format not recognized:", format)
            if node.name.count("[") != node.name.count("]"):
                raise Exception("Unclosed group symbols in the node name:", node.name)
            elif "[" in node.name:
                parts = re.split(r'(\[[^\]]+\])', node.name)
                current = data
                for part in parts[:-1]:
                    if part[0] == "[":
                        if current is None:
                            current = {}
                        if part[1:-1] not in current:
                            current[part[1:-1]] = {}
                        current = current[part[1:-1]]
                    else:
                        if part[0] == ".":
                            part = part[1:]
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                part = parts[-1]
                part = part[1:] if part[0]=="." else part
                current[part] = value
            else:
                data[node.name] = value
            if verbose:
                 print(node.name,'|',node.indent,'|',node.keyword,'|',str(node.value),
                       '|',repr(node.units_raw), end='')
                 if hasattr(node,'options'):
                     if node.options:
                         print(' |',node.options, end='') 
                 print()
        return data
        
