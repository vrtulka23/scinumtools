from .node_base import BaseNode
from .node_integer import IntegerNode
from .node_float import FloatNode
from .node_string import StringNode

class OptionNode(BaseNode):
    keyword: str = 'option'

    @staticmethod
    def is_node(parser):
        parser.part_equal()    
        if parser.is_parsed('part_equal'):
            parser.part_value()
            parser.part_units()
            parser.part_comment()
            return OptionNode(parser)
        parser.kwd_options()
        if parser.is_parsed('kwd_options'):
            parser.part_value()
            parser.part_units()
            parser.part_comment()
            return OptionNode(parser)
        
    def parse(self, env):
        node = env.nodes[-1]
        if not isinstance(node,(IntegerNode,FloatNode,StringNode)):
            raise Exception(f"Node '{env.nodes[-1].keyword}' does not support options")
        if self.dimension:
            for value in self.cast_value():
                self.value_raw = value
                env.nodes[-1].set_option(self.copy(), env)
        else:
            env.nodes[-1].set_option(self, env)
        return None
