from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np
import re

from ..settings import Sign, Keyword
from ..datatypes import BooleanType

@dataclass
class Case:
    path: str        # case path up to last @ sign
    value: bool      # final value of the case
    code: str        # code line with the case
    expr: str        # case expression
    branch_id: str   # branch ID
    branch_part: str # branch part
    case_id: str     # case ID
    case_type: str   # one of the types: case/else/end

@dataclass
class Branch:
    cases: list   = field(default_factory = list)  # list of case IDs
    types: list   = field(default_factory = list)  # list of case types
    nodes: dict   = field(default_factory = dict)  # number of node definitions
    
@dataclass
class BranchingList:
    # branch structure
    state: List[str]           = field(default_factory = list)  # list of openned branches
    branches: Dict[str,Branch] = field(default_factory = dict)  # all branches
    cases: Dict[str,Case]      = field(default_factory = dict)  # all cases

    # counters
    num_cases: int = 0
    num_branches: int = 0

    def _get_branch_id(self):
        """ Get ID of a current branch
        """
        if self.state:
            return self.state[-1]
        else:
            return None

    def _get_case_id(self):
        """ Get ID of a current case
        """
        branch_id = self._get_branch_id()
        return self.branches[branch_id].cases[-1]
        
    def _open_branch(self, case_id):
        """ Start a new branch
        """
        self.num_branches += 1        
        branch_id = f"{Sign.CONDITION}{self.num_branches}"
        self.state.append(branch_id)
        self.branches[branch_id] = Branch([case_id], [Keyword.CASE])
        return 0  # branch_part
    
    def _switch_case(self, case_id, case_type):
        """ Go to a new case withing a branch
        """
        branch_id = self._get_branch_id()
        self.branches[branch_id].cases.append(case_id)
        self.branches[branch_id].types.append(case_type)
        return len(self.branches[branch_id].cases)-1  # branch_part

    def _close_branch(self):
        """ Close current branch
        """
        #if len(self.state)>1:
        #    print(self.state[-1])
        # remove current branch from the state list
        self.state.pop()
       
    def register_case(self):
        """ Add a new case
        """
        self.num_cases += 1
        return self.num_cases
    
    def false_case(self):
        """ Checks if case value is false
        """
        if not self.state:
            return False
        # count number of true cases
        branch = self._get_branch_id()
        num_true = sum([self.cases[c].value==True for c in self.branches[branch].cases])
        # only first `true` case is valid
        case = self._get_case_id()
        return num_true!=1 or self.cases[case].value == False
        
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        if m := re.match(f"(.*{Sign.CONDITION})([0-9]+)$", node.name):
            path_new = m.group(1)
            path_old = ''
            if self.state:
                id_old = self._get_case_id()
                path_old = self.cases[id_old].path
            if node.case_type==Keyword.CASE:
                pass
            elif node.case_type==Keyword.ELSE and self.cases:
                pass
            elif node.case_type==Keyword.END and self.cases and path_old==path_new:
                self._close_branch()
                return
            else:
                raise Exception(f"Invalid condition:", node.code)
            case_id = fr"{Sign.CONDITION}{m.group(2)}"
            if path_new==path_old:  # same branch
                branch_part = self._switch_case(case_id, node.case_type)
            elif path_new<path_old: # lower branch
                # close openned branches unitil the same branch is reached
                while path_new!=path_old:
                    self._close_branch()
                    if self.state:
                        id_old = self._get_case_id()
                        path_old = self.cases[id_old].path
                    else:
                        path_old = ''
                branch_part = self._switch_case(case_id, node.case_type)
            else:                   # new branch
                branch_part = self._open_branch(case_id)
            branch_id = self._get_branch_id()
            self.cases[case_id] = Case(
                path        = path_new,          # path of a new case
                code        = node.code,         # code line
                expr        = node.value_expr,   # case logical expression
                value       = node.value,        # boolean value true/false
                branch_id   = branch_id,         # branch ID
                branch_part = branch_part,       # part on the branch
                case_id     = case_id,           # case ID
                case_type   = node.case_type,    # case type CASE/ELSE/END
            )
        else:
            raise Exception(f"Invalid condition:", node.code)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.state: # outside of any condition
            return
        case = self._get_case_id()
        if not node.name.startswith(self.cases[case].path): # ending case at lower indent
            self._close_branch()
        if self.state:
            node.branch_id = self._get_branch_id()
            node.case_id   = self._get_case_id()
            # Register node to the branch
            branch_id = self._get_branch_id()
            node_name = node.clean_name()
            if node_name in self.branches[branch_id].nodes:
                self.branches[branch_id].nodes[node_name] += 1
            else:
                self.branches[branch_id].nodes[node_name] = 1 
