from copy import deepcopy
from typing import Union

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.source_production_config import SourceConfig
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.crafting_tree_builder.placeable_types.infinite_material_transport import InfiniteMaterialBus
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.object_stats.crafting_category import CraftingCategory


class VirtualProductionConfigBuilder:

    def __init__(self, game_environment: GameEnvironment) -> None:
        self._game_env = game_environment
        self._choices = {}

    def __deepcopy__(self, memodict={}):
        copy = object.__new__(VirtualProductionConfigBuilder)
        copy._game_env = self._game_env
        copy._choices = deepcopy(self._choices)
        return copy

    def build_material(self, material: Union[str, Material]):
        # todo add recipe selection
        recipe = self._game_env.recipe_collection.get_material_recipes(material)[0]
        return self.build_recipe(recipe)

    def build_recipe(self, recipe: Recipe) -> VirtualAssemblerGroup:
        return VirtualAssemblerGroup(self.get_assembler(recipe.category), recipe)

    def get_assembler(self, category: CraftingCategory):
        # todo add assembler selection
        return self._game_env.category_to_assemblers(category)[0]

    def build_source(self, material):
        material_type = self._game_env.get_material_type(material)
        return SourceConfig(material, InfiniteMaterialBus(material_type))
