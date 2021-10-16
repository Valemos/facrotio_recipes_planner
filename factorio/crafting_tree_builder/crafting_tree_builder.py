from copy import deepcopy
from typing import Union

from factorio.crafting_environment import CraftingEnvironment
from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.recipe_graph.crafting_step import CraftingStep
from factorio.types.material import Material


class CraftingTreeBuilder:

    def __init__(self, crafting_env: CraftingEnvironment) -> None:
        self._final_material = None
        self._crafting_env = deepcopy(crafting_env)

    @classmethod
    def from_object_grid(cls, object_grid: ObjectCoordinateGrid):
        # todo finish this
        pass

    def set_final_material_rate(self, material: Union[str, Material]):
        self._final_material = Material.from_obj(material)

    def constrain_material_rate(self, material: Material):
        self._crafting_env.constrain_material_rate(material)

    def build_tree(self) -> CraftingStep:
        material_recipe = self._crafting_env.get_material_recipe(self.get_final_material())
        tree = CraftingStep(self._crafting_env.get_production_config(material_recipe))
        tree.create_ingredient_steps(self._crafting_env)

        step: CraftingStep
        for step in tree.iterate_bottom_to_up():
            if step.is_constrained():
                step.propagate_output_constraints()

        tree.deduce_infinite_materials()

        return tree

    def get_final_material(self):
        if self._final_material is None:
            raise ValueError("provide final material for tree")
