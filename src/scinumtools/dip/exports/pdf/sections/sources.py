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

from ..settings import *
from ....settings import DocsType, ROOT_SOURCE
from ....environment import Environment
from ....pygments import SyntaxLexer, StyleLexer, pygments_monkeypatch_style

class SourcesSection:
    
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
        
    def __init__(self, env: Environment):
        self.env = env
        
    def highlight_python_code(self, source):
        # format text using pygments
        lexer = SyntaxLexer()
        pygments_monkeypatch_style("StyleLexer", StyleLexer)
        pygments_style = 'StyleLexer'
        style = get_style_by_name(pygments_style)
        
        # format text with a lexer
        formatter = get_formatter_by_name('html', style=style)
        code = highlight(source.code, lexer, formatter)
        
        # add code lines
        lines = code.split('\n')
        for l in range(len(lines)):
            lineno = str(l+1)
            lines[l] = f"<a name=\"source_{source.name}_{lineno}\"></a>{lineno:5s}{lines[l]}"
        code = '\n'.join(lines)
        
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
    
    def parse_source(self, source):
        
        current_path = Path(source.path)
        
        CODE_STYLE = getSampleStyleSheet()["Code"]
        TABLE_STYLE = [                       
            ('GRID',       (0,1), (-1,-1),  0.5, PALETTE['prop_name']),
            ('BACKGROUND', (0,0), (1,0),   PALETTE['node_name']),  
            ('BACKGROUND', (0,1), (0,1),   PALETTE['prop_name']),  
            ('BACKGROUND', (1,1), (1,1),    PALETTE['prop_value']),  
            #('SPAN',       (0,-1), (1,-1)     ),   
        ]


        blocks = []
        p = Paragraph(f"<a name=\"source_{source.name}\"></a>{source.name}")

        if ROOT_SOURCE in source.name:
            data = [   
                [p,  current_path.name],
            ]
        else:
            if ROOT_SOURCE in source.parent_name:
                link_source = f"#source_{source.parent_name}" 
            else:
                link_source = f"#source_{source.parent_name}_{source.parent_lineno}" 
            src = Paragraph(f"<a href=\"{link_source}\" color=\"blue\">{source.parent_name}:{source.parent_lineno}</a>")
            data = [   
                [p,  current_path.name],
                ['Source:', src ],
            ]
        colWidths = list(np.array([0.3, 0.8])*(PAGE_WIDTH-2*inch))
        t = Table(data, style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
        t.keepWithNext = True
        blocks.append(t)

        if not ROOT_SOURCE in source.name:
            code = self.highlight_python_code(source)
            c = XPreformatted(code, CODE_STYLE) 
            blocks.append(Spacer(1,0.1*inch))
            blocks.append(c)
        
        return blocks
        
    def parse(self):
        blocks = []
        blocks.append(PageBreak())
        blocks.append(Paragraph(f"Sources", SECTION_STYLE))
        for name, source in self.env.sources.items():
            blocks.append(Spacer(1,0.1*inch))
            blocks += self.parse_source(source)
            blocks.append(Spacer(1,0.1*inch))
        blocks.append(Spacer(1,0.2*inch))
        return blocks