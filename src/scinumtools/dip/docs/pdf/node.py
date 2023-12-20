from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from .settings import *
from ..settings import DocsType
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode, ModNode, ImportNode
from ...settings import Order, Sign, Keyword, EnvType

class NodeSection:
    
    data: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data):
        self.data = data
            
    def parse_node(self, name, node):
    
        # define color
        color = NTYPES[node.ntype][1]
    
        # define table style
        TABLE_STYLE = [
            # whole grid
            #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod), 
            ('GRID',       (1,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   PALETTE['c4']),   
            ('BACKGROUND', (0,0), (-1,0),   PALETTE['node_name']),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            ('BACKGROUND', (1,1), (1,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (2,1), (-1,-1),  PALETTE['prop_value']),   
            ('SPAN',       (1,0), (2,0)     ),                            # parameter name
            ('BACKGROUND', (0,0), (0,-1),   color),                       # instance type
        ]
        
        # construct a node table
        node_target = Target(node.target)
        source_link = Link(node.link_source, f"{node.source[0]}:{node.source[1]}")
        injection_link = Link(node.link_injection, " | injected") if node.injection else ''
        import_link = Link(node.link_import, " | imported") if node.imported else ''
        dtype = node.dtype
        if node.constant:
            dtype = f"constant {dtype}"
        data = [
            ['', Paragraph(f"{node_target}{source_link}{injection_link}{import_link}"), '', dtype],
        ]
        if node.value:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['', 'Value:',        Paragraph(node.value, TABLE_BODY_STYLE)])
        if node.unit:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Unit:',          Paragraph(node.unit, TABLE_BODY_STYLE)])
        if node.condition:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Condition:',     Paragraph(HighlightReference(node.condition), style=TABLE_BODY_STYLE)])
        if node.tags:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Tags:',          Paragraph(", ".join(node.tags), TABLE_BODY_STYLE)])
        if node.options: 
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Options:',       Paragraph(", ".join(node.options), TABLE_BODY_STYLE)])
        if node.dformat:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Format:',        Paragraph(node.dformat, TABLE_BODY_STYLE)])
        if node.description:
            TABLE_STYLE.append(('SPAN', (2,len(data)), (-1,len(data)) ))
            data.append(['','Description:',   Paragraph(node.description, TABLE_BODY_STYLE)])
            
        return Table(
            data, style=TABLE_STYLE, hAlign='LEFT', 
            colWidths=ColumnWidths([0.01,0.2, 0.50, 0.29])
        )

    def parse(self):
        blocks = []
        blocks.append(Paragraph(Title(f"Parameter nodes"), H2) )
        names = list(self.data.keys())
        names.sort()
        for name in names:
            pdata = self.data[name]
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(Paragraph(f"<strong>"+Target(pdata.target, name)+"</strong>"))
            blocks.append(Spacer(1,0.1*inch))
            for node in pdata.nodes:
                blocks.append(self.parse_node(name, node))
        blocks.append(Spacer(1,0.2*inch))
        return blocks