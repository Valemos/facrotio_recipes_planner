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
        result = "\t"*level + repr(self.get_results()) + "\n"
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

    def get_results(self):
        return self.config.get_results_rates()

    def get_required(self):
        return self.config.get_required_rates()

    def iterate_all_steps(self):
        yield self
        
        for prev_step in self.previous_steps:
            yield from prev_step.iterate_all_steps()

    def set_machine_amount_by_inputs(self):
        input_materials = MaterialCollection()
        for prev_step in self.previous_steps:
            input_materials += prev_step.get_results()
        
        self.config.set_maximum_consumers(input_materials)

    def propagate_output_constraints(self):
        current_step: CraftingStep = self.next_step
        while current_step is not None:
            current_step.set_machine_amount_by_inputs()
            current_step = current_step.next_step

    def deduce_infinite_materials(self):
        """
        algorithm assumes, that for each ingredient in this node, there are only one ingredient source node
        """

        required_inputs = self.get_required()
        if len(required_inputs) == 0:
            return

        for ingredient_step in self.previous_steps:
            if ingredient_step.config.producers_amount == float('inf'):
                if ingredient_step.is_start_step():
                    # can cause problem for multiple output recipes
                    requested_material = required_inputs[ingredient_step.get_results().first()]
                    ingredient_step.config.producers_amount = requested_material.amount

                for required_material in required_inputs:
                    if required_material in ingredient_step.get_results():
                        ingredient_step.config.set_material_rate(required_material)
                        ingredient_step.deduce_infinite_materials()
