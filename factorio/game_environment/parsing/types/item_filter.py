from dataclasses import dataclass

from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class ItemFilter(ACompositeJsonSerializable):
    name: str = ""
    index: int = 0


class ItemFilterList(list, AContainerJsonSerializable):
    __element_type__ = ItemFilter
