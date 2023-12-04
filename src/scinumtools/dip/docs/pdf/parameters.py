from reportlab.platypus import Paragraph, Table, Spacer
from reportlab.lib.units import inch
import numpy as np

from .settings import *
from ..settings import DocsType

class ParametersSection:
    
    names: list
    data: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data):
        self.data = data
        self.names = list(self.data.keys())
        self.names.sort()
    
    def parse_table(self):
        TABLE_STYLE = [
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('BACKGROUND', (0,0), (0,0),   PALETTE['node_name']),  
            ('BACKGROUND', (0,1), (-1,-1),   PALETTE['prop_value']),  
            ('BACKGROUND', (1,0), (1,0),   NTYPES[0][1]),  
            ('BACKGROUND', (2,0), (2,0),   NTYPES[1][1]),  
            ('BACKGROUND', (3,0), (3,0),   NTYPES[2][1]),  
            ('BACKGROUND', (4,0), (4,0),   NTYPES[3][1]),  
            ('BACKGROUND', (5,0), (5,0),   NTYPES[4][1]),  
            ('BACKGROUND', (6,0), (6,0),   NTYPES[5][1]),  
            ('BACKGROUND', (7,0), (7,0),   NTYPES[6][1]),  
        ]
    
        data = [['Property name', '#', '#', '#', '#', '#', '#', '#']]
        for name in self.names:
            item = self.data[name]
            #p = Paragraph(AnchorLink(AnchorType.PARAM, item.name))
            p = Paragraph(Link(item.target, item.name))
            counts = ['' if c==0 else c for c in item.counts]
            data.append([p]+counts)
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.72, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]))
        
    def parse(self):
        blocks = []       
        blocks.append(Paragraph(Title(f"Parameter list"), H2))
        blocks.append(self.parse_table())
        blocks.append(Spacer(1,0.2*inch))
        return blocks