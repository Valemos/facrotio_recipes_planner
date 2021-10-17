from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property

from factorio.blueprint_analysis.a_grid_object import AGridObject
from factorio.crafting_tree_builder.internal_types.recipe import Recipe


@dataclass
class AssemblingMachineUnit(AGridObject):
    """represents one unit of crafting machinery"""

    crafting_speed: float = 0  # amount of work / time unit
    recipe: Recipe = None

    def __str__(self):
        return f"Rate: {self.crafting_speed}"

    def get_id(self):
        return hash(self.get_recipe().name)

    def get_recipe(self):
        if self.recipe is not None:
            return self.recipe
        else:
            raise ValueError("no recipe was provided to craft station")

    def copy_with_recipe(self, recipe):
        copied = deepcopy(self)
        copied.recipe = recipe
        return copied

    @cached_property
    def craft_rate(self):
        if self.get_recipe().time == 0:
            return float("inf")
        return self.crafting_speed / self.get_recipe().time

    def get_required(self, scale: float = 1):
        return self.get_recipe().get_required() * scale

    def get_required_rates(self, scale: float = 1):
        return self.get_recipe().get_required() * scale * self.craft_rate

    def get_results(self, scale: float = 1):
        return self.get_results() * scale

    def get_results_rates(self, scale: float = 1):
        return self.get_results() * scale * self.craft_rate
