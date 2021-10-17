from abc import abstractmethod
from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position
from factorio.game_environment.object_stats.material_type import MaterialType


@dataclass
class AMaterialTransport:
    direction: DirectionType = DirectionType.UP
    _material_bus: AMaterialBus = None

    @property
    def material_bus(self) -> AMaterialBus:
        if self._material_bus is None:
            self._material_bus = self.create_new_bus()
            self._material_bus.try_add(self)
        return self._material_bus

    @material_bus.setter
    def material_bus(self, bus):
        if not isinstance(bus, AMaterialBus):
            raise ValueError(f'not a material bus {repr(bus)}')
        self._material_bus = bus

    @property
    @abstractmethod
    def max_rate(self):
        pass

    @property
    @abstractmethod
    def material_type(self) -> MaterialType:
        pass

    @abstractmethod
    def create_new_bus(self) -> AMaterialBus:
        pass

    @abstractmethod
    def iterate_connection_spots(self, start_position: Position):
        pass

    def try_connect(self, other):
        """assumes other object is also AMaterialTransport"""
        if self.material_type == other.material_type:
            AMaterialBus.merge(self.material_bus, other.material_bus)
            return True
        return False

    def iterate_direction_forward(self, start_position, distance=1):
        if self.direction == DirectionType.UP:
            yield start_position.add_y(distance)
        elif self.direction == DirectionType.DOWN:
            yield start_position.add_y(-distance)
        elif self.direction == DirectionType.RIGHT:
            yield start_position.add_x(distance)
        elif self.direction == DirectionType.LEFT:
            yield start_position.add_x(-distance)
        else:
            raise ValueError("incorrect direction")

    def iterate_direction_backward(self, start_position, distance=1):
        yield from self.iterate_direction_forward(start_position, -distance)

    @staticmethod
    def iterate_all_sides(start_position, distance):
        yield start_position.add_y(distance)
        yield start_position.add_y(-distance)
        yield start_position.add_x(distance)
        yield start_position.add_x(-distance)

