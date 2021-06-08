
from factorio.types.material import Material
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.recipe_graph import *
from factorio.recipe_collections import recipes_info


environment = CraftingEnvironment(['electronic-circuit', 'copper-plate', 'iron-plate'])

result = build_recipe_graph(Material('science-pack-3', 2), environment)
print(result)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass