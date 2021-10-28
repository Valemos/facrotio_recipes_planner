from dataclasses import dataclass

from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.placeable_types.a_item_bus_unit import AItemBusUnit


@dataclass
class SplitterUnit(AItemBusUnit):

    def __init__(self, item_rate: float = 0):
        super().__init__()
        self.item_rate = item_rate
        self._cell_output_rates = MaterialCollection()

    def __str__(self):
        return f"Splitter Rate: {self.item_rate}"

    @property
    def max_rate(self):
        return self.item_rate

    def set_input_rates(self, new_rates: MaterialCollection):
        self._cell_output_rates = new_rates / 2

    def get_output_rates(self) -> MaterialCollection:
        return self._cell_output_rates

    @property
    def is_hidden_node(self) -> bool:
        return True

    def iter_input_cells(self):
        obj_cells_generator = self.iter_object_cells()
        yield from self.iter_cell_backward(next(obj_cells_generator))
        yield from self.iter_cell_backward(next(obj_cells_generator))

    def iter_output_cells(self):
        obj_cells_generator = self.iter_object_cells()
        yield from self.iter_cell_forward(next(obj_cells_generator))
        yield from self.iter_cell_forward(next(obj_cells_generator))

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
