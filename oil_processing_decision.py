# maximize yield of all oil derived liquids

from factorio.types.recipe import Recipe
from decision_making.strategy import *
from decision_making.option_tree_builder import *
from decision_making.strategy_operations import *
from decision_making.optimisation import get_pareto_optimal

from factorio.recipe_util.vanilla_collections import oil_recipes_info, recipes_vanilla
from factorio.types.material_collection import Material
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.types.production_unit import assembling_machine_2, furnace_2
from factorio.types.inserter_unit import inserter_fast
from factorio.types.transport_belt import transport_belt_2


environment = CraftingEnvironment(
    ['electronic-circuit', 'advanced-circuit', 'copper-plate', 'iron-plate', 'steel-plate'],
    assembling_machine_2,
    furnace_2,
    inserter_fast,
    transport_belt_2
)

class FactoryStep(BaseStep):
    
    def __init__(self, recipe: Recipe) -> None:
        self.recipe = recipe
        self.config = environment.get_production_config(recipe)
    
    def get_id(self):
        return self.recipe._global_id

    

option_builder = OptionTreeBuilder(FactoryStep)


rocket_fuel_rate = Material('rocket-fuel', 1)
oil_steps = [FactoryStep(rec) for rec in oil_recipes_info.values()]

option_builder.add_branches(FactoryStep(recipes_vanilla["crude-oil"]))



def criteria(strategy: Strategy):
    return 0


print("optimal solution")
solutions = get_pareto_optimal(get_all_strategies(option_builder.get_tree()), criteria)
