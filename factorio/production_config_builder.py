from copy import deepcopy
from typing import Union

from choice_form_app import ChoiceFormApp
from factorio.crafting_tree_builder.choice_collection import UserChoiceCollection
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.virtual_source_node import VirtualSourceNode
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.object_stats.crafting_category import CraftingCategory


class VirtualProductionConfigBuilder:

    def __init__(self, game_environment: GameEnvironment = None, choices: UserChoiceCollection = None) -> None:
        self.game_env = game_environment if game_environment is not None else GameEnvironment.load_default()
        self.choices = choices if choices is not None else UserChoiceCollection(ChoiceFormApp)

    def get_assembler(self, category: CraftingCategory):
        assemblers = self.game_env.category_to_assemblers(category)
        return self.choices.choose_from(assemblers)

    def build_material_node(self, material: Union[str, Material]):
        recipes = self.game_env.recipe_collection.get_material_recipes(material)
        recipe_node = self.build_recipe_node(self.choices.choose_from(recipes))
        recipe_node.set_output_rates(MaterialCollection([material]))
        return recipe_node

    def build_recipe_node(self, recipe: Recipe) -> VirtualAssemblerGroup:
        return VirtualAssemblerGroup(self.get_assembler(recipe.category), recipe)

    @staticmethod
    def build_source_node(material):
        return VirtualSourceNode(material)
