import math

from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit
from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from .material import Material
from .material_collection import MaterialCollection
from .recipe import Recipe
from ..placeable_types.a_material_connection_node import AMaterialConnectionNode


class VirtualAssemblerGroup(IAssemblerConfig, AMaterialConnectionNode):
    """represents production unit combined with input and output inserters"""

    def __init__(self,
                 assembling_machine: AssemblingMachineUnit = None,
                 recipe: Recipe = None,
                 constrained=False):

        super().__init__()
        self.assembler = assembling_machine
        self._recipe = recipe

        # not fixed config will be updated later during optimization
        self.producers_amount: float = float('inf')
        self._constrained: bool = constrained

    def display_tree(self, level=0):
        result = "\t" * level + self.get_short_description() + "\n"
        child: VirtualAssemblerGroup
        for child in self.get_inputs():
            result += child.display_tree(level + 1)
        return result

    def get_short_description(self):
        return f'{self.recipe.name} x {self.producers_amount}'

    def build_subtrees(self, node_builder):
        if self.is_source_step():
            return

        for ingredient in self.recipe.ingredients:
            child_node: VirtualAssemblerGroup = node_builder.build_material(ingredient)
            self.connect_input(child_node)
            child_node.build_subtrees(node_builder)

    @property
    def recipe(self):
        return self._recipe

    @property
    def constrained(self):
        return self._constrained

    @constrained.setter
    def constrained(self, value: bool):
        self._constrained = value

    @property
    def direction(self):
        return self.assembler.direction

    @property
    def position(self):
        return self.assembler.position

    @direction.setter
    def direction(self, direction):
        self.assembler.direction = direction

    @position.setter
    def position(self, pos):
        self.assembler.direction = pos

    def set_input_rates(self, new_rates: MaterialCollection):

        if not all(material in self.recipe.ingredients for material in new_rates):
            raise ValueError(f"materials don't match: \n{str(self.recipe.ingredients)}\n{str(new_rates)}")

        if len(new_rates) == 0:
            return

        self.producers_amount = min(self.get_max_consumers(ingredient) for ingredient in new_rates)

    def get_output_rates(self) -> MaterialCollection:
        return self.recipe.result_rates * self.assembler.crafting_speed * self.producers_amount

    def set_result_rate(self, target_rate: Material):
        """sets desired material rate if possible"""

        production_rate = self.recipe.results[target_rate].amount / self.get_craft_time()
        self.producers_amount = math.ceil(target_rate.amount / production_rate)

    def get_max_consumers(self, ingredient_consumed: Material):
        """uses certain recipe ingredient rate to calculate minimum amount of producers to consume them all"""

        if ingredient_consumed.amount == float('inf'):
            return float('inf')

        consumed_rate = self.recipe.ingredients[ingredient_consumed].amount / self.get_craft_time()
        return math.ceil(ingredient_consumed.amount / consumed_rate)

    def get_craft_time(self):
        return self.recipe.time * self.assembler.time_multiplier
