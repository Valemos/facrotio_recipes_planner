import math

from ..placeable_types.assembling_machine_unit import AssemblingMachineUnit
from ..i_assembler_config import IAssemblerConfig
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
        self.producers_amount: float = 0
        self._constrained: bool = constrained

    @property
    def is_hidden_node(self) -> bool:
        return False

    def get_node_message(self) -> str:
        return f"{self.recipe.name} x {self.producers_amount}"

    def get_legend_message(self):
        return f"{self.assembler.name}\tcrafting speed:{self.assembler.crafting_speed}"

    def display_tree(self, level=0):
        result = "\t" * level + self.get_short_description() + "\n"
        child: VirtualAssemblerGroup
        for child in self.get_inputs():
            result += child.display_tree(level + 1)
        return result

    def get_short_description(self):
        return f'{self.recipe.name} x {self.producers_amount}'

    def build_subtrees(self, environment):
        if self.is_source_step:
            return

        for ingredient in self.get_required_input_rates():
            child_node: VirtualAssemblerGroup = environment.build_material_node(ingredient)
            self.connect_input(child_node)
            if not child_node.is_source_step:
                child_node.build_subtrees(environment)

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

    def set_input_rates(self, rates: MaterialCollection):
        if len(rates) == 0: return
        self.producers_amount = min(self.get_max_consumers(ingredient) for ingredient in rates)

    def set_output_rates(self, rates: MaterialCollection):
        if len(rates) == 0: return
        sufficient_producers = max(self.get_min_producers(output) for output in rates if output in self.recipe.results)
        self.producers_amount = max(self.producers_amount, sufficient_producers)

    def propagate_sufficient_inputs(self):
        consumed_rates = self.get_required_input_rates()

        for inp in self.get_inputs():
            inp.set_output_rates(consumed_rates)
            inp.propagate_sufficient_inputs()

    def get_required_input_rates(self):
        return self.recipe.ingredients / self.get_craft_time() * self.producers_amount

    def get_output_rates(self) -> MaterialCollection:
        return self.recipe.results / self.get_craft_time() * self.producers_amount

    def set_result_material_rate(self, target_rate: Material):
        production_rate = self.recipe.results[target_rate].amount / self.get_craft_time()
        self.producers_amount = math.ceil(target_rate.amount / production_rate)

    def get_max_consumers(self, input_rate: Material):
        """uses certain recipe ingredient rate to calculate minimum amount of producers to consume them all"""

        if input_rate.amount == float('inf'):
            return float('inf')

        consumed_rate = self.recipe.ingredients[input_rate].amount / self.get_craft_time()
        return math.ceil(input_rate.amount / consumed_rate)

    def get_min_producers(self, output_rate: Material):
        """uses certain recipe output rate to calculate maximum needed amount of producers to satisfy demand"""

        if output_rate not in self.recipe.results:
            raise ValueError(f"material {output_rate.name} not found in recipe results {self.recipe.name}")

        if output_rate.amount == float('inf'):
            return float('inf')

        consumed_rate = self.recipe.results[output_rate].amount / self.get_craft_time()
        if consumed_rate > 0:
            return math.ceil(output_rate.amount / consumed_rate)
        else:
            return 0

    def get_craft_time(self):
        return self.recipe.time * self.assembler.time_multiplier
