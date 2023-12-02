from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np

from .settings import *

class TypesSection:
    
    data: dict
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data: dict):
        self.data = data
        
    def parse_table(self):
        
        TABLE_STYLE = [
            ('BACKGROUND', (0,0), (0,0),   NTYPES[self.data[0]][1]),  
            ('BACKGROUND', (0,1), (0,1),   NTYPES[self.data[1]][1]),  
            ('BACKGROUND', (0,2), (0,2),   NTYPES[self.data[2]][1]),  
            ('BACKGROUND', (0,3), (0,3),   NTYPES[self.data[3]][1]),  
            ('BACKGROUND', (0,4), (0,4),   NTYPES[self.data[4]][1]),  
            ('BACKGROUND', (2,0), (2,0),   NTYPES[self.data[5]][1]),  
            ('BACKGROUND', (2,1), (2,1),   NTYPES[self.data[6]][1]),  
        ]
    
        data = [   
            ['',NTYPES[self.data[0]][0],'',NTYPES[self.data[5]][0] ],
            ['',NTYPES[self.data[1]][0],'',NTYPES[self.data[6]][0] ],
            ['',NTYPES[self.data[2]][0] ],
            ['',NTYPES[self.data[3]][0] ],
            ['',NTYPES[self.data[4]][0] ],
        ]
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.05,0.45,0.05,0.45]))
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(Title(f"Node types"), H2))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    