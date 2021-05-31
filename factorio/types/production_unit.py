from dataclasses import dataclass
from .recipe import Recipe


@dataclass
class ProductionUnit:
    '''represents one unit of crafting machinery'''

    crafting_speed: float
    recipe: Recipe = None

    def get_id(self):
        return self.recipe.result.get_combined_name()

    def setup(self, recipe):
        return ProductionUnit(self.crafting_speed, recipe)

    def get_requirements(self, product_amount: float = 1):
        return self.recipe.get_requirements(product_amount)

    def craft(self, product_amount: float = 1):
        return self.recipe.craft(product_amount)

    # todo: rethink this function interface using craft amount
    def craft_with_time(self):
        return self.recipe.craft_with_time(self.crafting_speed)


assembling_machine_1 = ProductionUnit(0.5)
assembling_machine_2 = ProductionUnit(0.75)
assembling_machine_3 = ProductionUnit(1.25)
