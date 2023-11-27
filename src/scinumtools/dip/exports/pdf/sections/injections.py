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
    
    nodes: list      # node list
    inodes: list     # import node list
    reference: str
    env: Environment
    
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, inodes, nodes, env):
        self.inodes = inodes
        self.nodes = nodes
        self.env = env
            
    def _init_node(self, node):
        
        # additional settings
        self.reference = None
        if node.value_ref:
            self.reference = HighlightReference("{"+node.value_ref+"}")
                           
    def parse_node(self, inode):
    
        self._init_node(inode)
    
        # define table style
        TABLE_STYLE = [
            # whole grid
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   PALETTE['c4']),   
            ('BACKGROUND', (0,0), (-1,0),   PALETTE['node_name']),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            ('BACKGROUND', (0,1), (0,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (1,1), (1,-1),  PALETTE['prop_value']),  
        ]
        
        # construct a node table
        source = Paragraph(AnchorLink(AnchorType.SOURCE,inode.source))
        data = [
            [source, ''],
        ]
        if self.reference:
            data.append(['Request:', Paragraph(self.reference, TABLE_BODY_STYLE)])
            data.append(['Injection node:',      Paragraph(AnchorLink(AnchorType.NODE, inode),    TABLE_BODY_STYLE)])
            if inode.isource:
                isource = Paragraph(AnchorLink(AnchorType.SOURCE, inode.isource), TABLE_BODY_STYLE)
                data.append(['From source:', isource])
    
        colWidths = list(np.array([0.2, 0.8])*(PAGE_WIDTH-2*inch))
        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Injected nodes", H2) )
        for node in self.inodes:
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(self.parse_node(node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks
        