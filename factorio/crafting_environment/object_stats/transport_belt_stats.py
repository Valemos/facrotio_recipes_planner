from ..parsing.types.color import Color
from .a_stats import AStats
from factorio.entity_network.transport_belt_unit import TransportBeltUnit
from serialization.string_list_json import StringListJson


class TransportBeltStats(AStats):
    __ignored__ = ["energy_source"]

    name: str = None
    localised_name: StringListJson = None
    belt_speed: float = None
    friendly_map_color: Color = None
    enemy_map_color: Color = None

    def to_object(self) -> TransportBeltUnit:
        # 8 items can be on one belt tile at the same time
        return TransportBeltUnit(self.name, self.belt_speed * 8)
