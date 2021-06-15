
from factorio.types.material import Material
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.recipe_graph import *
from factorio.recipe_collections import recipes_info


local = CraftingEnvironment(['electronic-circuit', 'copper-plate'])
local.furnace_type = furnace_3

build_recipe_graph(Material("iron-plate", 10000), local)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass