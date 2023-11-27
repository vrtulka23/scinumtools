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
                    
    def _init_inode(self, node):
        ivalue, iunit = None, None
        if node.keyword==ModNode.keyword:
            ivalue = node.value
            if node.units_raw:
                iunit = node.units_raw
        else:
            if node.value.value:
                ivalue = str(node.value.value)
            if node.value.unit:
                iunit = node.value.unit
        return node.source, ivalue, iunit
                           
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
        target_injection = AnchorTarget(AnchorType.INJECT,inode)
        link_source = AnchorLink(AnchorType.SOURCE,inode.source)
        data = [
            [Paragraph(target_injection+link_source), ''],
        ]
        if self.reference:
            data.append(['Injecting node:',      Paragraph(AnchorLink(AnchorType.NODE, inode),    TABLE_BODY_STYLE)])
            data.append(['Request:', Paragraph(self.reference, TABLE_BODY_STYLE)])
            if inode.isource:
                isource, ivalue, iunit = self._init_inode(inode.isource)
                data.append(['From source:', Paragraph(AnchorLink(AnchorType.SOURCE, isource), TABLE_BODY_STYLE)])
                if ivalue:
                    data.append(['Value:', Paragraph(ivalue, TABLE_BODY_STYLE)])
                if iunit:
                    data.append(['Unit:',  Paragraph(iunit, TABLE_BODY_STYLE)])

        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.2, 0.8]))
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Injected values", H2) )
        for node in self.inodes:
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(self.parse_node(node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks
        