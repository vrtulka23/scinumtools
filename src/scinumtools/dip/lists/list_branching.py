from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np
import re

from ..settings import Sign, Keyword
from ..datatypes import BooleanType

@dataclass
class Case:
    path: str
    value: bool
    code: str

@dataclass
class BranchingList:
    state: List[List[str]]  = field(default_factory = list)  # current state
    cases: Dict[str,Case]   = field(default_factory = dict)  # list of all state

    def false_case(self):
        """ Checks if case value is false
        """
        if not self.state:
            return False
        state = self.state[-1][-1]
        return self.cases[state].value.value == False
        
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        if self.state:
            id_old = self.state[-1][-1]
            path_old = self.cases[id_old].path
        else:
            path_old = ''
        if m := re.match(f"(.*{Sign.CONDITION})(({Keyword.CASE}|{Keyword.ELSE})[0-9]*)$", node.name):
            path_new = m.group(1)
            id_new = fr"{Sign.CONDITION}{m.group(2)}"
            case_new = m.group(3)
            if case_new==Keyword.CASE:
                value = node.value
            elif case_new==Keyword.ELSE and self.cases:
                value = BooleanType(True)
            else:
                raise Exception(f"Invalid condition:", node.code)
            self.cases[id_new] = Case(
                path = path_new,
                value = value,
                code = node.code
            )
            if path_new==path_old:
                self.state[-1].append(id_new)
            else:
                self.state.append([id_new])
        elif self.cases and node.name==path_old + Keyword.END:    # end case using a keyword
            self.state.pop()
        else:
            raise Exception(f"Invalid condition:", node.code)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.state: # outside of any condition
            return        
        state = self.state[-1][-1]
        if not node.name.startswith(self.cases[state].path): # ending case at lower indent
            self.state.pop()
        if self.state:
            node.case = ({self.state[-1][0]}, {self.state[-1][-1]})

            