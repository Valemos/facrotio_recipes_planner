from dataclasses import dataclass
from typing import Optional

from factorio.game_environment.object_stats.a_stats import AStats
from factorio.game_environment.object_stats.item_type import ItemType
from factorio.crafting_tree_builder.internal_types.material import Material
from serialization.string_list_json import StringListJson


@dataclass
class ItemStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    type: ItemType = None
    order: str = None
    fuel_value: int = None
    stack_size: int = None
    place_result: str = None

    def to_game_object(self) -> Optional[Material]:
        return Material(self.name)
