import unittest
from copy import deepcopy

from factorio.types.material import Material
from factorio.types.material_collection import MaterialCollection
from factorio.types.recipe import Recipe, CraftStationType
from factorio.types.recipes_collection import RecipesCollection
from serialization.a_json_savable import AJsonSerializable


class TestSerializationDeserialization(unittest.TestCase):

    def setUp(self) -> None:
        self.material = Material("mat", 100)
        self.collection_empty = MaterialCollection()
        self.collection = MaterialCollection([self.material, Material("next", 2)])
        self.recipe = Recipe("name", 3, CraftStationType.CHEMICAL_PLANT, self.collection_empty, self.collection)
        self.recipes_collection = RecipesCollection()
        self.recipes_collection.add_unique_recipe(self.recipe)

    def test_material(self):
        self.test_obj(self.material)

    def test_material_collection(self):
        self.test_obj(self.collection_empty)
        self.test_obj(self.collection)

    def test_recipe(self):
        self.test_obj(self.recipe)

    def test_recipe_collection(self):
        self.test_obj(self.recipes_collection)

    def test_obj(self, obj: AJsonSerializable):
        j = obj.to_json()
        obj2 = obj.__class__.from_json(j)
        self.assertEqual(obj, obj2)
