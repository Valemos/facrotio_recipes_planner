from typing import Optional

from factorio.crafting_environment.stats.a_stats import AStats
from factorio.types.material import Material
from serialization.a_container_json_serializable import AContainerJsonSerializable
from serialization.enum_json import EnumByValueJson


class MaterialType(EnumByValueJson):
    ITEM = "item"
    FLUID = "fluid"


class MaterialStats(AStats):
    type: MaterialType = MaterialType.ITEM
    name: str = ""
    amount: int = 0
    probability: float = None

    def to_object(self) -> Material:
        return Material(self.name, self.amount)


class MaterialStatsList(list, AContainerJsonSerializable):
    __element_type__ = MaterialStats
