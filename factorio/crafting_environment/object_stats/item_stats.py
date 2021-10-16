from typing import Optional

from factorio.crafting_environment.object_stats.a_stats import AStats
from factorio.crafting_environment.object_stats.item_type import ItemType
from factorio.types.material import Material
from serialization.string_list_json import StringListJson


class ItemStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    type: ItemType = None
    order: str = None
    fuel_value: int = None
    stack_size: int = None
    place_result: str = None

    def to_object(self) -> Optional[Material]:
        return Material(self.name)
