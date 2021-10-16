from copy import deepcopy
from functools import cached_property
from pathlib import Path
from typing import Dict, List, Set
from typing import Union

from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import ProductionConfigBuilder
from factorio.types.material import Material
from factorio.types.production_config import ProductionConfig
from factorio.types.recipe import Recipe


class CraftingEnvironment:
    _final_recipe_ids: Set[int]

    def __init__(self,
                 final_materials: List[Union[str, Material]] = None,
                 game_env: GameEnvironment = None) -> None:

        self.game_env = game_env if game_env is not None else self.game_env_default
        self.constrains: Dict[str, ProductionConfig] = {}
        self.production_config_builder = ProductionConfigBuilder(self.game_env)

        self._final_recipe_ids = set()
        if final_materials is not None:
            for material in final_materials:
                self.add_final_recipe_name(Material.name_from(material))

    @cached_property
    def game_env_default(self):
        return GameEnvironment(Path('/home/anton/.factorio/script-output/recipe-lister/'))

    def add_final_recipe_name(self, recipe_name: str):
        recipe = self.game_env.recipe_collection.get_recipe(recipe_name)
        self._final_recipe_ids.add(recipe.get_id())

    def remove_final_recipe(self, recipe_name: str):
        recipe_id = self.game_env.recipe_collection.get_recipe(recipe_name).get_id()
        self._final_recipe_ids.remove(recipe_id)

    def add_constrain_config(self, config: ProductionConfig):
        """constrain amount of recipe crafts that can be produced by system"""
        config.constrained = True
        self.constrains[config.get_recipe().get_id()] = config

    def constrain_material_rate(self, material: Union[str, Material]):
        recipe = self.game_env.recipe_collection[material]
        config = self.get_config_unconstrained(recipe)
        config.set_material_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.game_env.recipe_collection.get_material_recipe(recipe_name)
        config = self.get_config_unconstrained(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self.constrains = {}

    def get_production_config(self, recipe: Recipe) -> ProductionConfig:
        """
        if material production is constrained, user producer config will apply
        
        WARNING! if the same config is requested multiple times, the same object will be returned
        """

        if recipe.get_id() in self.constrains:
            return deepcopy(self.constrains[recipe.get_id()])

        if self.is_final_recipe(recipe):
            result_material = recipe.get_results().first()
            return self.production_config_builder.build_source(result_material)

        return self.get_config_unconstrained(recipe)

    def is_final_recipe(self, recipe: Recipe):
        if recipe.get_id() in self._final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.get_required()) == 0

    def get_config_unconstrained(self, recipe: Recipe):
        return self.production_config_builder.build(recipe)
