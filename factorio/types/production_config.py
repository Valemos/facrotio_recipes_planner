from copy import deepcopy
from dataclasses import dataclass, field
from .recipe import Recipe
from .material_collection import MaterialCollection
from .item_bus import FixedItemBus, ItemBus
from .material import Material
from .production_unit import ProductionUnit
import math


@dataclass
class ProductionConfig:
    """represents production unit combined with input and output inserters"""

    producer: ProductionUnit
    input: ItemBus
    output: ItemBus

    # not fixed config will be updated later during execution
    producers_amount: float = float('inf')
    constrained: bool = False

    def copy_with_recipe(self, new_recipe: Recipe):
        new_config = deepcopy(self)
        new_config.producer = self.producer.setup(new_recipe)
        return new_config

    def get_required(self):
        return self.producer.get_required_scaled(self.producers_amount)

    def get_required_rates(self):
        return self.producer.get_required_rates(self.producers_amount)

    def get_results(self):
        return self.producer.get_results_scaled(self.producers_amount)

    def get_results_rates(self):
        return self.producer.get_results_rates(self.producers_amount)

    def get_recipe(self):
        return self.producer.recipe
    
    def get_production_rate(self):
        return self._get_config_production_rate(self.producers_amount)

    def set_material_rate(self, material_rate: Material):
        """sets desired material rate if possible"""
        # for recipes with more than one result correcting factor is added to match recipe craft results 
        recipe_results = self.get_recipe().get_results()
        craft_rate = recipe_results.total() * material_rate.amount / recipe_results[material_rate].amount

        self.producers_amount = self._get_machine_amount_for_craft_rate(craft_rate)
    
    def set_basic_material_rate(self, material_rate: Material):
        max_possible_rate = self.output.get_max_rate()
        self.producers_amount = min(material_rate.amount, max_possible_rate)

    def set_maximum_consumers(self, input_material_rate: MaterialCollection):
        """
        producers amount will be calculated from the input of the most scarce resource 
        e.g. minimal craft requirements for all materials
        """

        assert all(material in self.producer.recipe.ingredients for material in input_material_rate)

        # use current producers_amount as max possible at this point
        consumers_amount = self.producers_amount
        for ingredient in input_material_rate:
            max_consumers = self.get_maximum_ingredient_consumers(ingredient)
            if consumers_amount > max_consumers:
                consumers_amount = max_consumers
        
        possible_craft_rate = self._get_config_production_rate(consumers_amount)
        consumers_amount = self._get_machine_amount_for_craft_rate(possible_craft_rate)

        # if all input resources are infinite, producers amount also infinite
        self.producers_amount = consumers_amount

    def get_maximum_ingredient_consumers(self, ingredient_rate: Material):
        """uses certain recipe ingredient rate to calculate minimum amount to producers to consume them all"""

        if ingredient_rate.amount == float('inf'):
            return float('inf')
        
        # to get exactly ingredient_rate.amount items in input collection and scale everything else with it
        craft_input_rates = self.producer.get_required_rates(1)
        rate_scaling = ingredient_rate.amount / craft_input_rates[ingredient_rate].amount
        craft_rate_by_ingredient = self.producer.get_craft_rate() * rate_scaling

        return self._get_machine_amount_for_craft_rate(craft_rate_by_ingredient)

    @staticmethod
    def _warn_rate_too_high(item_name: str, rate: float, bus_type: str = None):
        message = f'WARNING! production config cannot support {item_name} rate = {rate}'
        if bus_type is not None:
            message += f' for {bus_type}'
        print(message)

    def _get_config_production_rate(self, machine_amount: float = 1):
        if machine_amount == float('inf'): return float('inf')

        machine_amount = math.ceil(machine_amount)
        input_required_rate = self.producer.get_required_rates(machine_amount).total()
        production_rate = self.producer.get_results_rates(machine_amount).total()

        # get inserter rates for total production scaling
        input_rate_max = self.input.get_max_rate(machine_amount) 
        output_rate_max = self.output.get_max_rate(machine_amount)
        
        if input_rate_max < input_required_rate:
            production_rate = input_rate_max
        
        if output_rate_max < production_rate:
            production_rate = output_rate_max
        
        return production_rate

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


class SourceProductionConfig(ProductionConfig):

    def __init__(self, recipe: Recipe, item_bus: FixedItemBus, is_constrained=False):
        self.material = recipe.result.first()
        super().__init__(ProductionUnit(1, recipe), item_bus, item_bus, item_bus.max_rate, is_constrained)

    def get_results_rates(self):
        collection = MaterialCollection()
        collection.add(Material(self.material.id, self.output.get_max_rate()))
        return collection

    def get_production_rate(self):
        return self.producers_amount

    def set_material_rate(self, material_rate: Material):
        assert self.material.id == material_rate.id
        self.producers_amount = material_rate.amount
    
    def set_basic_material_rate(self, material_rate: Material):
        self.set_material_rate(material_rate)

    def set_maximum_consumers(self, input_material_rate: MaterialCollection):
        print("WARN! trying to deduce producers amount for source material")
