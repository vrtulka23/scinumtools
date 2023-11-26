from reportlab.platypus import Table, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import numpy as np

from ..settings import *
from ....settings import ROOT_SOURCE
from ....environment import Environment

class UnitsSection:
    
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, env: Environment):
        self.env = env
        
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
        for name, unit in self.env.units.items():
            # create source link
            if ROOT_SOURCE in unit['source'][0]:
                link_source = f"#source_{unit['source'][0]}" 
            else:
                link_source = f"#source_{unit['source'][0]}_{unit['source'][1]}" 
            src = Paragraph(f"<a href=\"{link_source}\" color=\"blue\">{unit['source'][0]}:{unit['source'][1]}</a>")
            # add row to the table
            data.append([name, unit['value'], unit['units'], src])
            
        colWidths = list(np.array([0.2,0.2,0.2,0.4])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(f"List of units", H2))
        blocks.append(self.parse_table()) 
        blocks.append(Spacer(1,0.2*inch))
        return blocks
    