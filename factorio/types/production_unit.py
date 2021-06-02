from dataclasses import dataclass
from .recipe import Recipe


@dataclass
class ProductionUnit:
    '''represents one unit of crafting machinery'''

    crafting_speed: float  # amount of work / time unit
    recipe: Recipe = None

    def get_id(self):
        return self.recipe.global_id

    def setup(self, recipe):
        return ProductionUnit(self.crafting_speed, recipe)

    def get_craft_time(self):
        return self.recipe.time / self.crafting_speed

    def get_required_materials(self, amount: float = 1):
        return self.recipe.get_required_materials(amount)

    def get_result_scaled(self, amount: float = 1):
        return self.recipe.get_result_scaled(amount)

    def get_productivity_scaled(self, amount: float):
        return self.recipe.get_result_scaled(amount)


assembling_machine_1 = ProductionUnit(0.5)
assembling_machine_2 = ProductionUnit(0.75)
assembling_machine_3 = ProductionUnit(1.25)
