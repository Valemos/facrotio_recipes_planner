from factorio.recipe_graph.graph import *
from factorio.recipe_util.recipe_json_reading import read_default


space_recipes = read_default("./recipes/recipes.json")

local = VirtualCraftingEnvironment(
    # ['circuit', 'copper plate', 'iron plate', 'steel plate'],
    [],
    assembling_machine_2,
    furnace_2,
    inserter_fast,
    transport_belt_2,
    game_env=space_recipes
)

build_recipe_graph("circuit", local)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass