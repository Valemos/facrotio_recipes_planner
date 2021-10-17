from dataclasses import dataclass

from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


@dataclass
class AGridObject:
    direction: DirectionType
    position: Position
