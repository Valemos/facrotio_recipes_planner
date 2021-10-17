from dataclasses import dataclass, field

from factorio.crafting_tree_builder.placeable_types.material_transport import AItemTransport
from factorio.game_environment.blueprint.types.direction_type import DirectionType


@dataclass
class TransportBeltUnit(AItemTransport):
    item_rate: float = field(default=0, hash=True)
    direction: DirectionType = DirectionType.UP

    def __str__(self):
        return f"Rate: {self.item_rate}"

    @property
    def max_rate(self):
        return self.item_rate

    def iterate_object_cells(self):
        yield self.position.round()

    def iterate_connection_cells(self):
        rounded_position = self.position.round()
        yield from self.iterate_direction_forward(rounded_position)
        yield from self.iterate_cell_backward(rounded_position)
