from dataclasses import dataclass
import copy

@dataclass
class Type:
    value: str = None
    unit: str = None

    def copy(self):
        """ Copy a new object from self
        """
        return copy.copy(self)