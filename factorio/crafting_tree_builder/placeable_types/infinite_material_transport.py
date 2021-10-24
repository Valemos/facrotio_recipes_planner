from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialConnectionNode
from factorio.game_environment.object_stats.material_type import MaterialType


class InfiniteMaterialBus(AMaterialBus):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    @property
    def material_type(self) -> MaterialType:
        return self._material_type


class InfiniteMaterialTransportUnit(AMaterialConnectionNode):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    @property
    def max_rate(self):
        return float("inf")

    @property
    def material_type(self) -> MaterialType:
        return self._material_type

    def create_new_bus(self) -> AMaterialBus:
        return InfiniteMaterialBus(self._material_type)
