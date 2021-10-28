from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode
from factorio.game_environment.object_stats.material_type import MaterialType


class InfiniteMaterialBus(AMaterialBus):

    def __init__(self, material_type: MaterialType) -> None:
        super().__init__()
        self._material_type = material_type

    def get_node_message(self) -> str:
        return ""

    @property
    def material_type(self) -> MaterialType:
        return self._material_type
