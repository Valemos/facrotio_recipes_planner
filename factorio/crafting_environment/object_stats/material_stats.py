from factorio.crafting_environment.object_stats.a_stats import AStats
from factorio.crafting_environment.object_stats.item_type import ItemType
from factorio.types.material import Material
from serialization.a_container_json_serializable import AContainerJsonSerializable


class MaterialStats(AStats):
    type: ItemType = ItemType.ITEM
    name: str = ""
    amount: int = 0
    probability: float = None

    def to_object(self) -> Material:
        return Material(self.name, self.amount)


class MaterialStatsList(list, AContainerJsonSerializable):
    __element_type__ = MaterialStats
