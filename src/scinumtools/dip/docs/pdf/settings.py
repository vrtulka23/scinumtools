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

def Title(name:str=''):
    return f"<a name=\"SECTION_{name}\"></a>{name}"

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