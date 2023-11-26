from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm

SAMPLE_STYLE_SHEET = getSampleStyleSheet()

FONT_NAME = 'Helvetica'
FONT_SIZE = 10
PAGE_HEIGHT=defaultPageSize[1]; 
PAGE_WIDTH=defaultPageSize[0]
        
SECTION_STYLE = ParagraphStyle(
    "SectionTitleStyle",
    parent=SAMPLE_STYLE_SHEET['Normal'],
    fontName = FONT_NAME,
    fontSize = 14,
    spaceAfter = 10
)

GROUP_STYLE = ParagraphStyle(
    "CustomStyle",
    parent=SAMPLE_STYLE_SHEET["Normal"],
    fontName=FONT_NAME,
    fontSize=12,
    spaceBefore=0, 
    spaceAfter=10,  # Add 20 points of space after the paragraph
)

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

CASE_STYLE = [
    # whole grid
    #('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod),
    ('FONTNAME',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontName),
    ('FONTSIZE',   (0,0), (-1,-1),  TABLE_BODY_STYLE.fontSize),
    # top panel
    ('FONTSIZE',   (0,0), (-1,-1),  TABLE_HEADER_STYLE.fontSize),
    #('BACKGROUND', (0,0), (1,0),    colors.lightgreen),    
    #('BACKGROUND', (1,0), (-1,0),   colors.floralwhite),  
]

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