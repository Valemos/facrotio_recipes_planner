from dataclasses import dataclass

from factorio.game_environment.blueprint.types.position import Position


@dataclass
class Tile(ACompositeJsonSerializable):
    name: str = None
    position: Position = None


class TileList(list, AContainerJsonSerializable):
    __element_type__ = Tile
