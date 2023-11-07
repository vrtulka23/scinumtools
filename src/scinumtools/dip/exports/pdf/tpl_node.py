from reportlab.platypus import Paragraph, Table
from reportlab.lib.units import inch
import numpy as np

from .settings import *

def node_template(data, value, unit, condition, tags, options, keyword, node_format, node_description):

    TABLE_STYLE = [
        # whole grid
        #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod),
        ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
        ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
        # top panel
        ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
        ('TEXTCOLOR',  (0,0), (-1,0),   colors.saddlebrown),   
        #('BACKGROUND', (0,0), (-1,0),   colors.navajowhite),
        ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
        # property names
        #('BACKGROUND', (0,1), (0,-1),   colors.antiquewhite),  
        # property values
        #('BACKGROUND', (1,1), (-1,-1),  colors.floralwhite),   
        # parameter name
        ('SPAN',       (0,0), (1,0)     ),                               
    ]
    
    # construct a node table
    if value:
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Default value:', Paragraph(value, TABLE_BODY_STYLE)])
    if unit:
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Default unit:', Paragraph(unit, TABLE_BODY_STYLE)])
    if condition:
        condition = condition.replace("{","<font color='orange'>{")
        condition = condition.replace("}","}</font>")
        condition = Paragraph(condition, style=TABLE_BODY_STYLE)
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Condition:', condition])
    if tags:
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Tags:', Paragraph(", ".join(tags), TABLE_BODY_STYLE)])
    if options: 
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Options:', Paragraph(", ".join(options), TABLE_BODY_STYLE)])
    if node_format:
        TABLE_STYLE.append(('SPAN', (1,len(data)), (-1,len(data)) ))
        data.append(['Format:', Paragraph(node_format, TABLE_BODY_STYLE)])
    if node_description:
        TABLE_STYLE.append(('SPAN', (0,-1), (-1,-1) ))
        #TABLE_STYLE.append(('BACKGROUND', (0,-1), (-1,-1),  colors.floralwhite))
        data.append([Paragraph(node_description, TABLE_BODY_STYLE)])
    colWidths = list(np.array([0.2, 0.58, 0.22])*(PAGE_WIDTH-2*inch))
    
    return Table(data,style=TABLE_STYLE, hAlign='LEFT', colWidths=colWidths)
