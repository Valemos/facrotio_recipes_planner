from dataclasses import dataclass

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

    def iterate_connection_spots(self, start_position: Position):
        # todo define position for splitter according to rotation
        yield from iter([])
