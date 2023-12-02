from reportlab.platypus import Paragraph, Table, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np
import re

from .settings import *
from ...nodes import ModNode

class InjectionsSection:
    
    nodes: list      # node list
    
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data):
        self.data = data
                           
    def parse_item(self, item):
    
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
        
        # construct a item table
        target_injection = Target(item.target)
        link_source = Link(item.link_source, f"{item.source[0]}:{item.source[1]}") 
        data = [
            [Paragraph(target_injection+link_source), ''],
        ]
        data.append(['Injecting node:', Paragraph(Link(item.link_node, item.name),          TABLE_BODY_STYLE)])
        data.append(['Request:',        Paragraph(HighlightReference("{"+item.reference+"}"), TABLE_BODY_STYLE)])
        if item.isource:
            data.append(['From source:', Paragraph(Link(item.link_isource, f"{item.isource[0]}:{item.isource[1]}"), TABLE_BODY_STYLE)])
        if item.ivalue:
            data.append(['Value:', Paragraph(item.ivalue, TABLE_BODY_STYLE)])
        if item.iunit:
            data.append(['Unit:',  Paragraph(item.iunit, TABLE_BODY_STYLE)])

        return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.2, 0.8]))
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(Title(f"Injected values"), H2) )
        for item in self.data:
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(self.parse_item(item))
        blocks.append(Spacer(1,0.2*inch))
        return blocks
        