from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode


class VirtualSourceNode(IAssemblerConfig, AMaterialConnectionNode):

    def __init__(self, material: Material, constrained=False):
        super().__init__()
        self.material = material
        self._constrained = constrained
        self._recipe = Recipe(self.material.name, results=MaterialCollection([self.material]))

    @property
    def is_source_step(self):
        return True

    @property
    def is_hidden_node(self) -> bool:
        return False

    def get_node_message(self) -> str:
        return f"{self.material.name} {self.material.amount} items/s"

    @property
    def recipe(self):
        return self._recipe

    @property
    def constrained(self):
        return self._constrained

    @constrained.setter
    def constrained(self, value):
        self._constrained = value

    def get_required_rates(self):
        return MaterialCollection()

    def get_results_rates(self):
        return self._recipe.get_results()

    def set_max_consumers(self, input_materials: MaterialCollection):
        print("WARN! trying to set consumers for source material")

    def set_result_rate(self, material: Material):
        assert self.material.name == material.name
        self.material.amount = material.amount

    def get_id(self):
        return self.material.id

    def set_basic_material_rate(self, material_rate: Material):
        self.set_result_rate(material_rate)
