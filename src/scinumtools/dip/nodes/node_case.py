import re

from .node_base import BaseNode
from ..settings import Sign, Keyword
from ..solvers import LogicalSolver
from ..datatypes import BooleanType

global case_id
case_id = 0

class CaseNode(BaseNode):
    keyword: str = 'case'

    @staticmethod
    def is_node(parser):
        parser.kwd_case()
        if parser.is_parsed('kwd_case'):
            if parser.name.endswith(Sign.CONDITION + Keyword.CASE):
                parser.part_value()
            parser.part_comment()
            return CaseNode(parser)
            
    def parse(self, env):
        global case_id
        # Solve case
        if self.name.endswith(Sign.CONDITION + Keyword.CASE):
            case_id += 1
            self.name += str(case_id)
            with LogicalSolver(env) as s:
                if self.value_expr:
                    self.value = s.solve(self.value_expr)
                else:
                    self.value = s.solve(self.value_raw)
        elif self.name.endswith(Sign.CONDITION + Keyword.ELSE):
            case_id += 1
            self.name += str(case_id)
            self.value = BooleanType(True)
        return None
