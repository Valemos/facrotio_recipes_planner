from itertools import count
from typing import Union

from factorio.types.a_json_savable import AJsonSavable
from factorio.types.material import Material
from factorio.types.material_collection import MaterialCollection
from factorio.types.recipe import Recipe


class RecipesCollection(AJsonSavable):

    EMPTY_RECIPE = Recipe()

    def __init__(self) -> None:
        self._basic_materials: set[str] = set()
        self._recipes: list[Recipe] = []
        self._material_recipe_mapping: dict[str, list[int]] = {}

    def __getitem__(self, key):
        return self.get_material_recipe(key)

    @property
    def recipes(self):
        return self._recipes

    def add_unique_recipe(self, recipe: Recipe):
        if recipe in self._recipes:
            raise ValueError("recipe already exists")

        # remove recipe results are not basic anymore
        for result in recipe.get_results():
            if result in self._basic_materials:
                self._basic_materials.remove(Material.name_from(result))

        self._recipes.append(recipe)

        for result in recipe.get_results():
            self.add_material_recipe(result, recipe)

    def add_unique_basic_material(self, material: Union[str, Material]):
        if Material.name_from(material) in self._basic_materials:
            raise ValueError("basic material already exists")

        self._basic_materials.add(Material.name_from(material))

    def add_material_recipe(self, material: Material, recipe: Recipe):
        recipe_id = recipe.id

        if not self.is_recipe_exists(material):
            self._material_recipe_mapping[material.name] = []
        self._material_recipe_mapping[material.name].append(recipe_id)

    def get_recipe(self, recipe_name: str) -> Recipe:
        for recipe in self._recipes:
            if recipe.name == recipe_name:
                return recipe
        raise ValueError(f'no recipe with name "{recipe_name}"')

    def get_material_recipe(self, material: Union[str, Material]):
        if material in self._basic_materials:
            return self._get_basic_recipe(material)

        recipe_ids = self._material_recipe_mapping[Material.name_from(material)]
        return self.get_recipe_by_id(recipe_ids[0])

    def get_recipe_by_id(self, id_):
        for recipe in self._recipes:
            if recipe.id == id_:
                return recipe
        raise ValueError(f'no recipe with id "{id_}"')

    def is_recipe_exists(self, material: Material):
        return Material.name_from(material) in self._material_recipe_mapping

    def is_material_known(self, material: Material):
        return Material.name_from(material) in self._basic_materials or \
               material.name in self._material_recipe_mapping

    def to_json(self) -> dict:
        return {
            "basic": list(self._basic_materials),
            "composite": [recipe.to_json() for recipe in self._recipes]
        }

    @staticmethod
    def from_json(json_object: dict):
        collection = RecipesCollection()
        for basic in json_object["basic"]:
            collection.add_unique_basic_material(basic)

        for recipe_json in json_object["composite"]:
            collection.add_unique_recipe(Recipe.from_json(recipe_json))

        return collection

    def remove_recipe(self, recipe: Recipe):
        for material in recipe.get_results():
            self.remove_material_recipe_mapping(material, recipe)

        self._recipes.remove(recipe)

    def remove_recipe_by_name(self, name):
        self.remove_recipe(self.get_recipe_by_id(Recipe(name=name).id))

    def remove_material_recipe_mapping(self, material: Material, recipe: Recipe):
        self._material_recipe_mapping[material.name].remove(recipe.id)

    @staticmethod
    def _get_basic_recipe(material):
        return Recipe(name=material, results=MaterialCollection([material]))
