from dataclasses import dataclass
from typing import Any


@dataclass
class NamedItem:
    name: str = ""
    item: Any = None

    def __str__(self):
        return f"{self.name} {str(self.item)}"
