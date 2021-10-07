from configurations.vanilla_collections import furnace_3
from factorio.recipe_util.recipe_graph import *
from factorio.recipe_util.recipe_json_reading import read_space_exploration


space_recipes = read_space_exploration("./recipes/recipes.json")

local = CraftingEnvironment(['circuit', 'copper plate'], recipes_collection=space_recipes)
local.furnace_type = furnace_3

local.add_constraint_producers_amount("circuit", 1)
build_recipe_graph("circuit", local)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass