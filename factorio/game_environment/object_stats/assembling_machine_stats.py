from dataclasses import dataclass
from functools import lru_cache

from factorio.crafting_tree_builder.objects.assembling_machine import AssemblingMachine
from serialization.string_list_json import StringListJson
from .a_stats import AStats
from .crafting_category import CategoriesMapping
from .effects_dict import EffectsDict
from ..parsing.types.color import Color


@dataclass
class AssemblingMachineStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    type: str = None
    energy_usage: float = None
    ingredient_count: int = None
    crafting_speed: float = None
    crafting_categories: CategoriesMapping = None
    module_inventory_size: int = None
    allowed_effects: EffectsDict = None
    friendly_map_color: Color = None
    enemy_map_color: Color = None
    energy_source: dict = None
    pollution: int = None

    def to_object(self) -> AssemblingMachine:
        return AssemblingMachine(self.crafting_speed)
