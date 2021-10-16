from dataclasses import dataclass

from factorio.game_environment.parsing.types.position import Position


@dataclass
class GridObject:
    item: object
    position: Position
    orientation: int = None