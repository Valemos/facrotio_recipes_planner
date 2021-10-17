from copy import deepcopy

from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.source_production_config import SourceProductionConfig
from factorio.crafting_tree_builder.placeable_types.infinite_material_transport import InfiniteMaterialTransport
from factorio.crafting_tree_builder.placeable_types.material_transport import AItemTransport, AFluidTransport
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.object_stats.crafting_category import CraftingCategory
from factorio.game_environment.object_stats.material_type import MaterialType
from factorio.crafting_tree_builder.internal_types.production_config import ProductionConfig


class ProductionConfigBuilder:

    def __init__(self, game_environment: GameEnvironment) -> None:
        self._game_env = game_environment
        self._choices = {}

    def __deepcopy__(self, memodict={}):
        c = object.__new__(ProductionConfigBuilder)
        c._game_env = self._game_env
        c._choices = deepcopy(self._choices)
        return c

    def build(self, recipe: Recipe) -> ProductionConfig:
        material_type = self._game_env.get_material_type(recipe.get_results().first())
        return ProductionConfig(self.get_assembler(recipe.category),
                                self.get_material_transport(material_type),
                                self.get_material_transport(material_type))

    def get_assembler(self, category: CraftingCategory):
        # todo add assembler selection
        return self._game_env.category_to_assemblers(category)

    @staticmethod
    def get_material_transport(material_type: MaterialType):
        # unrestricted material bus for now
        return InfiniteMaterialTransport(material_type)

    def build_source(self, material):
        material_type = self._game_env.get_material_type(material)
        return SourceProductionConfig(material, self.get_material_transport(material_type))

