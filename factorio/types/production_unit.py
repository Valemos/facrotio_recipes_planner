from dataclasses import dataclass
from .recipe import Recipe


@dataclass
class ProductionUnit:
    """represents one unit of crafting machinery"""

    crafting_multiplier: float  # amount of work / time unit
    recipe: Recipe = None

    def __str__(self):
        return f"Rate: {self.crafting_multiplier}"

    def get_id(self):
        return hash(self.recipe.name)

    def setup(self, recipe):
        return ProductionUnit(self.crafting_multiplier, recipe)

    def get_craft_rate(self):
        if self.recipe.time == 0:
            return float("inf")
        return self.crafting_multiplier / self.recipe.time

    def get_required_scaled(self, scale: float = 1):
        return self.recipe.get_required() * scale

    def get_required_rates(self, scale: float = 1):
        required_multiplier = scale * self.get_craft_rate()
        return self.recipe.get_required() * required_multiplier

    def get_results_scaled(self, scale: float = 1):
        return self.recipe.get_results() * scale

    def get_results_rates(self, scale: float = 1):
        result_multiplier = scale * self.get_craft_rate()
        return self.recipe.get_results() * result_multiplier
