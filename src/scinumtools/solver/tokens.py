from .atom import AtomBase
from .operators import Otype

class Tokens:
    
    atom: AtomBase
    left: list
    right: list
    
    def __init__(self, atom):
        self.atom = atom
        self.left = []
        self.right = []
        
    def append(self, token):
        self.right.append(token)
        
    def get_left(self):
        return self.left.pop() if self.left else None
    
    def get_right(self):
        return self.right.pop(0) if self.right else None
    
    def put_left(self, token):
        self.left.append(token)
        
    def put_right(self, token):
        self.right.insert(0, token)
        
    def operate(self, operators, otype):
        iterator = 0
        while self.right:
            token = self.right.pop(0)
            if isinstance(token, operators) and otype==Otype.UNARY:
                token.operate_unary(self)
            elif isinstance(token, operators) and otype==Otype.BINARY:
                token.operate_binary(self)
            elif isinstance(token, operators) and otype==Otype.ARGS:
                token.operate_args(self)
            else:
                self.put_left(token)
        self.right = self.left
        self.left = []
