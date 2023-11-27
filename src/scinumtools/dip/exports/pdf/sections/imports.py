from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from ..settings import *
from ....nodes import Node, ImportNode
from ....settings import Order, Sign, Keyword, EnvType, DocsType
from ....environment import Environment

class ImportsSection:
    
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
            ('BACKGROUND', (0,1), (1,1),   PALETTE['prop_name']),        # request title
            ('BACKGROUND', (0,2), (2,2),   PALETTE['prop_name']),        # node name title
            ('BACKGROUND', (1,1), (-1,1),  PALETTE['prop_value']),      # request value
            ('SPAN',       (0,0), (2,0)     ),                            # parameter name
            ('SPAN',       (1,1), (2,1)     ),                            # request
            ('SPAN',       (0,2), (1,2)    ),                            # original names
        ]
        
        # construct a node table
        source = Paragraph(AnchorLink(AnchorType.SOURCE,inode.source))
        data = [
            [source, '', ''],
        ]
        if self.reference:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['Request:', Paragraph(self.reference, TABLE_BODY_STYLE)])
            rows = []
            for name in self.nodes.keys():
                for node in self.nodes[name]:
                    if node.isource==inode.source:
                        nrow = len(data)+1+len(rows)
                        TABLE_STYLE.append(('SPAN', (0,nrow), (1,nrow) ))
                        rows.append([
                            Paragraph(AnchorLink(AnchorType.NODE, node), TABLE_BODY_STYLE),  
                            '',
                            Paragraph(AnchorLink(AnchorType.SOURCE, node.source), TABLE_BODY_STYLE),  
                        ])
            if rows:
                TABLE_STYLE.append(('BACKGROUND', (0,3), (-1,-1),  PALETTE['prop_value']))
                data.append(['Imported node:', '',  'From source:'])
                data += rows
                        
        colWidths = list(np.array([0.2, 0.5, 0.3])*(PAGE_WIDTH-2*inch))
        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Imports", H2) )
        for node in self.inodes:
            if node.keyword==ImportNode.keyword:
                blocks.append(Spacer(1,0.1*inch))
                blocks.append(self.parse_node(node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks