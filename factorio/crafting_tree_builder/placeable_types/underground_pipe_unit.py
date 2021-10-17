from factorio.crafting_tree_builder.placeable_types.material_transport import AFluidTransport
from factorio.game_environment.blueprint.types.position import Position


class UndergroundPipeUnit(AFluidTransport):
    range: int = 10

    def iterate_connection_spots(self, start_position: Position):
        for distance in range(1, self.range):
            yield from self.iterate_direction_forward(start_position, distance)
