from .types.material import Material
from .types.recipe import Recipe

import json
from pathlib import Path
from typing import Dict
from itertools import count


with Path("factorio/recipes.json").open() as fin:
    recipes_json = json.load(fin)


fluid_types = set()
basic_ore_types = {"copper-ore", "iron-ore"}
oil_derived_types = {"light-oil", "heavy-oil", "petroleum-gas"}

recipes_info: Dict[str, Recipe] = {}
oil_recipes_info: Dict[str, Recipe] = {}

# empty recipe id is 0
recipe_id_counter = count(1)

for item_id, item in zip(recipe_id_counter, recipes_json):
    if item['recipe']['time'] is None:
        item['recipe']['time'] = 0

    if item['recipe']['yield'] is None:
        item['recipe']['yield'] = 1

    if item['type'] == 'Liquid':
        fluid_types.add(item['id'])

    recipe = Recipe(time=item['recipe']['time'], global_id=item_id)
    for ingredient in item['recipe']['ingredients']:
        recipe.add_ingredient(Material.from_dict(ingredient))

    recipe.add_result(Material(item['id'], item['recipe']['yield']))

    recipes_info[item['id']] = recipe


with Path("factorio/recipes_oil.json").open() as fin:
    oil_recipes_json = json.load(fin)


for oil_recipe_id, item in zip(recipe_id_counter, oil_recipes_json):
    recipe = Recipe(time=item['time'], global_id=oil_recipe_id)
    for ingredient in item['ingredients']:
        recipe.add_ingredient(Material.from_dict(ingredient))

    for result in item['yield']:
        recipe.add_result(Material.from_dict(result))

    oil_recipes_info[item["id"]] = recipe
