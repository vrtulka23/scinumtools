from .node_base import BaseNode

class ConstantNode(BaseNode):
    keyword: str = 'constant'

    @staticmethod
    def is_node(parser):
        parser.kwd_constant()
        if parser.is_parsed('kwd_constant'):
            parser.part_comment()
            return ConstantNode(parser)
            
    def parse(self, env):
        env.nodes[-1].constant = True
        return None
