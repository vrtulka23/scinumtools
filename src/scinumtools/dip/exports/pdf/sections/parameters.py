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
            ('BACKGROUND', (6,0), (6,0),   PALETTE['inj']),  
            ('BACKGROUND', (7,0), (7,0),   PALETTE['imp']),  
        ]
    
        data = [['Property name', '#', '#', '#', '#', '#', '#', '#']]
        for name in self.names:
            p = Paragraph(AnchorLink(AnchorType.PARAM, name))
            counts = [0, 0, 0, 0, 0, 0, 0]
            for node in self.nodes[name]:
                if DocsType.DECLARATION|DocsType.MODIFICATION in node.docs_type:
                    counts[2] += 1
                elif DocsType.DEFINITION|DocsType.MODIFICATION in node.docs_type:
                    counts[3] += 1
                elif DocsType.DECLARATION in node.docs_type:
                    counts[0] += 1
                elif DocsType.DEFINITION in node.docs_type:
                    counts[1] += 1
                elif DocsType.MODIFICATION in node.docs_type:
                    counts[4] += 1
                if node.value_ref:
                    counts[5] += 1
                if node.isource:
                    counts[6] += 1
                    
            counts = ['' if c==0 else c for c in counts]
            data.append([p]+counts)
        return Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.72, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]))
        
    def parse(self):
        blocks = []       
        blocks.append(Paragraph(AnchorTitle(AnchorType.SECTION,f"Parameter list"), H2))
        blocks.append(self.parse_table())
        blocks.append(Spacer(1,0.2*inch))
        return blocks