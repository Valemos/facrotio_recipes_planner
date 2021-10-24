from copy import deepcopy, copy
from pathlib import Path
from typing import Dict, List
from typing import Union

from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import ProductionNodeBuilder
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.crafting_tree_builder.internal_types.recipe import Recipe


class CraftingEnvironment:

    def __init__(self,
                 final_materials: List[Union[str, Material]] = None,
                 builder: ProductionNodeBuilder = None,
                 game_env: GameEnvironment = None, ) -> None:

        self.final_material = None
        self.game_env = game_env if game_env is not None else GameEnvironment.load_default()
        self._constrains: Dict[str, VirtualAssemblerGroup] = {}

        self.production_config_builder = builder

        self._final_recipe_ids = set()
        if final_materials is not None:
            for material in final_materials:
                self.add_final_recipe_name(Material.name_from(material))

    def __deepcopy__(self, memodict={}):
        c = object.__new__(CraftingEnvironment)
        c.game_env = self.game_env
        c._constrains = deepcopy(self._constrains)
        c.production_config_builder = deepcopy(self.production_config_builder)
        return c

    def copy(self):
        shallow = copy(self)
        shallow.game_env = copy(self.production_config_builder)
        return shallow

    def add_final_recipe_name(self, recipe_name: str):
        recipe = self.game_env.recipe_collection.get_recipe(recipe_name)
        self._final_recipe_ids.add(recipe.get_id())

    def remove_final_recipe(self, recipe_name: str):
        recipe_id = self.game_env.recipe_collection.get_recipe(recipe_name).get_id()
        self._final_recipe_ids.remove(recipe_id)

    def add_constrain_config(self, config: VirtualAssemblerGroup):
        """constrain amount of recipe crafts that can be produced by system"""
        config.constrained = True
        self._constrains[config.recipe.get_id()] = config

    def constrain_material_rate(self, material: Union[str, Material]):
        config = self.get_material_config(material)
        config.set_material_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.game_env.recipe_collection.get_recipe(recipe_name)
        config = self.get_config_unconstrained(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self._constrains = {}

    def get_production_config(self, recipe: Recipe) -> VirtualAssemblerGroup:
        """
        if material production is constrained, user producer config will apply
        
        WARNING! if the same config is requested multiple times, the same object will be returned
        """
        # todo move functionality of creating assembling configs to step providers if needed
        if recipe.get_id() in self._constrains:
            return deepcopy(self._constrains[recipe.get_id()])

        if self.is_final_recipe(recipe):
            result_material = recipe.get_results().first()
            return self.production_config_builder.build_source(result_material)

        return self.get_config_unconstrained(recipe)

    def is_final_recipe(self, recipe: Recipe):
        if recipe.get_id() in self._final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.ingredients) == 0

    def get_config_unconstrained(self, recipe: Recipe):
        return self.production_config_builder.build_recipe(recipe)

    def get_material_recipe(self, material: Material):
        return self.game_env.recipe_collection.get_material_recipe(material)

    def get_material_config(self, material):
        recipe = self.get_material_recipe(material)
        return self.get_production_config(recipe)
