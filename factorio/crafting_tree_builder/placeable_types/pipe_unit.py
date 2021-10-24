from factorio.crafting_tree_builder.placeable_types.a_fluid_bus_unit import AFluidBusUnit


class PipeUnit(AFluidBusUnit):

    def __str__(self):
        return f'Pos: {str(self.position)}'

    def iter_object_cells(self):
        yield self.grid_position

    def connect_on_grid(self, grid):
        for cell in self.iter_all_sides(self.grid_position, 1):
            obj = grid.get(cell)
            if isinstance(obj, AFluidBusUnit):
                if self.grid_position in obj.iter_input_cells():
                    self.connect_bus(obj)

                if self.grid_position in obj.iter_output_cells():
                    self.connect_bus(obj)

    def iter_input_cells(self):
        yield from self.iter_all_sides(self.grid_position, 1)

    def iter_output_cells(self):
        yield from self.iter_all_sides(self.grid_position, 1)
