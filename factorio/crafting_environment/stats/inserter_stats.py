from typing import Optional

from factorio.types.inserter_unit import InserterUnit
from serialization.string_list_json import StringListJson
from .a_stats import AStats
from ..objects.misc.color import Color


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

    def to_object(self) -> InserterUnit:
        return InserterUnit(self.name)
