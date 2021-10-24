from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.a_item_bus_unit import AItemBusUnit
from factorio.game_environment.blueprint.types.loader_type import LoaderType


@dataclass
class UndergroundBeltUnit(AItemBusUnit):

    item_rate: float = 0
    range: int = 0
    loader_type: LoaderType = LoaderType.INPUT

    @property
    def max_rate(self):
        return self.item_rate

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
        for distance in range(1, self.range + 1):
            yield from self.iter_cell_forward(pos, distance)
