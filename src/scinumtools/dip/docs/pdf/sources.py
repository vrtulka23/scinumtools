from reportlab.platypus import Paragraph, Table, Spacer, PageBreak, XPreformatted
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import get_formatter_by_name
from pygments.styles import get_style_by_name
from pygments.token import STANDARD_TYPES, Token
import numpy as np
from pathlib import Path
import re

from .settings import *
from ..settings import DocsType
from ...settings import Sign, ROOT_SOURCE
from ...pygments import SyntaxLexer, StyleLexer

class SourcesSection:
    
    data: list
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, data: list):
        self.data = data
        
    def highlight_python_code(self, item):
        # format text using pygments
        lexer = SyntaxLexer()
        style = StyleLexer

        # format text with a lexer
        formatter = get_formatter_by_name('html', style=style) 
        code = highlight(item.code, lexer, formatter)
        
        # add code lines
        lines = code.split(Sign.NEWLINE)
        for l in range(len(lines)-2):  # the last two lines are always empty
            lineno = str(l+1)
            lines[l] = Target(f"{item.target}_{lineno}", f" {lineno:5s}{lines[l]}")
        code = Sign.NEWLINE.join(lines)

        # replace standard CSS classes with explicit text formatting
        token_settings = dict(style)
        for token, class_name in STANDARD_TYPES.items():
            token_style = token_settings[token]
            attributes = []
            if token_style['color']:
                attributes.append(f"color=\"#{token_style['color']}\"")
            attributes = " ".join(attributes)
            code = code.replace(f"class=\"{class_name}\"", attributes)   
        
        # replace DIP specific CSS classes with explicit text formatting
        def replace(m):
            token = getattr(Token.DIP,m.group(1))
            if token not in token_settings:
                return f">{m.group(2)}"
            else:
                token_style = token_settings[token]
                attributes = []
                if token_style['color']:
                    attributes.append(f"color=\"#{token_style['color']}\"")
                attributes = " ".join(attributes)
                if token_style['bold']:
                    return f"{attributes}><b>{m.group(2)}</b>"
                else:
                    return f"{attributes}>{m.group(2)}"
        code = re.sub("class=\" \-DIP \-DIP\-([a-zA-Z]*)\">(.*?)(?=</span)", replace, code)

        return code
    
    def parse_item(self, item):
        
        current_path = Path(item.path)
        
        CODE_STYLE = getSampleStyleSheet()["Code"]
        TABLE_STYLE = [                       
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('BACKGROUND', (0,0), (1,0),   PALETTE['node_name']),  
            ('BACKGROUND', (0,1), (0,-1),   PALETTE['prop_name']),  
            ('BACKGROUND', (1,1), (1,-1),    PALETTE['prop_value']),  
            #('SPAN',       (0,-1), (1,-1)     ),   
        ]


        blocks = []
        p = Paragraph(Target(item.target) + item.name)

        data = [   
            [p,  ''],
            ['File:', current_path.name],
        ]
        if ROOT_SOURCE not in item.name:
            src = Paragraph(Link(item.link_source, f"{item.parent[0]}:{item.parent[1]}"))
            data.append(['Source:', src ])
        t = Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=ColumnWidths([0.2, 0.8]))
        t.keepWithNext = True
        blocks.append(t)

        if not ROOT_SOURCE in item.name:
            code = self.highlight_python_code(item)
            c = XPreformatted(code, CODE_STYLE) 
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(c)
        
        return blocks
        
    def parse(self):
        blocks = []
        blocks.append(Paragraph(Title(f"List of sources"), H2))
        for item in self.data:
            blocks.append(Spacer(1,0.1*inch))
            blocks += self.parse_item(item)
            blocks.append(Spacer(1,0.1*inch))
        blocks.append(Spacer(1,0.2*inch))
        return blocks