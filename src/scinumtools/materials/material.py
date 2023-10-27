from .material_base import MaterialBase
from .solve_material import MaterialSolver

class Material(MaterialBase):
    
    _expr: str
    
    def __str__(self):
        return f"Material({self._expr})"
            
    def __repr__(self):
        return f"Material({self._expr})"
