from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
import numpy as np
import re

from ..environment import Environment
from ..settings import Order, Sign, Keyword, EnvType
from ..lists import NodeList
from ..nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode

class ExportPDF:
    
    env: Environment
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        pass
    
    def __init__(self, env: Environment, **kwargs):
        if env.envtype != EnvType.DOCS:
            raise Exception("Given environment is not a documentation environment")
        self.env = env
        
        self.PAGE_HEIGHT=defaultPageSize[1]; 
        self.PAGE_WIDTH=defaultPageSize[0]
        styles = getSampleStyleSheet()
        fontName = 'Helvetica'
        fontSize = 10

        self.sectionStyle = ParagraphStyle(
            "SectionTitleStyle",
            parent=styles['Normal'],
            fontName = fontName,
            fontSize = 14,
            spaceAfter = 10
        )
        self.groupStyle = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            fontName=fontName,
            fontSize=12,
            spaceBefore=0, 
            spaceAfter=10,  # Add 20 points of space after the paragraph
        )
        self.tableHeaderStyle = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            fontName=fontName,
            fontSize=fontSize,
            textColor=colors.saddlebrown
        )
        self.tableBodyStyle = ParagraphStyle(
            "CustomStyle",
            parent=styles["Normal"],
            fontName=fontName,
            fontSize=fontSize,
        )
        self.tableStyle = [
            # whole grid
            ('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod),
            ('FONTNAME',   (0,0), (-1,-1),  self.tableBodyStyle.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  self.tableBodyStyle.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  self.tableHeaderStyle.fontSize),
            ('TEXTCOLOR',  (0,0), (-1,0),   colors.saddlebrown),   
            ('BACKGROUND', (0,0), (-1,0),   colors.navajowhite),
            ('ALIGN',      (-2,0),(-1,0),   'RIGHT'),
            # property names
            ('BACKGROUND', (0,1), (0,-1),   colors.antiquewhite),  
            # property values
            ('BACKGROUND', (1,1), (-1,-1),  colors.floralwhite),   
            # parameter name
            ('SPAN',       (0,0), (1,0)     ),                               
        ]
        self.caseStyle = [
            # whole grid
            ('GRID',       (0,0), (-1,-1),  0.5,     colors.goldenrod),
            ('FONTNAME',   (0,0), (-1,-1),  self.tableBodyStyle.fontName),
            ('FONTSIZE',   (0,0), (-1,-1),  self.tableBodyStyle.fontSize),
            # top panel
            ('FONTSIZE',   (0,0), (-1,-1),  self.tableHeaderStyle.fontSize),
            ('BACKGROUND', (0,0), (1,0),    colors.lightgreen),    
            ('BACKGROUND', (1,0), (-1,0),   colors.floralwhite),  
        ]

    def prepare_values(self, node):
        # find out units
        unit = ''
        if node.value and node.value.unit:
            unit = node.value.unit
        elif node.units_raw:
            unit = node.units_raw
        # prepare values, options and data types
        value = None
        options = None
        # boolean node
        if node.keyword == BooleanNode.keyword:
            dtype = node.keyword
            if node.value:
                value = Keyword.TRUE if node.value.value else Keyword.FALSE
        # integer node
        elif node.keyword == IntegerNode.keyword:
            if node.units_raw:
                options = [f"{option.value.value} {option.value.unit}" for option in node.options]
            else:
                options = [f"{option.value.value}" for option in node.options]
            dtype = node.keyword
            if node.value:
                value = str(int(node.value.value))
                if node.value.unsigned:
                    dtype = f"u{dtype}"
                if node.value.precision:
                    dtype = f"{dtype}{node.value.precision}"
        # float node
        elif node.keyword == FloatNode.keyword:
            if node.units_raw:
                options = [f"{option.value.value} {option.value.unit}" for option in node.options]
            else:
                options = [f"{option.value.value}" for option in node.options]
            dtype = node.keyword
            if node.value:
                exp = np.log10(node.value.value)
                if exp<=3 or exp>=-3:
                    value = f"{node.value.value:.03f}"
                else:
                    value = f"{node.value.value:.03e}"
                if node.value.precision:
                    dtype = f"{dtype}{node.value.precision}"
        # string node
        elif node.keyword == StringNode.keyword:
            options = [str(option.value.value) for option in node.options]
            dtype = node.keyword
            if node.value:
                value = str(node.value.value)
            
        return dtype, value, unit, options

    def print_node(self, node, parent_name:str=''):
        # reconstruct a clean node name
        node.name = f"{parent_name}{Sign.SEPARATOR}{node.name}"
        name = f"<strong>{node.clean_name()}</strong>"
        p = Paragraph(name, self.tableHeaderStyle)
        # prepare additional node data
        dtype, value, unit, options = self.prepare_values(node)
        if node.constant:
            dtype = f"constant {dtype}"
        data = [
            [p, '', dtype],
        ]
        # construct a node table
        tableStyle2 = self.tableStyle.copy()
        if value:
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Default value:', Paragraph(value, self.tableBodyStyle)])
        if unit:
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Default unit:', Paragraph(unit, self.tableBodyStyle)])
        if node.condition:
            condition = node.condition
            condition = condition.replace("{","<font color='orange'>{")
            condition = condition.replace("}","}</font>")
            condition = Paragraph(condition, style=self.tableBodyStyle)
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Condition:', condition])
        if node.tags:
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Tags:', Paragraph(", ".join(node.tags), self.tableBodyStyle)])
        if options: 
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Options:', Paragraph(", ".join(options), self.tableBodyStyle)])
        if node.keyword == StringNode.keyword and node.format:
            tableStyle2.append(('SPAN', (1,len(data)), (-1,len(data)) ))
            data.append(['Format:', Paragraph(node.format, self.tableBodyStyle)])
        if node.description:
            tableStyle2.append(('SPAN', (0,-1), (-1,-1) ))
            tableStyle2.append(('BACKGROUND', (0,-1), (-1,-1),  colors.floralwhite))
            data.append([Paragraph(node.description, self.tableBodyStyle)])
        colWidths = list(np.array([0.2, 0.58, 0.22])*(self.PAGE_WIDTH-2*inch))
        t = Table(data,style=tableStyle2, hAlign='LEFT', colWidths=colWidths)
        return t
    
    def collect_blocks(self, nodes, parent_name:str=''):
        blocks = []
        # first list all direct nodes in a group
        for group_name in nodes.keys():
            if parent_name:
                group_path = f"{parent_name}{Sign.SEPARATOR}{group_name}"
            else:
                group_path = group_name
            child = nodes[group_name]
            if isinstance(child, Node):
                blocks.append(self.print_node(child, parent_name))
                blocks.append(Spacer(inch, inch/12))
        # list all subgroups
        for group_name in nodes.keys():
            if parent_name:
                group_path = f"{parent_name}{Sign.SEPARATOR}{group_name}"
            else:
                group_path = group_name
            child = nodes[group_name]
            if isinstance(child, NodeList) and len(child):
                blocks += self.collect_blocks(child, group_path)
        # display case for the current group
        if m := re.match(f".*({Sign.CONDITION}[0-9]+)$", parent_name):
            cid = m.group(1)
            case = self.env.branching.cases[m.group(1)]
            if case.expr:
                condition = case.expr
                condition = condition.replace("{","<font color='orange'>{")
                condition = condition.replace("}","}</font>")
            else:
                condition = ''
            condition = Paragraph(condition, style=self.tableBodyStyle)
            data = [
                [case.case_type, condition],
            ]
            colWidths = list(np.array([0.1, 0.9])*(self.PAGE_WIDTH-2*inch))
            t = Table(data,style=self.caseStyle, hAlign='LEFT', colWidths=colWidths)
            blocks.insert(0, t)
            blocks.insert(1, Spacer(inch, inch/12))
            
            def my_replace(m):
                case = self.env.branching.cases[m.group(1)]
                return f"{case.branch_id}{case.branch_type}"
            parent_name = re.sub(r'\.(@[0-9]+)', my_replace, parent_name)
        # add a title block
        if blocks:
            p = Paragraph(f"<strong>{parent_name}</strong>", self.groupStyle)
            p.keepWithNext = True # Keep title on the same page as parameters
            blocks.insert(0, p)
        return blocks

    def build(self, file_path: str, title, pageinfo):
        
        def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Bold',16)
            canvas.drawCentredString(self.PAGE_WIDTH/2.0, self.PAGE_HEIGHT-108, title)
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch, 0.75 * inch, "First Page / %s" % pageinfo)
            canvas.restoreState()
            
        def myLaterPages(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Roman',9)
            canvas.drawString(inch, 0.75 * inch, "Page %d %s" % (doc.page, pageinfo))
            canvas.restoreState()

        doc = SimpleDocTemplate(file_path)
        blocks = [Spacer(1,1*inch)]

        # list of all nodes
        p = Paragraph(f"Parameter list", self.sectionStyle)
        blocks.append(p)
        nodes = self.env.nodes.query("*")
        parameters = []
        for node in nodes:
            name = node.clean_name()
            if name not in parameters:
                parameters.append(name)
        parameters.sort()
        for name in parameters:
            p = Paragraph(f"<strong>{name}</strong>")
            blocks.append(p)
        blocks.append(Spacer(1,0.2*inch))
        
        # collect all declarations and definitions
        p = Paragraph(f"Declarations and definitions", self.sectionStyle)
        blocks.append(p)
        for block in self.collect_blocks(self.env.nodes):
            blocks.append(block)
        blocks.append(Spacer(1,0.2*inch))

        # modifications
        p = Paragraph(f"Modifications", self.sectionStyle)
        blocks.append(p)
        
        # build a documentation
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
