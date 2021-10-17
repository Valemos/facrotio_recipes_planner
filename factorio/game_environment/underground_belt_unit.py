from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.material_transport import AItemTransport
from factorio.game_environment.blueprint.types.position import Position


@dataclass
class UndergroundBeltUnit(AItemTransport):

    item_rate: float = 0
    range: int = 0

    @property
    def max_rate(self):
        return self.item_rate

    def iterate_connection_cells(self, start_position: Position):
        for distance in range(1, self.range + 1):
            yield from self.iterate_direction_forward(start_position)
