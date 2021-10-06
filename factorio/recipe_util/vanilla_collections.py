from factorio.recipe_util.recipe_json_reading import read_recipes
from factorio.types.recipe import Recipe

import json
from pathlib import Path

with Path("factorio/recipes.json").open() as fin:
    recipes_json = json.load(fin)


fluid_types = set()
basic_ore_types = {"copper-ore", "iron-ore"}
furnace_recipe_types = {"iron-plate", "copper-plate", "steel-plate"}
oil_recipe_types = {"light-oil", "heavy-oil", "petroleum-gas"}
chemical_recipe_types = oil_recipe_types.union({"solid-fuel", "plastic"})

recipes_vanilla, material_ids = read_recipes(recipes_json)

EMPTY_RECIPE = Recipe(0)
EMPTY_RECIPE._global_id = 0
