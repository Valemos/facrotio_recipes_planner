from dataclasses import dataclass

from factorio.game_environment.object_stats.a_stats import AStats
from factorio.game_environment.object_stats.item_type import ItemType
from factorio.crafting_tree_builder.internal_types.material import Material
from serialization.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class MaterialStats(AStats):
    type: ItemType = ItemType.ITEM
    name: str = ""
    amount: int = 0
    probability: float = None

    def to_game_object(self) -> Material:
        return Material(self.name, self.amount)


class MaterialStatsList(list, AContainerJsonSerializable):
    __element_type__ = MaterialStats
