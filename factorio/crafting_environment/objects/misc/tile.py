from factorio.crafting_environment.objects.misc.position import Position
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


class Tile(ACompositeJsonSerializable):
    name: str = None
    position: Position = None


class TileList(list, AContainerJsonSerializable):
    __element_type__ = Tile
