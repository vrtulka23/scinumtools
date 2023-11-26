from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from .node import NodeSection
from ..settings import *
from ....nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode, ImportNode
from ....settings import Order, Sign, Keyword, EnvType, DocsType
from ....environment import Environment

class InjectionsSection(NodeSection):
    
    def parse(self):
        self.color = PALETTE['mod']
        
        blocks = []
        blocks.append(Paragraph(f"Injected nodes", H2) )
        for name in self.names:
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(Paragraph(f"<strong>{name}</strong><a name=\"injection_{name}\"></a>"))
            blocks.append(Spacer(1,0.1*inch))
            for node in self.nodes[name]:
                if node.keyword==ImportNode.keyword:
                    continue
                blocks.append(self.parse_node(name, node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks