import json

from .node_base import BaseNode
from ..datatypes import StringType

class DescriptionNode(BaseNode):
    keyword: str = 'description'

    @staticmethod
    def is_node(parser):
        parser.kwd_description()
        if parser.is_parsed('kwd_description'):
            parser.part_value()
            parser.part_comment()
            return DescriptionNode(parser)
                     
    def parse(self, env):
        if env.nodes[-1].keyword not in ['str','int','float','bool']:
            raise Exception("Description can be set only to str, int, float and bool nodes:", env.nodes[-1].code)
        if env.nodes[-1].description == None:
            env.nodes[-1].description = str(self.value_raw)
        else:
            env.nodes[-1].description += str(self.value_raw)
        return None
