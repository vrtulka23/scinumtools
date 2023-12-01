from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from enum import Enum
import unicodedata
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

NTYPES = [
    ('Declaration',                '#698D3F',),
    ('Definition',                 '#AABA78',),
    ('Declaration / Modification', '#D77F33',),
    ('Definition / Modification',  '#DDA15E',),
    ('Modification',               '#FBE974',),
    ('Injection',                  '#AB88BF',),
    ('Import',                     '#D0BCDC',),
]

PALETTE = {
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

H0 = ParagraphStyle(
    name = 'Heading0',
    fontSize = 18,
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
    SECTION = 'SECTION'

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
    elif aname==AnchorType.SECTION:
        name = args[0]
        return str(unicodedata.normalize('NFD',name)), name

def AnchorLink(aname:AnchorType, *args):
    key, name = _anchor_args(aname, *args)
    return f"<a href=\"#{aname.value}_{key}\" color=\"blue\">{name}</a>"

def AnchorTarget(aname:AnchorType, *args):
    key, name = _anchor_args(aname, *args)
    return f"<a name=\"{aname.value}_{key}\"></a>"
    
def AnchorTitle(aname:AnchorType, *args):
    key, name = _anchor_args(aname, *args)
    return f"<a name=\"{aname.value}_{key}\"></a> {name}"

def Target(key:str, name:str=''):
    return f"<a name=\"{key}\"></a>{name}"
    
def Link(key:str, name:str=''):
    return f"<a href=\"#{key}\" color=\"blue\">{name}</a>"
    
def HighlightReference(text:str):
    text = text.replace("{","<font color='orange'>{")
    text = text.replace("}","}</font>")
    return text
    
def ColumnWidths(ratios: list):
    return list(np.array(ratios)*(PAGE_WIDTH-5.2*cm))