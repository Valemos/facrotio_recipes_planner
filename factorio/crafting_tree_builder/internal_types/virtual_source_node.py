from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode


class VirtualSourceNode(IAssemblerConfig, AMaterialConnectionNode):

    def __init__(self, material: Material, constrained=False):
        super().__init__()
        self._constrained = constrained
        self._output_rates = MaterialCollection([material])

    @property
    def is_source_step(self):
        return True

    @property
    def is_hidden_node(self) -> bool:
        return False

    def get_node_message(self) -> str:
        return '\n'.join(f"{rate.name} {rate.amount:.1f} items/s" for rate in self._output_rates)

    @property
    def recipe(self):
        return Recipe(self._output_rates.first().name, results=self._output_rates)

    @property
    def constrained(self):
        return self._constrained

    @constrained.setter
    def constrained(self, value):
        self._constrained = value

    def get_input_rates(self) -> MaterialCollection:
        return MaterialCollection()

    def get_output_rates(self) -> MaterialCollection:
        return self._output_rates

    def set_output_rates(self, rates: MaterialCollection):
        self._output_rates = rates
