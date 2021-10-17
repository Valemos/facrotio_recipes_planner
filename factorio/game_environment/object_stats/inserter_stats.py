from dataclasses import dataclass

from serialization.string_list_json import StringListJson
from .a_stats import AStats
from ..blueprint.types.color import Color
from ...crafting_tree_builder.placeable_types.inserter_unit import InserterUnit


@dataclass
class InserterStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    max_energy_usage: int = None
    inserter_extension_speed: float = None
    inserter_rotation_speed: float = None
    friendly_map_color: Color = None
    enemy_map_color: Color = None
    energy_source: dict = None
    pollution: int = None

    def to_game_object(self) -> InserterUnit:
        empirical_cycle_speed = self.inserter_rotation_speed * -65.97 + 2.04
        return InserterUnit(empirical_cycle_speed)
