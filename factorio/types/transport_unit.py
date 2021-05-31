from dataclasses import dataclass
from .material import Material


@dataclass
class TransportUnit(Material):
    item_speed: float = 0


transport_belt_1 = TransportUnit(item_speed=15, id="transport-belt")
transport_belt_2 = TransportUnit(item_speed=30, id="fast-transport-belt")
transport_belt_3 = TransportUnit(item_speed=45, id="express-transport-belt")


