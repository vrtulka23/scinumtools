from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np

from ..settings import Order, Sign

@dataclass
class NodeList:
    nodes: List     = field(default_factory = list)  # list of nodes
    
    def __len__(self):
        return len(self.nodes)
    
    def __getitem__(self, key):
        return self.nodes[key]
        
    def pop(self):
        return self.nodes.pop(0)
    
    def append(self, node):
        self.nodes.append(node)
        
    def prepend(self, nodes):
        self.nodes = nodes + self.nodes
        
    def order(self, order: Order):
        self.nodes = list(dict(sorted({node.name:node for node in self.nodes}.items())).values())
    
    def query(self, query:str, tags:list=None):
        """ Select local nodes according to a query

        :param str query: Node selection query
        :param list tags: List of tags
        """
        nodes = NodeList()
        if query==Sign.WILDCARD:
            nodes = NodeList([node.copy() for node in self.nodes])
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
            tagged = NodeList()
            for n in range(len(nodes)):
                if nodes[n].tags and np.in1d(tags, nodes[n].tags):
                    tagged.append(nodes[n])
            nodes = tagged
        return nodes