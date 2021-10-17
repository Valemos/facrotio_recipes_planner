from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.game_environment.object_stats.material_type import MaterialType


class ItemBus(AMaterialBus):

    @property
    def material_type(self):
        return MaterialType.ITEM


class FluidBus(AMaterialBus):

    @property
    def material_type(self):
        return MaterialType.FLUID
