from dataclasses import dataclass, field
from factorio.types.recipe import Recipe
from factorio.types.material import Material
import math
from factorio.types.material_collection import MaterialCollection
from .production_config import ProductionConfig
from typing import List


@dataclass(repr=False)
class CraftingStep:
    config: ProductionConfig

    # reference to steps of type CraftingStep
    next_step: object = None
    previous_steps: List[object] = field(default_factory=list)

    class ConstraintError(Exception):
        def __init__(self, *args: object) -> None:
            super().__init__(*args)

    def __repr__(self, level=0) -> str:
        result = "\t"*level + repr(self.get_result()) + "\n"
        for child in self.previous_steps:
            result += child.__repr__(level+1)
        return result

    def is_start_step(self):
        """returns True if node represents basic resourse in crafting tree"""
        return len(self.previous_steps) == 0

    def is_constrained(self):
        return self.config.fixed

    def set_constrained(self, fixed=True):
        self.config.fixed = fixed

    def get_id(self):
        return self.config.producer.get_id()

    def get_result(self):
        # TODO: update result function to return material output rates
        return self.config.get_craft_result()

    def get_required_materials(self):
        # TODO: update requirements function to return material input rates
        return self.config.get_requirements()

    def iterate_all_steps(self):
        yield self
        
        for prev_step in self.previous_steps:
            yield from prev_step.iterate_all_steps()

    def _get_maximum_craft_amount(self, ingredient: Material, recipe: Recipe) -> float:
        return recipe.get_required_materials()[ingredient].amount / ingredient.amount

    def set_machine_amount_by_inputs(self):
        """
        sets maximum possible craft output count based on resource input
        """

        input_materials = MaterialCollection()
        for prev_step in self.previous_steps:
            input_materials += prev_step.get_result()
        
        # craft amount will be calculated from the most scarce resource on input e.g. minimal craft amount by each material
        craft_amount = float('inf')
        for ingredient in self.get_required_materials():
            possible_craft_amount = self._get_maximum_craft_amount(ingredient, self.config.get_recipe())
            if craft_amount > possible_craft_amount:
                craft_amount = possible_craft_amount
        
        # if all input resources are inf producers amount also infinite
        self.config.producers_amount = math.ceil(craft_amount) if craft_amount != float('inf') else float('inf')

    def propagate_output_constraint(self):
        """
        deduces and changes outputs for next steps in craft chain
        """
        current_step: CraftingStep = self.next_step
        while current_step is not None:
            current_step.set_machine_amount_by_inputs()
            current_step = current_step.next_step

    def deduce_infinite_materials(self):
        """
        algorithm assumes, that for each ingredient in this node, there are only one ingredient source node
        """

        required_inputs = self.get_required_materials()
        if len(required_inputs) == 0:
            return

        for ingredient_step in self.previous_steps:
            if ingredient_step.config.producers_amount == float('inf'):
                for required_material in required_inputs:
                    if required_material in ingredient_step.get_result():
                        ingredient_step.config.set_material_production(required_material)
                        ingredient_step.deduce_infinite_materials()
