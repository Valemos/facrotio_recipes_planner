from abc import ABC

from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialTransport
from factorio.crafting_tree_builder.placeable_types.material_buses import FluidBus, ItemBus
from factorio.game_environment.object_stats.material_type import MaterialType


class AItemTransport(AMaterialTransport, ABC):

    @property
    def material_type(self):
        return MaterialType.ITEM

    def create_new_bus(self) -> AMaterialBus:
        return ItemBus()


class AFluidTransport(AMaterialTransport, ABC):

    @property
    def material_type(self):
        return MaterialType.FLUID

    def create_new_bus(self) -> AMaterialBus:
        return FluidBus()

    def max_rate(self):
        return float("inf")
