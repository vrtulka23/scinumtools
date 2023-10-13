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
        if m := re.match(fr"(.*{Sign.CONDITION})({Keyword.CASE}|{Keyword.ELSE})$", self.name):
            case_id += 1
            self.name = f"{m.group(1)}{str(case_id)}{m.group(2)}"
            if m.group(2) == Keyword.CASE:
                with LogicalSolver(env) as s:
                    if self.value_expr:
                        self.value = s.solve(self.value_expr)
                    else:
                        self.value = s.solve(self.value_raw)
            elif m.group(2) == Keyword.ELSE:
                self.value = BooleanType(True)
        return None
