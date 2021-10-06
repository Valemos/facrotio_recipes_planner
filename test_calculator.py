from factorio.recipe_util.recipe_graph import *


local = CraftingEnvironment(['electronic-circuit', 'copper-plate'])
local.furnace_type = furnace_3

local.add_constraint_producers_amount("utility-science-pack", 1)
build_recipe_graph("utility-science-pack", local)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass