import unittest

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import VirtualProductionConfigBuilder


class TestCraftingAdvisorGraph(unittest.TestCase):

    def setUp(self) -> None:
        self.game_env = GameEnvironment.load_default()
        self.node_builder = VirtualProductionConfigBuilder(self.game_env)

    def test_set_material_consumption(self):
        material = Material("iron-gear-wheel", 1)
        node = self.node_builder.build_material(material)

        self.assertEqual(node.get_output_rates(), MaterialCollection([material]))

        component_rates = node.recipe.ingredient_rates * 2

        node.set_max_consumers(component_rates)
        self.assertEqual(node.get_output_rates(), MaterialCollection([material * 2]))

        component_rates = node.recipe.ingredient_rates * 2.5

        node.set_max_consumers(component_rates)
        self.assertEqual(node.get_output_rates(), MaterialCollection([material * 2]))

        component_rates = node.recipe.ingredient_rates * 3

        node.set_max_consumers(component_rates)
        self.assertEqual(node.get_output_rates(), MaterialCollection([material * 3]))
