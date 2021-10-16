from factorio.crafting_tree_builder.objects.material_transport import ItemTransport, FluidTransport
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.object_stats.crafting_category import CraftingCategory
from factorio.game_environment.object_stats.material_type import MaterialType
from factorio.types.production_config import ProductionConfig
from factorio.types.recipe import Recipe
from factorio.types.source_production_config import SourceProductionConfig


class ProductionConfigBuilder:

    def __init__(self, game_environment: GameEnvironment) -> None:
        self._game_env = game_environment

    def build(self, recipe: Recipe) -> ProductionConfig:
        material_type = self._game_env.get_material_type(recipe.get_results().first())
        return ProductionConfig(self.get_assembler(recipe.category),
                                self.get_material_transport(material_type),
                                self.get_material_transport(material_type))

    def get_assembler(self, category: CraftingCategory):
        # todo add assembler selection
        return self._game_env.category_to_assemblers(category)

    def get_material_transport(self, material_type: MaterialType):
        # todo add transport creation from game environment and selection
        if MaterialType.ITEM == material_type:
            return ItemTransport()
        if MaterialType.FLUID == material_type:
            return FluidTransport()

    def build_source(self, material):
        material_type = self._game_env.get_material_type(material)
        return SourceProductionConfig(material, self.get_material_transport(material_type))

