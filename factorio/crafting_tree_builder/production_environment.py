from typing import Iterator

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.game_environment.game_environment import GameEnvironment
from factorio.recipe_graph.production_node import ProductionNode


class ProductionEnvironment:
    def __init__(self, game_env: GameEnvironment):
        self.game_env = game_env

    def get_material_buses(self, material: Material) -> Iterator[AMaterialBus]:
        # todo for given material yield all buses, that can supply it for a given node
        pass

    def build_graph(self) -> ProductionNode:
        pass
