from typing import Union

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from serialization.i_json_serializable import IJsonSerializable


class RecipesCollection(IJsonSerializable):

    EMPTY_RECIPE = Recipe()

    def __init__(self) -> None:
        self._basic_materials: set[str] = set()
        self._recipes: dict[str, Recipe] = {}
        self._material_recipe_mapping: dict[str, list[int]] = {}

    def __getitem__(self, key):
        return self.get_material_recipe(key)

    def __eq__(self, other):
        return self._recipes == other._recipes and \
               self._basic_materials == other._basic_materials

    @property
    def recipes(self):
        return self._recipes

    @property
    def recipe_names_iter(self):
        return (name for name in self._recipes.keys())

    def add_unique_recipe(self, recipe: Recipe):
        if recipe in self._recipes:
            print(f'recipe "{recipe.name}" already exists')
            return

        self._recipes[recipe.name] = recipe

        # recipe results are not basic materials anymore
        for result in recipe.get_results():
            if result in self._basic_materials:
                self._basic_materials.remove(Material.name_from(result))

        self._create_recipe_mappings(recipe)

    def add_unique_basic_material(self, material: Union[str, Material]):
        if Material.name_from(material) in self._basic_materials:
            print(f'basic material "{material}" already exists')
            return

        self._basic_materials.add(Material.name_from(material))

    def add_material_recipe(self, material: Material, recipe: Recipe):
        recipe_id = recipe.get_id()

        if not self.is_recipe_exists(material):
            self._material_recipe_mapping[material.name] = []
        self._material_recipe_mapping[material.name].append(recipe_id)

    def get_recipe(self, recipe_name: str) -> Recipe:
        if recipe_name in self._recipes:
            return self._recipes[recipe_name]
        raise ValueError(f'no recipe with name "{recipe_name}"')

    def get_material_recipe(self, material: Union[str, Material]):
        if Material.name_from(material) in self._basic_materials:
            return self._get_basic_recipe(material)

        recipe_ids = self._material_recipe_mapping[Material.name_from(material)]
        return self.get_recipe_by_id(recipe_ids[0])

    def get_recipe_by_id(self, id_):
        for recipe in self._recipes.values():
            if recipe.get_id() == id_:
                return recipe
        raise ValueError(f'no recipe with id "{id_}"')

    def is_recipe_exists(self, material: Union[str, Material]):
        return Material.name_from(material) in self._material_recipe_mapping

    def is_material_known(self, material: Union[str, Material]):
        return Material.name_from(material) in self._basic_materials or \
               self.is_recipe_exists(material)

    def to_json(self) -> dict:
        return {
            "basic": list(self._basic_materials),
            "composite": [recipe.to_json() for recipe in self._recipes.values()]
        }

    @classmethod
    def from_json(cls, json_object: dict):
        collection = RecipesCollection()
        for basic in json_object["basic"]:
            collection.add_unique_basic_material(basic)

        for recipe_json in json_object["composite"]:
            collection.add_unique_recipe(Recipe.from_json(recipe_json))

        return collection

    def update_recipe(self, new_recipe: Recipe):
        """if recipe with equal name exists, updates it at the same position and updates new material mappings"""

        self._remove_recipe_mappings(self._recipes[new_recipe.name])
        self._recipes[new_recipe.name] = new_recipe
        self._create_recipe_mappings(new_recipe)

    def remove_recipe(self, recipe: Recipe):
        self._remove_recipe_mappings(recipe)
        del self._recipes[recipe.name]

    def remove_recipe_by_name(self, name):
        self.remove_recipe(self.get_recipe_by_id(Recipe(name=name).get_id()))

    def remove_material_recipe_mapping(self, material: Material, recipe: Recipe):
        self._material_recipe_mapping[material.name].remove(recipe.get_id())

    def _remove_recipe_mappings(self, recipe):
        for material in recipe.get_results():
            self.remove_material_recipe_mapping(material, recipe)

    def _create_recipe_mappings(self, recipe):
        for result in recipe.get_results():
            self.add_material_recipe(result, recipe)

    @staticmethod
    def _get_basic_recipe(material):
        return Recipe(name=material, results=MaterialCollection([material]))

    def get_unresolved_names(self):
        names = set()
        for recipe in self._recipes.values():
            for ingredient in recipe.ingredients:
                if not self.is_material_known(ingredient):
                    names.add(ingredient.name)
        return names
