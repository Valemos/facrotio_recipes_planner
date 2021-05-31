from typing import Dict
from factorio.material_collection import MaterialCollection
from factorio.material import Material
from factorio.recipe import Recipe
import json
from pathlib import Path


with Path("factorio/recipes.json").open() as fin:
    recipes_json = json.load(fin)


recipes_info: Dict[str, Recipe] = {}

for item in recipes_json:
    if item['recipe']['time'] is None:
        item['recipe']['time'] = 0

    if item['recipe']['yield'] is None:
        item['recipe']['yield'] = 1

    recipe = Recipe(time=item['recipe']['time'])
    for ingredient in item['recipe']['ingredients']:
        recipe.add_ingredient(Material.from_dict(ingredient))

    recipe.add_result(Material(item['id'], item['recipe']['yield']))

    recipes_info[item['id']] = recipe
