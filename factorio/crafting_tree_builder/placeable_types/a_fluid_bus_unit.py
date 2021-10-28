from abc import ABC

from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_bus_unit import AMaterialBusUnit
from factorio.crafting_tree_builder.placeable_types.material_buses import FluidBus
from factorio.game_environment.object_stats.material_type import MaterialType


class AFluidBusUnit(AMaterialBusUnit, ABC):

    @property
    def is_hidden_node(self) -> bool:
        return True

    def get_node_message(self) -> str:
        return ""

    @property
    def material_type(self):
        return MaterialType.FLUID

    def create_new_bus(self) -> AMaterialBus:
        return FluidBus()

    def max_rate(self):
        return float("inf")
