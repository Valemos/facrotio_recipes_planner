from copy import deepcopy
from typing import Union

from factorio.crafting_tree_builder.choice_collection import UserChoiceCollection
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.source_production_config import VirtualSourceNode
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.crafting_tree_builder.placeable_types.infinite_material_transport import InfiniteMaterialBus
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.object_stats.crafting_category import CraftingCategory


class VirtualProductionConfigBuilder:

    def __init__(self, game_environment: GameEnvironment, choices: UserChoiceCollection) -> None:
        self.game_env = game_environment
        self.choices = choices

    def get_assembler(self, category: CraftingCategory):
        assemblers = self.game_env.category_to_assemblers(category)
        return self.choices.choose_from(assemblers)

    def build_material_node(self, material: Union[str, Material]):
        recipes = self.game_env.recipe_collection.get_material_recipes(material)
        return self.build_recipe_node(self.choices.choose_from(recipes))

    def build_recipe_node(self, recipe: Recipe) -> VirtualAssemblerGroup:
        return VirtualAssemblerGroup(self.get_assembler(recipe.category), recipe)

    def build_source_node(self, material):
        material_type = self.game_env.get_material_type(material)
        return VirtualSourceNode(material, InfiniteMaterialBus(material_type))
