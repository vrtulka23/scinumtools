import csv
import json

from .node_base import BaseNode
from .parser import Parser
from . import BooleanNode, IntegerNode, FloatNode, StringNode
from ..settings import Sign

class TableNode(BaseNode):
    keyword: str = 'table'
    
    @staticmethod
    def is_node(parser):
        if parser.keyword=='table':
             parser.part_dimension()
             parser.part_equal()
             if parser.is_parsed('part_equal'): # definition
                 parser.part_value()  
             else:
                 parser.defined = True  # declaration
             parser.part_units()    
             parser.part_comment()
             return TableNode(parser)
         
    def parse(self, env):
        lines = self.value_raw.split(Sign.NEWLINE)
        # Parse nodes from table header
        table = []
        dimension = []
        while len(lines)>0:
            line = lines.pop(0)
            if line.strip()=='':
                break
            # Parse node parameters
            parser = Parser(
                code=line,
                source=self.source
            )
            parser.part_name()      # parse node name
            parser.part_type()      # parse node type
            parser.part_dimension() # parse node type dimension
            parser.part_units()     # parse node units
            if not parser.is_empty():
                raise Exception(f"Incorrect header format: {line}")
            # Initialize actual node
            types = {
                'bool':  BooleanNode,
                'int':   IntegerNode,
                'float': FloatNode,
                'str':   StringNode,
            }
            # Create column
            if parser.keyword in types:
                node = types[parser.keyword](parser)
                node.value_raw = []
                table.append(node)
            else:
                raise Exception(f"Incorrect format or missing empty line after header: {self.code}")
        # Remove whitespaces from all table rows
        for l,line in enumerate(lines):
            lines[l] = line.strip()
            if line=='': del lines[l]
        # Read table and assign its values to the nodes
        ncols = len(table)
        csvtab = csv.reader(lines, delimiter=' ')
        for row in csvtab:
            if len(row)>ncols or len(row)<ncols:
                raise Exception(f"Number of header nodes does not match number of table columns: {ncols} != {len(row)}")
            for c in range(ncols):
                if table[c].dimension:
                    table[c].value_raw.append(json.loads(row[c]))
                else:
                    table[c].value_raw.append(row[c])
        # set additional node parameters
        nodes_new = []
        for node in table:
            nvalues = len(node.value_raw)
            node.dimension = [(nvalues,nvalues)]
            node.name = self.name + Sign.SEPARATOR + node.name
            node.indent = self.indent
            nodes_new.append(node)
        return nodes_new
