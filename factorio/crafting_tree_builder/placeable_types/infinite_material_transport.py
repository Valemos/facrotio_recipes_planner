from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_bus_unit import AMaterialBusUnit
from factorio.game_environment.object_stats.material_type import MaterialType


class InfiniteMaterialBus(AMaterialBus):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    @property
    def material_type(self) -> MaterialType:
        return self._material_type


class InfiniteMaterialTransportUnit(AMaterialBusUnit):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__(None, None)
        self._material_type = material_type

    def connect_input(self, provider):
        # todo finish this
        pass

    def connect_output(self, consumer):
        # todo finish this
        pass

    @property
    def max_rate(self):
        return float("inf")

    @property
    def material_type(self) -> MaterialType:
        return self._material_type

    def iter_object_cells(self):
        yield from []

    def iter_input_cells(self):
        yield from []

    def create_new_bus(self) -> AMaterialBus:
        return InfiniteMaterialBus(self._material_type)
