import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass, field
import copy

from ..units import Quantity, UnitEnvironment
from .settings import *
from .datatypes import NumberType, BooleanType
from .lists import NodeList, SourceList, UnitList

@dataclass
class Case:
    name: str
    value: bool
    code: str
    
@dataclass
class Environment:
    # Environment variables
    nodes: NodeList       = field(default_factory = NodeList)    # nodes
    units: UnitList       = field(default_factory = UnitList)    # list of cutom units
    sources: SourceList   = field(default_factory = SourceList)  # list of reference sources
    functions: Dict       = field(default_factory = dict)        # custom native functions

    # Reference on the current node
    autoref: str = None

    # Documentation mode
    docs: bool = False  

    # Hierarchy list
    parent_indents: List[int] = field(default_factory = list)    # indent level
    parent_names: List[str]   = field(default_factory = list)    # list of parent names

    # Case list
    cases: List[Case]       = field(default_factory = list)
    
    def __post_init__(self):
        self.parent_indents.append(-1)
    
    def copy(self):
        """ Copy a new object from self
        """
        return copy.copy(self)
        
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

    def false_case(self):
        """ Checks if case value is false
        """
        if not self.cases:
            return False
        return self.cases[-1].value.value == False
        
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        casename = self.cases[-1].name if self.cases else ''
        if node.name.endswith(Sign.CONDITION + Keyword.CASE):
            if casename+Keyword.CASE!=node.name:   # register new case
                self.cases.append(Case(
                    name = node.name[:-4],
                    value = node.value,
                    code = node.code
                ))
        elif node.name==casename + Keyword.ELSE:
            self.cases[-1].value = BooleanType(True)
            self.cases[-1].code = node.code
        elif node.name==casename + Keyword.END:    # end case using a keyword
            self.cases.pop()
        else:
            raise Exception(f"Invalid condition:", node.name)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.cases: # outside of any condition
            return        
        if not node.name.startswith(self.cases[-1].name): # ending case at lower indent
            self.cases.pop()
        if not self.docs:
            node.name = node.name.replace(Sign.CONDITION + Keyword.CASE + Sign.SEPARATOR,'')
            node.name = node.name.replace(Sign.CONDITION + Keyword.ELSE + Sign.SEPARATOR,'')

    def request(self, path:str, count:int=None, namespace:Namespace=Namespace.NODES, tags:list=None):
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
                if namespace == Namespace.NODES:
                    nodes = source.env.nodes.query(query, tags=tags)
                elif namespace == Namespace.SOURCES:
                    nodes = source.env.sources.query(query)
                elif namespace == Namespace.UNITS:
                    nodes = source.env.sources.query(query)
                else:
                    nodes = source.env.query(query, namespace, tags=tags)
        else:         # use values parsed in the current file
            if not self.nodes:
                raise Exception(f"Local nodes are not available for DIP import:", path)
            nodes = self.nodes.query(query, tags=tags)
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
            nodes = self.nodes.query(query, tags=tags)
        elif tags is not None:
            nodes = self.nodes.query("*", tags=tags)
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

    def pdf(self, file_path:str):

        nodes = self.nodes.query('*')
        with ExportPDF(nodes) as exp:
            exp.export(file_path)
        
