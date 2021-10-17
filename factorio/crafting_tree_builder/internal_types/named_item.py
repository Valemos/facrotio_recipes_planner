from dataclasses import dataclass
from typing import Any


@dataclass
class NamedObject:
    name: str = ""
    item: Any = None

    def __str__(self):
        return f"{self.name} {str(self.item)}"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, NamedObject):
            return self.name == other.name
        else:
            raise ValueError(f"incorrect type {repr(other.__class__)}")

    def __hash__(self):
        return hash(self.name)
