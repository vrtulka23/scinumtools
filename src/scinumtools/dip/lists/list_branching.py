from dataclasses import dataclass, field
from typing import List, Dict, Union
import numpy as np

from ..settings import Sign, Keyword
from ..datatypes import BooleanType

@dataclass
class Part:
    value: bool
    code: str

@dataclass
class Case:
    name: str
    value: bool
    code: str

@dataclass
class BranchingList:
    state: List[str]      = field(default_factory = list)  # current state
    cases: Dict[str,Case] = field(default_factory = dict)  # list of all state

    def false_case(self):
        """ Checks if case value is false
        """
        if not self.state:
            return False
        return self.cases[self.state[-1]].value.value == False
        
    def solve_case(self, node):
        """ Manage condition nodes

        :param node: Condition node
        """
        casename = self.cases[self.state[-1]].name if self.state else ''
        if node.name.endswith(Sign.CONDITION + Keyword.CASE):
            print('A',node)
            if casename+Keyword.CASE!=node.name:   # register new case
                print('B',node)
                cid = f"#{len(self.cases)}"
                self.state.append(cid)
                self.cases[cid] = Case(
                    name = node.name[:-4],
                    value = node.value,
                    code = node.code
                )
            else:
                print('BB',node)
                self.cases[self.state[-1]].value = node.value
                self.cases[self.state[-1]].code = node.code
        elif node.name==casename + Keyword.ELSE:
            print('C',node)
            self.cases[self.state[-1]].value = BooleanType(True)
            self.cases[self.state[-1]].code = node.code
        elif node.name==casename + Keyword.END:    # end case using a keyword
            print('D',node)
            self.state.pop()
        else:
            raise Exception(f"Invalid condition:", node.name)

    def prepare_node(self, node):
        """ Manage parameter nodes in a condition

        :param node: Parameter node
        """
        if not self.state: # outside of any condition
            return        
        if not node.name.startswith(self.cases[self.state[-1]].name): # ending case at lower indent
            self.state.pop()