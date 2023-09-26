from .node_base import BaseNode

class EmptyNode(BaseNode):
    keyword: str = 'empty'

    @staticmethod
    def is_node(parser):
        if parser.is_empty():
            return EmptyNode(parser)
        parser.part_comment()
        if parser.is_parsed('part_comment'):
            return EmptyNode(parser)
