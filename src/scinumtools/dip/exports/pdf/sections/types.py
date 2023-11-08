from reportlab.platypus import Table, Paragraph, Spacer
from reportlab.lib.units import inch
import numpy as np

from ..settings import *

class TypesSection:
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def parse_table(self):
        TABLE_STYLE = [
            ('BACKGROUND', (1,0), (1,0),   PALETTE['dec']),  
            ('BACKGROUND', (1,1), (1,1),   PALETTE['def']),  
            ('BACKGROUND', (1,2), (1,2),   PALETTE['dec/mod']),  
            ('BACKGROUND', (1,3), (1,3),   PALETTE['def/mod']),  
            ('BACKGROUND', (1,4), (1,4),   PALETTE['mod']),  
        ]
    
        data = [   
            ['','','Declaration'],
            ['','','Definition'],
            ['','','Declaration / Modification'],
            ['','','Definition / Modification'],
            ['','','Modification'],
        ]
        colWidths = list(np.array([0.015, 0.035,0.95])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Node types", SECTION_STYLE))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    