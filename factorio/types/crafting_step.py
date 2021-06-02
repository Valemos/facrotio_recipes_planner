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

    def set_fixed(self, fixed):
        self.config.fixed = fixed

    def get_id(self):
        return self.config.machine.get_id()

    def get_result(self):
        return self.config.get_result()

    def get_required_materials(self):
        return self.config.get_required_materials()

    def fixed_nodes_count(self):
        if self.is_start_step():
            return 1 if self.config.fixed else 0

        total = 0
        for child in self.previous_steps:
            total += child.fixed_nodes_count()

        return total + (1 if self.config.fixed else 0)

    def set_machine_amount_sufficient(self):
        """
        sets minimum possible resource count to support next resource production
        next element must be constrained, so it's input can be used in this function for evaluation
        """
        if not self.next_step.is_constrained():
            raise CraftingStep.ConstraintError("next step was not constrained to deduce output")

        required_for_next: MaterialCollection = self.next_step.get_required_materials()
        
        craft_amount = 0
        for output_material in self.get_result():
            required_amount = required_for_next[output_material].amount
            sufficient_craft_amount = required_amount / output_material.amount
            if craft_amount < sufficient_craft_amount:
                craft_amount = sufficient_craft_amount

        self.config.machine_amount = math.ceil(craft_amount)

    def _get_maximum_craft_amount(self, ingredient: Material, recipe: Recipe) -> float:
        return recipe.get_result_amount(ingredient) / ingredient.amount

    def set_machine_amount_by_inputs(self):
        """sets maximum possible craft output count based on resource input"""
        
        # assumed, that crafting tree was built correctly, and all input steps already constrained

        input_materials = MaterialCollection()
        for prev_step in self.previous_steps:
            input_materials += prev_step.get_result()
        
        # craft amount will be calculated from the most scarce resource on input
        craft_amount = float('inf')
        for ingredient in self.get_required_materials():
            possible_craft_amount = self._get_maximum_craft_amount(ingredient, self.config.get_recipe())
            if craft_amount > possible_craft_amount:
                craft_amount = possible_craft_amount
        
        self.config.machine_amount = math.ceil(craft_amount)

    def propagate_output_constraint(self):
        """
        deduces and changes outputs for next steps in craft chain
        """
        current_step: CraftingStep = self.next_step
        while current_step is not None:
            current_step.set_machine_amount_by_inputs()
            current_step = current_step.next_step
