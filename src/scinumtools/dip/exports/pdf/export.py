from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, KeepTogether 
from reportlab.lib.units import inch
import numpy as np
import re

from .settings import *
from .tpl_node import node_template
from ...environment import Environment
from ...settings import Order, Sign, Keyword, EnvType
from ...lists import NodeList
from ...nodes import Node, BooleanNode, IntegerNode, FloatNode, StringNode

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
        p = Paragraph(name, TABLE_HEADER_STYLE)
        # prepare additional node data
        dtype, value, unit, options = self.prepare_values(node)
        if node.constant:
            dtype = f"constant {dtype}"
        data = [
            [p, '', dtype],
        ]
        node_format = node.format if node.keyword == StringNode.keyword else None
        return node_template(data, value, unit, node.condition, node.tags, options, node.keyword, node_format, node.description)
    
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
            condition = Paragraph(condition, style=TABLE_BODY_STYLE)
            data = [
                [case.case_type, condition],
            ]
            colWidths = list(np.array([0.1, 0.9])*(PAGE_WIDTH-2*inch))
            t = Table(data,style=CASE_STYLE, hAlign='LEFT', colWidths=colWidths)
            blocks.insert(0, t)
            blocks.insert(1, Spacer(inch, inch/12))
            
            def my_replace(m):
                case = self.env.branching.cases[m.group(1)]
                branch_part = chr(ord('a')+case.branch_part)
                return f"{case.branch_id}{branch_part}"
            parent_name = re.sub(r'\.(@[0-9]+)', my_replace, parent_name)
        # add a title block
        if blocks:
            p = Paragraph(f"<strong>{parent_name}</strong>", GROUP_STYLE)
            p.keepWithNext = True # Keep title on the same page as parameters
            blocks.insert(0, p)
        return blocks

    def build(self, file_path: str, title, pageinfo):
        
        def myFirstPage(canvas, doc):
            canvas.saveState()
            canvas.setFont('Times-Bold',16)
            canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, title)
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
        p = Paragraph(f"Parameter list", SECTION_STYLE)
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
        p = Paragraph(f"Declarations and definitions", SECTION_STYLE)
        blocks.append(p)
        for block in self.collect_blocks(self.env.nodes):
            blocks.append(block)
        blocks.append(Spacer(1,0.2*inch))

        # modifications
        p = Paragraph(f"Modifications", SECTION_STYLE)
        blocks.append(p)
        
        # build a documentation
        doc.build(blocks, onFirstPage=myFirstPage, onLaterPages=myLaterPages)    
