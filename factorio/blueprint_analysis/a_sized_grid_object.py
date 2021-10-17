from abc import abstractmethod, ABC
from dataclasses import dataclass

from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


@dataclass
class ASizedGridObject(ABC):
    direction: DirectionType = None
    position: Position = None

    @abstractmethod
    def iterate_object_cells(self):
        pass

    @abstractmethod
    def iterate_connection_cells(self):
        pass

    def iterate_direction_forward(self, position, distance=1):
        if self.direction == DirectionType.UP:
            yield position.add_y(distance)
        elif self.direction == DirectionType.DOWN:
            yield position.add_y(-distance)
        elif self.direction == DirectionType.RIGHT:
            yield position.add_x(distance)
        elif self.direction == DirectionType.LEFT:
            yield position.add_x(-distance)
        else:
            raise ValueError("incorrect direction")

    def iterate_cell_backward(self, position, distance=1):
        yield from self.iterate_direction_forward(position, -distance)

    def iterate_cell_forward_backward(self, position, distance=1):
        if self.direction == DirectionType.UP:
            yield position.add_y(distance)
            yield position.add_y(-distance)
        elif self.direction == DirectionType.DOWN:
            yield position.add_y(-distance)
            yield position.add_y(distance)
        elif self.direction == DirectionType.RIGHT:
            yield position.add_x(distance)
            yield position.add_x(-distance)
        elif self.direction == DirectionType.LEFT:
            yield position.add_x(-distance)
            yield position.add_x(distance)
        else:
            raise ValueError("incorrect direction")

    @staticmethod
    def iterate_all_sides(start_position, distance):
        yield start_position.add_y(distance)
        yield start_position.add_y(-distance)
        yield start_position.add_x(distance)
        yield start_position.add_x(-distance)
