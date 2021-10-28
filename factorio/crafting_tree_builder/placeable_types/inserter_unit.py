from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode
from factorio.crafting_tree_builder.placeable_types.a_item_bus_unit import AItemBusUnit
from factorio.crafting_tree_builder.placeable_types.a_sized_grid_object import ASizedGridObject


@dataclass(eq=True, unsafe_hash=True)
class InserterUnit(AMaterialConnectionNode, ASizedGridObject):
    cycle_speed: float = 1
    capacity: float = 1
    range: int = 1

    def __str__(self):
        return f"Inserter Cycle: {self.cycle_speed} Size: {self.capacity} Range: {self.range}"

    @property
    def is_hidden_node(self) -> bool:
        return True

    @property
    def max_rate(self):
        return self.cycle_speed * self.capacity

    def connect_on_grid(self, grid):
        for cell in self.iter_input_cells():
            grid_obj = grid.get(cell)
            if grid_obj is not None:
                self.connect_input(grid_obj)
                break

        for cell in self.iter_output_cells():
            grid_obj = grid.get(cell)
            if grid_obj is not None:
                self.connect_output(grid_obj)
                break

    def iter_object_cells(self):
        yield self.grid_position

    def iter_input_cells(self):
        position = self.grid_position
        for distance in range(1, self.range + 1):
            yield from self.iter_cell_forward(position, distance)

    def iter_output_cells(self):
        position = self.grid_position
        for distance in range(1, self.range + 1):
            yield from self.iter_cell_backward(position, distance)
