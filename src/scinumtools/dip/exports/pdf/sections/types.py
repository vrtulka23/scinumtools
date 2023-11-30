from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
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
            ('BACKGROUND', (0,0), (0,0),   PALETTE['dec']),  
            ('BACKGROUND', (0,1), (0,1),   PALETTE['def']),  
            ('BACKGROUND', (0,2), (0,2),   PALETTE['dec/mod']),  
            ('BACKGROUND', (0,3), (0,3),   PALETTE['def/mod']),  
            ('BACKGROUND', (0,4), (0,4),   PALETTE['mod']),  
            ('BACKGROUND', (2,0), (2,0),   PALETTE['inj']),  
            ('BACKGROUND', (2,1), (2,1),   PALETTE['imp']),  
        ]
    
        data = [   
            ['','Declaration','','Injection'],
            ['','Definition','','Import'],
            ['','Declaration / Modification'],
            ['','Definition / Modification'],
            ['','Modification'],
        ]
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.05,0.45,0.05,0.45]))
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,f"Node types"), H2))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    