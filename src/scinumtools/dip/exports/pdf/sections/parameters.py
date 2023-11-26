from reportlab.platypus import Paragraph, Table, Spacer
from reportlab.lib.units import inch
import numpy as np

from ..settings import *
from ....settings import DocsType

class ParametersSection:
    
    names: list
    nodes: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, nodes):
        self.nodes = nodes
        self.names = list(self.nodes.keys())
        self.names.sort()
    
    def parse_table(self):
        TABLE_STYLE = [
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('BACKGROUND', (0,0), (0,0),   PALETTE['node_name']),  
            ('BACKGROUND', (0,1), (-1,-1),   PALETTE['prop_value']),  
            ('BACKGROUND', (1,0), (1,0),   PALETTE['dec']),  
            ('BACKGROUND', (2,0), (2,0),   PALETTE['def']),  
            ('BACKGROUND', (3,0), (3,0),   PALETTE['dec/mod']),  
            ('BACKGROUND', (4,0), (4,0),   PALETTE['def/mod']),  
            ('BACKGROUND', (5,0), (5,0),   PALETTE['mod']),  
        ]
    
        data = [['Property name', '#', '#', '#', '#', '#']]
        for name in self.names:
            p = Paragraph(f"<a href=\"#node_{name}\" color=\"blue\">{name}</a>")
            counts = [0, 0, 0, 0, 0]
            for node in self.nodes[name]:
                if DocsType.DEFINITION|DocsType.MODIFICATION in node.docs_type:
                    counts[3] += 1
                elif DocsType.DEFINITION in node.docs_type:
                    counts[1] += 1
                elif DocsType.DECLARATION|DocsType.MODIFICATION in node.docs_type:
                    counts[2] += 1
                elif DocsType.DECLARATION in node.docs_type:
                    counts[0] += 1
                elif DocsType.MODIFICATION in node.docs_type:
                    counts[4] += 1
            counts = ['' if c==0 else c for c in counts]
            data.append([p]+counts)
        colWidths = list(np.array([0.8, 0.04, 0.04, 0.04, 0.04, 0.04])*(PAGE_WIDTH-2*inch))
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        
    def parse(self):
        blocks = []       
        blocks.append(Paragraph(f"Parameter list", H2))
        blocks.append(self.parse_table())
        blocks.append(Spacer(1,0.2*inch))
        return blocks