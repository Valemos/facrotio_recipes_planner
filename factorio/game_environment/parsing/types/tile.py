from dataclasses import dataclass

from factorio.crafting_tree_builder.objects import Position
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class Tile(ACompositeJsonSerializable):
    name: str = None
    position: Position = None


class TileList(list, AContainerJsonSerializable):
    __element_type__ = Tile
