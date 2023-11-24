from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np

from ..settings import *

class TOCSection:
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def parse_table(self):
        TABLE_STYLE = [
        ]
    
        sections = {
            'types':      'Node types',
            'parameters': 'Parameters',
            'nodes':      'Nodes',
            'imports':    'Imports',
            'units':      'Units',
            'sources':    'Sources',
        }
        data = []
        for href, name in sections.items():
            data.append([Paragraph(f"<a href=\"#section_{href}\" color=\"blue\">{name}</a>"),      ''])
            
        colWidths = list(np.array([0.3,0.7])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"Table of context", SECTION_STYLE))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    