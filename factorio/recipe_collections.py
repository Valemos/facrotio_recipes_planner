from .types.material import Material
from .types.recipe import CraftStationType, Recipe

import json
from pathlib import Path
from typing import Dict
from itertools import count


with Path("factorio/recipes.json").open() as fin:
    recipes_json = json.load(fin)


fluid_types = set()
basic_ore_types = {"copper-ore", "iron-ore"}
furnace_recipe_types = {"iron-plate", "copper-plate", "steel-plate"}
oil_recipe_types = {"light-oil", "heavy-oil", "petroleum-gas"}
chemical_recipe_types = oil_recipe_types.union({"solid-fuel", "plastic"})

recipes_info: Dict[str, Recipe] = {}
oil_recipes_info: Dict[str, Recipe] = {}

EMPTY_RECIPE = Recipe(0, global_id=0)

recipe_id_counter = count(1)

for item_id, cur_recipe_json in zip(recipe_id_counter, recipes_json):
    if cur_recipe_json['recipe']['time'] is None:
        cur_recipe_json['recipe']['time'] = 0

    if cur_recipe_json['recipe']['yield'] is None:
        cur_recipe_json['recipe']['yield'] = 1

    if cur_recipe_json['type'] == 'Liquid':
        fluid_types.add(cur_recipe_json['id'])

    if cur_recipe_json["id"] in furnace_recipe_types:
        _producer_type = CraftStationType.FURNACE
    elif cur_recipe_json["id"] in chemical_recipe_types:
        _producer_type = CraftStationType.CHEMICAL_PLANT
    else:
        _producer_type = CraftStationType.ASSEMBLING

    recipe = Recipe(time=cur_recipe_json['recipe']['time'], producer_type=_producer_type, global_id=item_id)
    for ingredient in cur_recipe_json['recipe']['ingredients']:
        recipe.add_ingredient(Material.from_dict(ingredient))

    recipe.add_result(Material(cur_recipe_json['id'], cur_recipe_json['recipe']['yield']))

    recipes_info[cur_recipe_json['id']] = recipe


with Path("factorio/recipes_oil.json").open() as fin:
    oil_recipes_json = json.load(fin)


for oil_recipe_id, cur_recipe_json in zip(recipe_id_counter, oil_recipes_json):
    if cur_recipe_json["id"].endswith("-cracking"):
        _producer_type = CraftStationType.CHEMICAL_PLANT
    else:
        _producer_type = CraftStationType.OIL_REFINERY

    recipe = Recipe(time=cur_recipe_json['time'], producer_type=_producer_type, global_id=oil_recipe_id)
    for ingredient in cur_recipe_json['ingredients']:
        recipe.add_ingredient(Material.from_dict(ingredient))

    for result in cur_recipe_json['yield']:
        recipe.add_result(Material.from_dict(result))

    recipes_info[cur_recipe_json["id"]] = recipe
    oil_recipes_info[cur_recipe_json["id"]] = recipe
