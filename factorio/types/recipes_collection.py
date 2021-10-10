from itertools import count
from typing import Union

from factorio.types.material import Material
from factorio.types.recipe import Recipe


class RecipesCollection:

    EMPTY_RECIPE = Recipe()

    def __init__(self) -> None:
        self._materials: set[Material] = set()
        self._recipes: set[Recipe] = set()
        self._material_recipe_mapping: dict[str, list[int]] = {}

        self.add_unique_recipe(self.EMPTY_RECIPE)

    def __getitem__(self, key):
        return self.get_material_recipe(key)

    @staticmethod
    def read_from_json(json_objects, read_recipe_function):
        recipes = RecipesCollection()
        for basic_name in json_objects["basic"]:
            basic_recipe = Recipe(name=basic_name)
            basic_recipe.add_result(Material(basic_name))
            recipes.add_unique_recipe(basic_recipe)

        for recipe_json in json_objects["composite"]:
            recipe = read_recipe_function(recipe_json)
            for ingredient in recipe.get_required():
                recipes.add_unique_material_or_skip(ingredient)

            for result in recipe.get_results():
                recipes.add_unique_material_or_skip(result)

            recipes.add_unique_recipe(recipe)
        return recipes

    @property
    def all_recipes(self):
        return self._recipes

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
        recipe_id = recipe.id

        if not self.can_craft(material):
            self._material_recipe_mapping[material.name] = []
        self._material_recipe_mapping[material.name].append(recipe_id)

    def get_recipe(self, recipe_name: str) -> Recipe:
        for recipe in self._recipes:
            if recipe.name == recipe_name:
                return recipe
        raise ValueError(f'no recipe with name "{recipe_name}"')

    def get_material_recipe(self, material: Union[str, Material]):
        recipe_ids = self._material_recipe_mapping[Material.from_obj(material).name]
        return self.get_recipe_by_id(recipe_ids[0])

    def get_recipe_by_id(self, id_):
        for recipe in self._recipes:
            if recipe.id == id_:
                return recipe
        raise ValueError(f'no recipe with id "{id_}"')

    def can_craft(self, ingredient: Material):
        return ingredient.name in self._material_recipe_mapping
