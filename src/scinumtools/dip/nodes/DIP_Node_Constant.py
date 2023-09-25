from .DIP_Node import Node

class ConstantNode(Node):
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
