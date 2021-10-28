from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.transport_belt_unit import TransportBeltUnit
from serialization.string_list_json import BasicListJson
from .a_stats import AStats
from ..blueprint.types.color import Color
from ..blueprint.types.direction_type import DirectionType


@dataclass
class TransportBeltStats(AStats):
    __ignored__ = ["energy_source"]

    name: str = None
    localised_name: BasicListJson = None
    belt_speed: float = None
    friendly_map_color: Color = None
    enemy_map_color: Color = None

    def to_game_object(self) -> TransportBeltUnit:
        # 8 items can be on one belt tile at the same time
        return TransportBeltUnit(item_rate=self.belt_speed * 8)
