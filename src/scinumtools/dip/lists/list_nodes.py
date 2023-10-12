from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np

from ..settings import Order, Sign

@dataclass
class NodeList:
    nodes: List     = field(default_factory = list)  # list of nodes
    
    def __len__(self):
        return len(self.nodes)
    
    def __delitem__(self, key):
        del self.nodes[key]
    
    def __getitem__(self, key: Union[int, str]):
        if isinstance(key, int):
            return self.nodes[key]
        elif isinstance(key, str):
            nodes = NodeList()
            for node in self.nodes:
                if node.name == key:
                    return node.copy()
                elif node.name.startswith(key+Sign.SEPARATOR):
                    node = node.copy()
                    node.name = node.name[len(key)+1:]
                    nodes.append(node)
            return nodes
        else:
            raise Exception("Node list keys can be only integers or strings:", key)
        
    def keys(self):
        keys = []
        for node in self.nodes:
            node_key = node.name.split(Sign.SEPARATOR)[0]
            if node_key not in keys:
                keys.append(node_key)
        keys.sort()
        return keys
        
    def pop(self):
        return self.nodes.pop(0)
    
    def append(self, node):
        self.nodes.append(node)
        
    def prepend(self, nodes):
        self.nodes = nodes + self.nodes
        
    def query(self, query:str, tags:list=None, order:Order=None):
        """ Select local nodes according to a query

        :param str query:   Node selection query
        :param list tags:   List of tags
        :param Order order: List ordering
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
        if order:
            nodes = list(dict(sorted({node.name:node for node in nodes}.items())).values())
        return nodes