from itertools import count
from typing import Union

from factorio.types.material import Material
from factorio.types.recipe import Recipe


class RecipesCollection:

    EMPTY_RECIPE = Recipe(0)

    def __init__(self) -> None:
        self._materials: set[Material] = set()
        self._recipes: set[Recipe] = set()
        self._material_recipe_mapping: dict[int, list[int]] = {}

        self.add_unique_recipe(self.EMPTY_RECIPE)

    def read_from_json(self, json_objects, read_recipe_function):
        for recipe_json in json_objects:
            recipe = read_recipe_function(recipe_json)
            for ingredient in recipe.get_required():
                self.add_unique_material_or_skip(ingredient)

            for result in recipe.get_results():
                self.add_unique_material_or_skip(result)

            self.add_unique_recipe(recipe)

    def add_unique_recipe(self, recipe: Recipe):
        if recipe in self._recipes:
            raise ValueError("recipe already exists")

        self._recipes.add(recipe)

        for result in recipe.get_results():
            self.add_material_recipe(result, recipe)

    def add_unique_material_or_skip(self, material):
        if material not in self._materials:
            self._materials.add(material)

    def add_material_recipe(self, material: Material, recipe: Recipe):
        material_id = material.id
        recipe_id = recipe.id

        if material_id not in self._material_recipe_mapping:
            self._material_recipe_mapping[material_id] = []
        self._material_recipe_mapping[material_id].append(recipe_id)

    def get_recipe(self, recipe_name: str) -> Recipe:
        for recipe in self._recipes:
            if recipe.name == recipe_name:
                return recipe
        raise ValueError(f'no recipe with name "{recipe_name}"')

    def get_material_recipe(self, material: Union[str, Material]):
        material_id = Material.from_obj(material).id
        recipe_ids = self._material_recipe_mapping[material_id]
        return self.get_recipe_by_id(recipe_ids[0])

    def get_recipe_by_id(self, obj_id):
        for recipe in self._recipes:
            if recipe.id == obj_id:
                return recipe
        raise ValueError(f'no recipe with id "{obj_id}"')
