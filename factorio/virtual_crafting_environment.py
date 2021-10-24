from copy import deepcopy, copy
from typing import Dict, List
from typing import Union

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import VirtualProductionConfigBuilder


class VirtualCraftingEnvironment:

    def __init__(self,
                 final_materials: List[Union[str, Material]] = None,
                 builder: VirtualProductionConfigBuilder = None,
                 game_env: GameEnvironment = None, ) -> None:

        self.final_material = None
        self.game_env = game_env if game_env is not None else GameEnvironment.load_default()
        self._constrains: Dict[str, VirtualAssemblerGroup] = {}

        self.node_config_builder = builder

        self._final_recipe_ids = set()
        if final_materials is not None:
            for material in final_materials:
                recipes = self.game_env.recipe_collection.get_material_recipes(material)
                for recipe in recipes:
                    self.add_final_recipe(recipe)

    def __copy__(self):
        shallow = copy(self)
        shallow.game_env = self.game_env
        shallow.node_config_builder = deepcopy(self.node_config_builder)
        shallow._constrains = deepcopy(self._constrains)
        shallow._final_recipe_ids = deepcopy(self._final_recipe_ids)
        return shallow

    def add_final_recipe(self, recipe: Recipe):
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
        config.set_result_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.game_env.recipe_collection.get_recipe(recipe_name)
        config = self.node_config_builder.build_recipe(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self._constrains = {}

    def get_material_config(self, material: Material) -> VirtualAssemblerGroup:
        """
        if material production is constrained, user producer config will apply
        """

        config = self.node_config_builder.build_material(material)

        if config.recipe.get_id() in self._constrains:
            return deepcopy(self._constrains[config.recipe.get_id()])

        if self.is_final_recipe(config.recipe):
            return self.node_config_builder.build_source(material)

        return config

    def is_final_recipe(self, recipe: Recipe):
        if recipe.get_id() in self._final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.ingredients) == 0
