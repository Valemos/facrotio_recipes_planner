from factorio.types.material import Material
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.recipe_functions import *
import factorio.types.transport_belt as transport
from factorio.types.production_config import ProductionConfig
from factorio.recipe_collections import recipes_info
from factorio.types.production_unit import assembling_machine_1


environment = CraftingEnvironment(['electronic-circuit', 'copper-plate', 'iron-plate'])
# environment.add_constraint_amount_produced(Material('electronic-circuit', 3))

result = build_recipe_graph(Material('assembling-machine-1', 0.5), environment)
result = build_recipe_graph(Material('assembling-machine-1', 1), environment)
result = build_recipe_graph(Material('assembling-machine-1', 2), environment)
print(result)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass