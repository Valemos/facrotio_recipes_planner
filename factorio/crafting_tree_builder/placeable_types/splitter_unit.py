from dataclasses import dataclass
from math import floor

from factorio.crafting_tree_builder.placeable_types.material_transport import AItemTransport
from factorio.game_environment.blueprint.types.position import Position


@dataclass
class SplitterUnit(AItemTransport):
    item_rate: float = 0

    def __str__(self):
        return f"Rate: {self.item_rate}"

    @property
    def max_rate(self):
        return self.item_rate

    def iterate_connection_cells(self):
        obj_cells_generator = self.iterate_object_cells()
        yield from self.iterate_cell_forward_backward(next(obj_cells_generator))
        yield from self.iterate_cell_forward_backward(next(obj_cells_generator))

    def iterate_object_cells(self):
        if self.direction.is_horizontal():
            first = Position(floor(self.position.x), self.position.y)
            yield first
            yield first.add_y(-1)
        elif self.direction.is_vertical():
            first = Position(self.position.x, floor(self.position.y))
            yield first
            yield first.add_x(-1)
        else:
            raise ValueError("unknown direction")

