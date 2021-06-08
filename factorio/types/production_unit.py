from dataclasses import dataclass
from .recipe import Recipe


@dataclass
class ProductionUnit:
    '''represents one unit of crafting machinery'''

    crafting_multiplier: float  # amount of work / time unit
    recipe: Recipe = None

    def get_id(self):
        return self.recipe.global_id

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


assembling_machine_inf = ProductionUnit(float('inf'), Recipe(0, global_id=0))
assembling_machine_1 = ProductionUnit(0.5)
assembling_machine_2 = ProductionUnit(0.75)
assembling_machine_3 = ProductionUnit(1.25)

furnace_1 = ProductionUnit(1)
furnace_2 = ProductionUnit(2)
furnace_3 = ProductionUnit(2)
