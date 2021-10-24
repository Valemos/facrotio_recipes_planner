from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import ProductionNodeBuilder


def build_for_material(material: Material, game_env: GameEnvironment):
    recipe = game_env.recipe_collection.get_material_recipe(material)

    config_builder = ProductionNodeBuilder(game_env)
