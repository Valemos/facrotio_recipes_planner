from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.material_transport import AItemTransport
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


@dataclass(eq=True, unsafe_hash=True)
class InserterUnit(AItemTransport):
    cycle_speed: float = 1
    capacity: float = 1
    range: int = 1

    def __str__(self):
        return f"Cycle: {self.cycle_speed} Size: {self.capacity}"

    @property
    def max_rate(self):
        return self.cycle_speed * self.capacity

    def iterate_connection_spots(self, start_position: Position):
        if self.direction == DirectionType.UP or self.direction == DirectionType.DOWN:
            yield start_position.add_y(1)
            yield start_position.add_y(-1)
        elif self.direction == DirectionType.LEFT or self.direction == DirectionType.RIGHT:
            yield start_position.add_x(1)
            yield start_position.add_x(-1)
        else:
            raise ValueError(f"cannot understand direction {self.direction.name}")
