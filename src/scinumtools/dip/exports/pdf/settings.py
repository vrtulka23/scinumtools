from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from enum import Enum
import numpy as np

from ...settings import ROOT_SOURCE

SAMPLE_STYLE_SHEET = getSampleStyleSheet()

FONT_NAME = 'Helvetica'
FONT_SIZE = 10
PAGE_HEIGHT=defaultPageSize[1]; 
PAGE_WIDTH=defaultPageSize[0]

TABLE_HEADER_STYLE = ParagraphStyle(
    "CustomStyle",
    parent=SAMPLE_STYLE_SHEET["Normal"],
    fontName=FONT_NAME,
    fontSize=FONT_SIZE,
    textColor=colors.saddlebrown
)

TABLE_BODY_STYLE = ParagraphStyle(
    "CustomStyle",
    parent=SAMPLE_STYLE_SHEET["Normal"],
    fontName=FONT_NAME,
    fontSize=FONT_SIZE,
)

PALETTE = {
    'dec':     '#698D3F',
    'def':     '#AABA78',
    'dec/mod': '#D77F33',
    'def/mod': '#DDA15E',
    'mod':     '#FBE974',
    'c4': colors.saddlebrown, #'#',
    'node_name': '#E7CCB1', #colors.navajowhite, 
    'prop_name': '#FAEDCD', #colors.antiquewhite, #'#',
    'prop_value': '#FEFAE0', #colors.floralwhite, #'#',
}

TITLE = ParagraphStyle(
    name = 'Title',
    fontSize = 20,
    leading = 16,
    fontName='Times-Bold',
    spaceAfter=cm,
)

H1 = ParagraphStyle(
    name = 'Heading1',
    fontSize = 18,
    leading = 16,
    fontName='Times-Bold',
    spaceAfter=cm,
)

H2 = ParagraphStyle(
    name = 'Heading2',
    fontSize = 16,
    leading = 14,
    fontName='Times-Bold',
    spaceAfter=cm,
)

class AnchorType(Enum):
    NODE   = 'NODE'
    PARAM  = 'PARAM'
    SOURCE = 'SOURCE'
    INJECT = 'INJECT'
    IMPORT = 'IMPORT'

def _anchor_args(aname:AnchorType, *args):
    if aname == AnchorType.PARAM:
        name = args[0]
        return name, name
    elif aname == AnchorType.NODE:
        name = args[0].name
        source = args[0].source[0]
        lineno = args[0].source[1]
        return f"{name}_{source}_{lineno}", name
    elif aname == AnchorType.INJECT:
        name = args[0].name
        source = args[0].source[0]
        lineno = args[0].source[1]
        return f"{name}_{source}_{lineno}", ' | injected'
    elif aname == AnchorType.IMPORT:
        source, lineno = args[0][0], args[0][1]
        return f"{source}_{lineno}", f" | imported"
    elif aname==AnchorType.SOURCE:
        source, lineno = args[0][0], args[0][1]
        if ROOT_SOURCE in source:
            return f"{source}", f"{source}:{lineno}"
        else:
            return f"{source}_{lineno}", f"{source}:{lineno}"

def AnchorLink(aname:AnchorType, *args):
    key, name = _anchor_args(aname, *args)
    return f"<a href=\"#{aname.value}_{key}\" color=\"blue\">{name}</a>"

def AnchorTarget(aname:AnchorType, *args):
    key, name = _anchor_args(aname, *args)
    return f"<a name=\"{aname.value}_{key}\"></a>"
    
def HighlightReference(text:str):
    text = text.replace("{","<font color='orange'>{")
    text = text.replace("}","}</font>")
    return text
    
def ColumnWidths(ratios: list):
    return list(np.array(ratios)*(PAGE_WIDTH-5.2*cm))