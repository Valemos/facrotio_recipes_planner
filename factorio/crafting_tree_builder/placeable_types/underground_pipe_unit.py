from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.crafting_tree_builder.placeable_types.a_fluid_bus_unit import AFluidBusUnit
from factorio.game_environment.blueprint.types.loader_type import LoaderType


class UndergroundPipeUnit(AFluidBusUnit):
    range: int = 10
    loader_type: LoaderType = LoaderType.INPUT

    def connect_on_grid(self, grid: ObjectCoordinateGrid):
        for other_pipe_cell in self._iter_connect_cells():
            obj = grid.get(other_pipe_cell)
            if isinstance(obj, UndergroundPipeUnit):
                self.connect_bus(obj)

    def iter_object_cells(self):
        yield self.grid_position

    def iter_input_cells(self):
        if LoaderType.INPUT == self.loader_type:
            yield from self.iter_cell_backward(self.grid_position, 1)
        else:
            yield from tuple()

    def iter_output_cells(self):
        if LoaderType.OUTPUT == self.loader_type:
            yield from self.iter_cell_forward(self.grid_position, 1)
        else:
            yield from tuple()

    def _iter_connect_cells(self):
        pos = self.grid_position
        for distance in range(1, self.range):
            yield from self.iter_cell_forward(pos, distance)
