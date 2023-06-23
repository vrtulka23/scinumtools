class Expression:
    
    left: str
    expr: str
    right: str
    
    def __repr__(self):
        return f"Expr({self.right.strip()})"
    
    def __init__(self, expr:str):
        self.expr = expr
        self.right = expr
        self.left = ''
        
    def shift(self, nchar:int=1):
        self.left += self.right[:nchar]
        self.right = self.right[nchar:]
        
    def remove(self, string:str):
        self.right = self.right[len(string):]
        
    def pop_left(self):
        left = self.left.strip()
        self.left = ''
        return left
