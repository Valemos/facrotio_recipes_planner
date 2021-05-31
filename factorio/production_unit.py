from dataclasses import dataclass
from .recipe import Recipe
from factorio import recipe


@dataclass
class ProductionUnit:
    crafting_speed: float
    recipe: Recipe = None

    def get_id(self):
        return self.recipe.result.items[0].id

    def setup(self, recipe):
        return ProductionUnit(self.crafting_speed, recipe)

    def craft(self):
        return self.recipe.craft()

    # todo: rethink this function interface using craft amount
    def craft_with_time(self):
        return self.recipe.craft_with_time(self.crafting_speed)


assembling_machine_1 = ProductionUnit(0.5)
assembling_machine_2 = ProductionUnit(0.75)
assembling_machine_3 = ProductionUnit(1.25)
