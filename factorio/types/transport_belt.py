from dataclasses import dataclass, field
from .material import Material


@dataclass(frozen=True, eq=True)
class TransportBelt(Material):
    item_rate: float = field(default=0, hash=True)


transport_belt_inf = TransportBelt(item_rate=float('inf'), name="")
transport_belt_1 = TransportBelt(item_rate=15, name="transport-belt")
transport_belt_2 = TransportBelt(item_rate=30, name="fast-transport-belt")
transport_belt_3 = TransportBelt(item_rate=45, name="express-transport-belt")


