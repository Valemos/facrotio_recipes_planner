from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode


class OutputMaterialNode(IAssemblerConfig, AMaterialConnectionNode):

    def __init__(self, material) -> None:
        super().__init__()
        self.material = material

    @property
    def is_hidden_node(self) -> bool:
        return False

    def get_node_message(self) -> str:
        rates = self.get_input_rates()
        return f"{self.material.name} {rates[self.material].amount} total items/s"

    @property
    def recipe(self) -> Recipe:
        return Recipe()

    @property
    def constrained(self) -> bool:
        return False
