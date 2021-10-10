from configurations.vanilla_collections import assembling_machine_2, furnace_2, inserter_fast, \
    transport_belt_2
from factorio.recipe_util.recipe_graph import *
from factorio.recipe_util.recipe_json_reading import read_space_exploration


space_recipes = read_space_exploration("./recipes/recipes.json")

local = CraftingEnvironment(
    # ['circuit', 'copper plate', 'iron plate', 'steel plate'],
    [],
    assembling_machine_2,
    furnace_2,
    inserter_fast,
    transport_belt_2,
    recipes_collection=space_recipes
)

build_recipe_graph("circuit", local)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass