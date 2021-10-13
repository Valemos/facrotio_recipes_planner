import json
from pathlib import Path

from ..types.material import Material
from ..types.material_collection import MaterialCollection
from ..types.recipe import CraftStationType, Recipe
from ..types.recipes_collection import RecipesCollection


def _read_recipe_vanilla(recipe_json):
    from configurations.vanilla_collections import fluid_types, furnace_recipe_types, chemical_recipe_types

    if recipe_json["recipe"]["time"] is None:
        recipe_json["recipe"]["time"] = 0
    if recipe_json["recipe"]["yield"] is None:
        recipe_json["recipe"]["yield"] = 1
    if recipe_json["type"] == "Liquid":
        fluid_types.add(recipe_json["name"])
    if recipe_json["name"] in furnace_recipe_types:
        _producer_type = CraftStationType.FURNACE
    elif recipe_json["name"] in chemical_recipe_types:
        _producer_type = CraftStationType.CHEMICAL_PLANT
    else:
        _producer_type = CraftStationType.ASSEMBLING
    recipe = Recipe(time=recipe_json["recipe"]["time"],
                    producer_type=_producer_type,
                    name=recipe_json["name"],
                    ingredients=MaterialCollection.from_json(recipe_json["recipe"]["ingredients"]))

    recipe.add_result(Material(recipe_json["name"], recipe_json["recipe"]["yield"]))

    return recipe


def _read_json_from_path(path):
    with Path(path).open("r") as fin:
        return json.load(fin)


def read_vanilla_database(path):
    recipes = RecipesCollection()
    for recipe_json in _read_json_from_path(path):
        recipes.add_unique_recipe(_read_recipe_vanilla(recipe_json))
    return recipes


def read_default(path):
    return RecipesCollection.from_json(_read_json_from_path(path))
