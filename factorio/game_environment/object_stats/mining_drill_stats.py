from dataclasses import dataclass
from typing import Optional

from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit
from serialization.string_list_json import StringListJson
from .a_stats import AStats
from .effects_dict import EffectsDict
from .resource_category import ResourceCategoryMapping
from ..blueprint.types.color import Color


@dataclass
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

    def to_game_object(self) -> Optional[object]:
        return AssemblingMachineUnit(crafting_speed=self.mining_speed)
