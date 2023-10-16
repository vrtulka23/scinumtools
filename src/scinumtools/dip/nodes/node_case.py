import re

from .node_base import BaseNode
from ..settings import Sign, Keyword
from ..solvers import LogicalSolver
from ..datatypes import BooleanType

class CaseNode(BaseNode):
    keyword: str = 'case'
    case_id: int = 0
    case_type: str = None

    @staticmethod
    def is_node(parser):
        parser.kwd_case()
        if parser.is_parsed('kwd_case'):
            if parser.name.endswith(Sign.CONDITION + Keyword.CASE):
                parser.part_value()
            parser.part_comment()
            return CaseNode(parser)
            
    def parse(self, env):
        if m := re.match(fr"(.*{Sign.CONDITION})({Keyword.CASE}|{Keyword.ELSE}|{Keyword.END})$", self.name):
            self.case_id = env.branching.register_case()  # set node case ID
            self.case_type = m.group(2)
            self.name = f"{m.group(1)}{str(self.case_id)}" 
            if m.group(2) == Keyword.CASE:
                with LogicalSolver(env) as s:
                    if self.value_expr:
                        self.value = s.solve(self.value_expr)
                    else:
                        self.value = s.solve(self.value_raw)
            elif m.group(2) == Keyword.ELSE:
                self.value = BooleanType(True)
        return None
