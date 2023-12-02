from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np

from .settings import *
from ...settings import ROOT_SOURCE

class UnitsSection:
    
    data: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data: list):
        self.data = data
        
    def parse_table(self):
        TABLE_STYLE = [
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('BACKGROUND', (0,0), (-1,0),   PALETTE['node_name']),  
            ('BACKGROUND', (0,1), (0,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (1,1), (-1,-1),    PALETTE['prop_value']),  
        ]
    
        data = [   
            ['Name','Value','Units','Source'],
        ]
        for item in self.data:
            src = Paragraph(Link(item.link_source, f"{item.source[0]}:{item.source[1]}")) 
            # add row to the table
            data.append([item.name, item.value, item.units, src])
            
        colWidths = list(np.array([0.2,0.2,0.2,0.4])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(Title(f"List of units"), H2))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    