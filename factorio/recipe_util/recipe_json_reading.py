from itertools import count

from factorio.recipe_util.vanilla_collections import fluid_types, furnace_recipe_types, chemical_recipe_types
from factorio.types.material import Material
from factorio.types.recipe import CraftStationType, Recipe


def read_recipes(all_recipes_json) -> tuple[dict[int, Recipe], dict[str, Material]]:
    result_recipes = {}
    result_materials = {}
    material_id_iter = count(100000)

    def add_next_material_or_skip(m):
        if m.name not in result_materials:
            result_materials[m.name] = next(material_id_iter)

    recipe_id_iter = count(1)
    for recipe_json in all_recipes_json:
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

        recipe = Recipe(time=recipe_json['recipe']['time'], producer_type=_producer_type)
        recipe._global_id = next(recipe_id_iter)
        for ingredient in map(Material.from_dict, recipe_json['recipe']['ingredients']):
            add_next_material_or_skip(ingredient)
            recipe.add_ingredient(ingredient)

        recipe_result = Material(recipe_json['id'], recipe_json['recipe']['yield'])
        add_next_material_or_skip(recipe_result)
        recipe.add_result(recipe_result)

        result_recipes[recipe_json['id']] = recipe

    return result_recipes, result_materials
