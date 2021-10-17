from factorio.crafting_tree_builder.placeable_types.material_transport import AFluidTransport
from factorio.game_environment.blueprint.types.position import Position


class PipeUnit(AFluidTransport):

    def iterate_connection_spots(self, start_position: Position):
        yield from self.iterate_all_sides(start_position, 1)
