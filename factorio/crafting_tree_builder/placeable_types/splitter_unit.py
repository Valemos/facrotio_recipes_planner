from dataclasses import dataclass
from math import floor

from factorio.crafting_tree_builder.placeable_types.a_item_bus_unit import AItemBusUnit
from factorio.game_environment.blueprint.types.position import Position


@dataclass
class SplitterUnit(AItemBusUnit):

    def __init__(self, item_rate: float = 0, direction=None, position=None):
        super().__init__(direction, position)
        self.item_rate = item_rate

    def __str__(self):
        return f"Rate: {self.item_rate}"

    @property
    def max_rate(self):
        return self.item_rate

    def iter_input_cells(self):
        obj_cells_generator = self.iter_object_cells()
        yield from self.iter_cell_forward(next(obj_cells_generator))
        yield from self.iter_cell_forward(next(obj_cells_generator))

    def iter_output_cells(self):
        obj_cells_generator = self.iter_object_cells()
        yield from self.iter_cell_backward(next(obj_cells_generator))
        yield from self.iter_cell_backward(next(obj_cells_generator))

    def iter_object_cells(self):
        first = self.grid_position
        if self.direction.is_horizontal():
            yield first
            yield first.add_y(-1)
        elif self.direction.is_vertical():
            yield first
            yield first.add_x(-1)
        else:
            raise ValueError("unknown direction")
