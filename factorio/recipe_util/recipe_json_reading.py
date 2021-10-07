import json
from pathlib import Path

from ..types.material import Material
from ..types.recipe import CraftStationType, Recipe
from ..types.recipes_collection import RecipesCollection


def _read_recipe_vanilla(recipe_json):
    from configurations.vanilla_collections import fluid_types, furnace_recipe_types, chemical_recipe_types

    if recipe_json['recipe']['time'] is None:
        recipe_json['recipe']['time'] = 0
    if recipe_json['recipe']['yield'] is None:
        recipe_json['recipe']['yield'] = 1
    if recipe_json['type'] == 'Liquid':
        fluid_types.add(recipe_json['id'])
    if recipe_json["id"] in furnace_recipe_types:
        _producer_type = CraftStationType.FURNACE
    elif recipe_json["id"] in chemical_recipe_types:
        _producer_type = CraftStationType.CHEMICAL_PLANT
    else:
        _producer_type = CraftStationType.ASSEMBLING
    recipe = Recipe(time=recipe_json['recipe']['time'], producer_type=_producer_type, name=recipe_json['id'])

    for material in map(Material.from_dict, recipe_json['recipe']['ingredients']):
        recipe.add_ingredient(material)

    recipe.add_result(Material(recipe_json['id'], recipe_json['recipe']['yield']))

    return recipe


def _read_recipe_space_exploration(recipe_json):
    recipe = Recipe(time=recipe_json["time"],
                    producer_type=CraftStationType[recipe_json["craft_type"]],
                    name=recipe_json["id"])

    for ingredient in map(Material.from_dict, recipe_json["ingredients"]):
        recipe.add_ingredient(ingredient)

    for result in map(Material.from_dict, recipe_json["products"]):
        recipe.add_result(result)

    return recipe


def _read_json_from_path(path):
    with Path(path).open("r") as fin:
        return json.load(fin)


def _collection_from_json(path, function):
    collection = RecipesCollection()
    collection.read_from_json(_read_json_from_path(path), function)
    return collection


def read_vanilla(path):
    return _collection_from_json(path, _read_recipe_vanilla)


def read_space_exploration(path):
    return _collection_from_json(path, _read_recipe_space_exploration)
