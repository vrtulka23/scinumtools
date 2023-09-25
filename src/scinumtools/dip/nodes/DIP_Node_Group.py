from .DIP_Node import Node

class GroupNode(Node):
    keyword: str = 'group'

    @staticmethod
    def is_node(parser):
        parser.part_comment()
        if parser.is_empty():
            return GroupNode(parser)
