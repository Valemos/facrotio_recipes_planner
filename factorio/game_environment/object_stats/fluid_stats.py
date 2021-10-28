from dataclasses import dataclass

from factorio.game_environment.object_stats.a_stats import AStats
from factorio.crafting_tree_builder.internal_types.material import Material
from serialization.string_list_json import BasicListJson


@dataclass
class FluidStats(AStats):
    name: str = None
    localised_name: BasicListJson = None
    order: str = None
    default_temperature: int = None
    max_temperature: int = None
    fuel_value: int = None
    emissions_multiplier: float = None

    def to_game_object(self):
        return Material(self.name)
