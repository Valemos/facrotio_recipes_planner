import math

from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit
from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from .material import Material
from .material_collection import MaterialCollection
from .recipe import Recipe
from ..placeable_types.a_material_bus import AMaterialBus
from ..placeable_types.a_material_transport import AMaterialConnectionNode


class VirtualAssemblerGroup(IAssemblerConfig, AMaterialConnectionNode):
    """represents production unit combined with input and output inserters"""

    def __init__(self,
                 assembling_machine: AssemblingMachineUnit = None,
                 recipe: Recipe = None,
                 constrained=False):
        # todo update usages of production config and AssemblingMachineUnit
        super().__init__(None, None)
        self.assembler = assembling_machine
        self._recipe = recipe

        # not fixed config will be updated later during optimization
        self.producers_amount: float = float('inf')
        self._constrained: bool = constrained

    def display_tree(self, level=0):
        result = "\t" * level + self.get_short_description() + "\n"
        child: VirtualAssemblerGroup
        for child in self._inputs:
            result += child.display_tree(level + 1)
        return result

    def get_short_description(self):
        return f'{self.recipe.name} x {self.producers_amount}'

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

    def set_max_consumers(self, input_materials: MaterialCollection):
        pass

    def get_required(self):
        return self.recipe.ingredients * self.producers_amount

    def get_results(self):
        return self.recipe.results * self.producers_amount

    def get_required_rates(self):
        return self.recipe.ingredient_rates * self.assembler.crafting_speed * self.producers_amount

    def get_results_rates(self):
        return self.recipe.result_rates * self.assembler.crafting_speed * self.producers_amount

    def set_material_rate(self, material_rate: Material):
        """sets desired material rate if possible"""
        # for recipes with more than one result correcting factor is added to match recipe craft results
        recipe_results = self.get_results()
        craft_rate = recipe_results.total() * material_rate.amount / recipe_results[material_rate].amount

        self.producers_amount = self._get_machine_amount_for_craft_rate(craft_rate)

    def set_basic_material_rate(self, material_rate: Material):
        max_possible_rate = self.output.max_rate()
        self.producers_amount = min(material_rate.amount, max_possible_rate)

    def set_max_consumers(self, input_material_rates: MaterialCollection):
        """
        producers amount will be calculated from the input of the most scarce resource 
        e.g. minimal craft requirements for all materials
        """

        if not all(material in self.assembler.get_required() for material in input_material_rates):
            raise ValueError(f"collections don't match: \n"
                             f"{str(self.recipe.ingredients)}\n"
                             f"{str(input_material_rates)}")

        # use current producers_amount as max possible at this point
        consumers_amount = self.producers_amount
        for ingredient in input_material_rates:
            max_consumers = self.get_max_consumers(ingredient)
            if consumers_amount > max_consumers:
                consumers_amount = max_consumers
        
        possible_craft_rate = self._get_config_production_rate(consumers_amount)
        consumers_amount = self._get_machine_amount_for_craft_rate(possible_craft_rate)

        # if all input resources are infinite, producers amount also infinite
        self.producers_amount = consumers_amount

    def get_max_consumers(self, ingredient_rate: Material):
        """uses certain recipe ingredient rate to calculate minimum amount to producers to consume them all"""

        if ingredient_rate.amount == float('inf'):
            return float('inf')
        
        # to get exactly ingredient_rate.amount items in input collection and scale everything else with it
        craft_input_rates = self.assembler.get_required_rates(1)
        rate_scaling = ingredient_rate.amount / craft_input_rates[ingredient_rate].amount
        craft_rate_by_ingredient = self.assembler.craft_rate() * rate_scaling

        return self._get_machine_amount_for_craft_rate(craft_rate_by_ingredient)

    def connect_material_bus(self, bus: AMaterialBus):
        # todo connect material bus and save materials supplied by it. add material check logic
        pass

    @staticmethod
    def _warn_rate_too_high(item_name: str, rate: float, bus_type: str = None):
        message = f'WARNING! production config cannot support {item_name} rate = {rate}'
        if bus_type is not None:
            message += f' for {bus_type}'
        print(message)

    def _get_machine_amount_for_craft_rate(self, craft_rate: float):
        """
        resulting productivity rate from self.get_results_rates()
        will match or will be more than provided material
        """

        if craft_rate == float('inf'): return float('inf')

        one_machine_rate = self._get_config_production_rate(1)
        theoretical_machine_amount = math.ceil(craft_rate / one_machine_rate)
        actual_rate = self._get_config_production_rate(theoretical_machine_amount)

        # if conveyour belts cannot support too much
        if actual_rate < craft_rate:
            self._warn_rate_too_high('ingredient', craft_rate, 'output')
            return self._get_machine_amount_for_craft_rate(actual_rate)
        else:
            return theoretical_machine_amount

