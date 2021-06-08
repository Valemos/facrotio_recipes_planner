from .types.material import Material
from .types.recipe import Recipe

import json
from pathlib import Path
from typing import Dict
from itertools import count


with Path("factorio/recipes.json").open() as fin:
    recipes_json = json.load(fin)


recipes_info: Dict[str, Recipe] = {}
fluid_types = set()
ore_types = {"copper-ore", "iron-ore"}

# empty recipe id is 0
for item_id, item in zip(count(1), recipes_json):
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
