from abc import abstractmethod, ABC

from factorio.deterministic_hash import hash_det
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


class ASizedGridObject(ABC):

    def __init__(self):
        self._direction: DirectionType = DirectionType.NO_DIRECTION
        self._position: Position = Position()

    def __hash__(self):
        return hash_det((self._direction, self._position))

    def __eq__(self, other):
        return self._direction == other.direction and \
                self._position == other.position

    def set_placement(self, position=None, direction=None):
        self.position = position
        self.direction = direction
        return self

    @property
    def direction(self):
        return self._direction

    @property
    def position(self) -> Position:
        return self._position

    @direction.setter
    def direction(self, direction):
        self._direction = direction if direction is not None else DirectionType.NO_DIRECTION

    @position.setter
    def position(self, position):
        self._position = position if position is not None else Position()

    @property
    def grid_position(self):
        return self.position.floor()

    @abstractmethod
    def connect_on_grid(self, grid):
        pass

    @abstractmethod
    def iter_object_cells(self):
        pass

    @abstractmethod
    def iter_input_cells(self):
        pass

    @abstractmethod
    def iter_output_cells(self):
        pass

    def place_on_grid(self, grid):
        for cell in self.iter_object_cells():
            grid.place_object(self, cell)

        self.connect_on_grid(grid)

    def iter_cell_forward(self, position, distance=1):
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

    def iter_cell_backward(self, position, distance=1):
        yield from self.iter_cell_forward(position, -distance)

    def iter_cell_forward_backward(self, position, distance=1):
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
    def iter_all_sides(start_position, distance):
        yield start_position.add_y(distance)
        yield start_position.add_y(-distance)
        yield start_position.add_x(distance)
        yield start_position.add_x(-distance)
