from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np
import re

from ..settings import Sign, Keyword
from ..datatypes import BooleanType

@dataclass
class Case:
    path: str   # case path up to last @ sign
    value: bool # final value of the case
    code: str   # code line with the case
    expr: str   # case expression
    branch_id: str   # branch ID
    case_id: str     # case ID
    case_type: str   # one of the types: case/else/end

@dataclass
class BranchingList:
    state: List[List[str]]  = field(default_factory = list)  # current state
    cases: Dict[str,Case]   = field(default_factory = dict)  # list of cases
    branches: Dict[str,int] = field(default_factory = dict)  # list of branches
    case_id: int = 0
    branch_id: int = 0
    
    def _close_branch(self):
        self.state.pop()
    
    def false_case(self):
        """ Checks if case value is false
        """
        if not self.state:
            return False
        case = self.state[-1][-1]
        return self.cases[case].value.value == False
        
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        if self.state:
            id_old = self.state[-1][-1]
            path_old = self.cases[id_old].path
        else:
            path_old = ''
        if m := re.match(f"(.*{Sign.CONDITION})([0-9]+)$", node.name):
            path_new = m.group(1)
            if node.case_type==Keyword.CASE:
                value = node.value
            elif node.case_type==Keyword.ELSE and self.cases:
                value = node.value 
            elif node.case_type==Keyword.END and self.cases and path_old==path_new:
                self._close_branch()
                return
            else:
                raise Exception(f"Invalid condition:", node.code)
            case_id = fr"{Sign.CONDITION}{m.group(2)}"
            if path_new==path_old:
                self.state[-1].append(case_id)
            else:
                self.branch_id += 1
                self.state.append([case_id])
            part = chr(ord('a')+len(self.state[-1])-1)
            branch_id = f"{Sign.CONDITION}{self.branch_id}{part}"
            self.cases[case_id] = Case(
                path = path_new,
                value = value,
                code = node.code,
                expr = node.value_expr,
                branch_id = branch_id,
                case_id = case_id,
                case_type = node.case_type,
            )
        else:
            raise Exception(f"Invalid condition:", node.code)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.state: # outside of any condition
            return        
        case = self.state[-1][-1]
        if not node.name.startswith(self.cases[case].path): # ending case at lower indent
            self._close_branch()
        if self.state:
            node.case = ({self.state[-1][0]}, {self.state[-1][-1]})
