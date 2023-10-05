import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass, field
import copy

from ..units import Quantity, UnitEnvironment
from .settings import Format, Sign, Keyword, Namespace
from .datatypes import NumberType

@dataclass
class EnvSource:
    source: Union[str] # can be also DIP
    path: str
    name: str
    
@dataclass
class Environment:
    # Environment variables
    nodes: List     = field(default_factory = list)   # nodes
    units: Dict     = field(default_factory = dict)   # custom units
    sources: Dict   = field(default_factory = dict)   # custom reference sources
    functions: Dict = field(default_factory = dict)  # custom native functions

    # Reference on the current node
    autoref: str = None

    # Documentation mode
    docs: bool = False  

    # Hierarchy list
    parent_indents: List[int] = field(default_factory = list)  # indent level
    parent_names: List[str]   = field(default_factory = list)    # list of parent names

    # Case list
    case_counts: List[int]  = field(default_factory = list)     # case number in a current condition
    case_names: List[str]   = field(default_factory = list)    # condition case name
    
    def __post_init__(self):
        self.parent_indents.append(-1)
        self.case_counts.append(0)
        self.case_names.append('')
    
    def copy(self):
        """ Copy a new object from self
        """
        return copy.copy(self)
        
    def pop_node(self):
        """ Pop first node out of the node list
        """
        return self.nodes.pop(0)

    def prepend_nodes(self, nodes):
        """ Prepend new nodes to the node list
        """
        self.nodes = nodes + self.nodes
    
    def update_hierarchy(self, node, excluded):
        """ Register new node to the hierarchy

        :param node: Node that should be added
        :param list excluded: List of node keywords that should be excluded from the hierarchy
        """
        if node.name is not None and node.keyword not in excluded:
            while node.indent<=self.parent_indents[-1]:
                self.parent_indents.pop()
                self.parent_names.pop()
            self.parent_names.append(node.name)
            self.parent_indents.append(node.indent)
            node.name = Sign.SEPARATOR.join(self.parent_names)

    def is_case(self):
        """ Checks if outside or inside of a valid case clause
        """
        return not self.case_names[-1] or self.case_counts[-1]<2

    def _end_case(self):
        self.case_names.pop()
        self.case_counts.pop()
    
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        casename = self.case_names[-1]
        if node.name.endswith(Sign.CONDITION + Keyword.CASE):
            if casename+Keyword.CASE!=node.name:   # register new case
                self.case_names.append(node.name[:-4])
                self.case_counts.append(0)
            if node.value or self.case_counts[-1]==1:
                self.case_counts[-1] += 1
        elif node.name==casename + Keyword.ELSE:
            self.case_counts[-1] += 1
        elif node.name==casename + Keyword.END:    # end case using a keyword
            self._end_case()
        else:
            raise Exception(f"Invalid condition:", node.name)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.case_names[-1]: # outside of any condition
            return        
        if not node.name.startswith(self.case_names[-1]): # ending case at lower indent
            self._end_case()
        node.name = node.name.replace(
            Sign.CONDITION + Keyword.CASE + Sign.SEPARATOR,''
        )
        node.name = node.name.replace(
            Sign.CONDITION + Keyword.ELSE + Sign.SEPARATOR,''
        )

    
    def add_unit(self, name:str, unit:Quantity):
        """ Add a new source

        :param str name: Name of a new unit
        :param Quantity unit: Quantity object
        :param float num: Numerical value
        :param str expr: Unit expression
        """
        name = f"[{name}]"
        if name in self.units:
            raise Exception("Reference unit alread exists:", name)
        self.units[name] = {'magnitude':unit.magnitude.value, 'dimensions':unit.baseunits.dimensions.value()} #,'prefixes':['k','M','G']}
        
    def add_source(self, name:str, source:str, path:str):
        """ Add a new source

        :param str name: Name of a new source
        :param source: Source can be either a DIP object or a text
        :param str path: Source path
        """
        if name in self.sources:
            raise Exception("Reference source alread exists:", name)
        self.sources[name] = EnvSource(source=source, path=str(path), name=name)
        
    def query(self, query:str, namespace:int=Namespace.NODES, tags:list=None):
        """ Select local nodes according to a query

        :param str query: Node selection query
        :param str namespace: Query namespace (nodes, sources, or units)
        :param list tags: List of tags
        """
        if namespace==Namespace.NODES:
            nodes = []
            if query==Sign.WILDCARD:
                nodes = [node.copy() for node in self.nodes]
            elif query[-2:]==Sign.SEPARATOR + Sign.WILDCARD:
                for node in self.nodes:
                    if node.name.startswith(query[:-1]):
                        node = node.copy()
                        node.name = node.name[len(query[:-1]):]
                        nodes.append(node.copy())
            else:
                for node in self.nodes:
                    if node.name==query:
                        node = node.copy()
                        node.name = node.name.split(Sign.SEPARATOR)[-1]
                        nodes.append(node.copy())
            if tags:
                tagged = []
                for n in range(len(nodes)):
                    if nodes[n].tags and np.in1d(tags, nodes[n].tags):
                        tagged.append(nodes[n])
                nodes = tagged
            return nodes
        elif namespace==Namespace.SOURCES:
            if query==Sign.WILDCARD:   # return all sources
                return self.sources
            else:                     # return particular source
                if query not in self.sources:
                    raise Exception("Requested source does not exists:", query)
                return {query: self.sources[query]}
        elif namespace==Namespace.UNITS:
            if query==Sign.WILDCARD:   # return all units
                return self.units
            else:                     # return particular unit
                if query not in self.units:
                    raise Exception("Requested unit does not exists:", query)
                return {query: self.units[query]}
        else:
            raise Exception("Invalid query namespace selected:", namespace)
        
    def request(self, path:str, count:int=None, namespace:str=Namespace.NODES, tags:list=None):
        """ Request nodes from a path

        :param str path: Request path
        :param int count: Number of nodes that should be selected
        :param str namespace: Query namespace (nodes, sources, or units)
        :param list tags: List of tags
        """
        if self.autoref and path == Sign.QUERY: # reference type {?}
            filename,query = '', self.autoref
        elif Sign.QUERY in path:                    # reference type {source?query}
            filename,query = path.split(Sign.QUERY)
        else:                                      # reference type {source}
            filename,query = path,Sign.WILDCARD
        if filename:  # use external source to parse the values
            source = self.sources[filename].source
            if isinstance(source, str):
                return source
            else:
                nodes = source.env.query(query, namespace, tags=tags)
        else:         # use values parsed in the current file
            if not self.nodes:
                raise Exception(f"Local nodes are not available for DIP import:", path)
            nodes = self.query(query, namespace, tags=tags)
        if count:
            if isinstance(count, list) and len(nodes) not in count:
                raise Exception(f"Path returned invalid number of nodes:", path, count, len(nodes))
            elif np.isscalar(count) and len(nodes)!=count:
                raise Exception(f"Path returned invalid number of nodes:", path, count, len(nodes))
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
            nodes = self.query(query, tags=tags)
        elif tags is not None:
            nodes = self.query("*", tags=tags)
        else:
            nodes = self.nodes
        for node in nodes:
            if format==Format.VALUE:
                data[node.name] = node.value.value
            elif format==Format.TYPE:
                data[node.name] = node.value
            elif format==Format.TUPLE:
                if isinstance(node.value, NumberType) and node.value.unit is not None:
                    data[node.name] = (node.value.value, node.value.unit)
                else:
                    data[node.name] = node.value.value
            elif format==Format.QUANTITY:
                if isinstance(node.value, NumberType):
                    data[node.name] = Quantity(node.value.value, node.value.unit)
                else:
                    data[node.name] = node.value.value
            elif format==Format.NODE:
                data[node.name] = node
            else:
                raise Exception("Data format not recognized:", format)
            if verbose:
                 print(node.name,'|',node.indent,'|',node.keyword,'|',str(node.value),
                       '|',repr(node.units_raw), end='')
                 if hasattr(node,'options'):
                     if node.options:
                         print(' |',node.options, end='') 
                 print()
        return data
