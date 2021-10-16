from typing import Optional

from serialization.string_list_json import StringListJson
from .a_stats import AStats
from .effects_dict import EffectsDict
from .resource_category import ResourceCategoryMapping
from factorio.entity_network.assembling_machine import AssemblingMachine
from ..parsing.types.color import Color


class MiningDrillStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    energy_usage: int = None
    mining_speed: float = None
    resource_categories: ResourceCategoryMapping = None
    allowed_effects: EffectsDict = None
    friendly_map_color: Color = None
    enemy_map_color: Color = None
    energy_source: dict = None
    pollution: int = None

    def to_object(self) -> Optional[object]:
        return AssemblingMachine(self.mining_speed)
