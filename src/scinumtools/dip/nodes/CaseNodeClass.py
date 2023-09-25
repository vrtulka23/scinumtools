from . import Node
from ..settings import Sign, Keyword
from ..solvers import LogicalSolver

class CaseNode(Node):
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
        # Solve case
        if self.name.endswith(Sign.CONDITION + Keyword.CASE):
            with LogicalSolver(env) as s:
                if self.value_expr:
                    self.value = s.solve(self.value_expr)
                else:
                    self.value = s.solve(self.value_raw)
        return None
