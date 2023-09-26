from .node_base import BaseNode

class GroupNode(BaseNode):
    keyword: str = 'group'

    @staticmethod
    def is_node(parser):
        parser.part_comment()
        if parser.is_empty():
            return GroupNode(parser)
