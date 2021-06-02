from dataclasses import dataclass
from .material import Material


@dataclass(frozen=True)
class TransportBelt(Material):
    item_speed: float = 0


transport_belt_1 = TransportBelt(item_speed=15, id="transport-belt")
transport_belt_2 = TransportBelt(item_speed=30, id="fast-transport-belt")
transport_belt_3 = TransportBelt(item_speed=45, id="express-transport-belt")


