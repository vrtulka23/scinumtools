from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from ..settings import *
from ....nodes import Node, ImportNode
from ....settings import Order, Sign, Keyword, EnvType, DocsType
from ....environment import Environment

class ImportsSection:
    
    names: list
    nodes: list
    reference: str
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, nodes, env):
        self.nodes = nodes
        self.env = env
            
    def _init_node(self, node):
        
        # additional settings
        self.reference = None
        if node.value_ref:
            self.reference = "<font color='orange'>{"+node.value_ref+"}</font>"
                           
    def parse_node(self, node):
    
        self._init_node(node)
    
        # define table style
        TABLE_STYLE = [
            # whole grid
            #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod), 
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   PALETTE['c4']),   
            ('BACKGROUND', (0,0), (-1,0),   PALETTE['node_name']),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            ('BACKGROUND', (0,1), (1,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (1,1), (-1,-1),  PALETTE['prop_value']),   
            ('SPAN',       (0,0), (2,0)     ),                            # parameter name
        ]
        
        # construct a node table
        source = Paragraph(f"<a href=\"#source_{node.source[0]}_{node.source[1]}\" color=\"blue\">{node.source[0]}:{node.source[1]}</a>")
        data = [
            [source, '', ''],
        ]
        if self.reference:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['Request:', Paragraph(self.reference, TABLE_BODY_STYLE)])
            TABLE_STYLE.append(('VALIGN',(0,len(data)),(0,len(data)),'TOP'))
            data.append(['Nodes:', Paragraph('<br/>'.join(node.names), TABLE_BODY_STYLE)])

        colWidths = list(np.array([0.2, 0.57, 0.23])*(PAGE_WIDTH-2*inch))
        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Imports", H2) )
        for node in self.nodes:
            if node.keyword==ImportNode.keyword:
                blocks.append(Spacer(1,0.1*inch))
                blocks.append(self.parse_node(node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks