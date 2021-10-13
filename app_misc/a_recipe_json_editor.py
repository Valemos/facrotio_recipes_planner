import json
from abc import ABCMeta, abstractmethod
from pathlib import Path

from factorio.types.recipes_collection import RecipesCollection


class ARecipeJsonEditor(metaclass=ABCMeta):

    @property
    @abstractmethod
    def recipe_file_path(self) -> Path:
        pass

    def save_recipes_to_json(self, recipes: RecipesCollection):
        with self.recipe_file_path.open("w") as fout:
            json.dump(recipes.to_json(), fout)

    def read_recipes_from_json(self):
        with self.recipe_file_path.open("r") as fin:
            try:
                recipes = RecipesCollection.from_json(json.load(fin))
            except ValueError as err:
                print(err)
                recipes = RecipesCollection()

        return recipes
