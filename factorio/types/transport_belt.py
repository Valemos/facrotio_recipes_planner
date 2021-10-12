from dataclasses import dataclass, field
from .material import Material


@dataclass(frozen=True, eq=True)
class TransportBelt(Material):
    item_rate: float = field(default=0, hash=True)

    def __str__(self):
        return f"Rate: {self.item_rate}"
