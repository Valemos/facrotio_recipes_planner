from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialTransport
from factorio.game_environment.object_stats.material_type import MaterialType


class InfiniteMaterialBus(AMaterialBus):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    @property
    def material_type(self) -> MaterialType:
        return self._material_type


class InfiniteMaterialTransport(AMaterialTransport):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    @property
    def max_rate(self):
        return float("inf")

    @property
    def material_type(self) -> MaterialType:
        return self._material_type

    def iterate_connection_spots(self, start_position):
        return

    def create_new_bus(self) -> AMaterialBus:
        return InfiniteMaterialBus(self._material_type)
