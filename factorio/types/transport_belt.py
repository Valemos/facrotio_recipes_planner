from dataclasses import dataclass, field
from .material import Material


@dataclass(frozen=True, eq=True)
class TransportBelt(Material):
    item_speed: float = field(default=0, hash=True)


transport_belt_1 = TransportBelt(item_speed=15, id="transport-belt")
transport_belt_2 = TransportBelt(item_speed=30, id="fast-transport-belt")
transport_belt_3 = TransportBelt(item_speed=45, id="express-transport-belt")


