from copy import deepcopy, copy
from typing import Union

from factorio.crafting_environment import CraftingEnvironment
from factorio.crafting_tree_builder.coordinate_grid import CoordinateGrid
from factorio.game_environment.parsing.blueprint import Blueprint
from factorio.game_environment.parsing.blueprint_object import BlueprintObject
from factorio.recipe_graph.crafting_step import CraftingStep
from factorio.types.material import Material


class CraftingTreeBuilder:

    def __init__(self, crafting_env: CraftingEnvironment) -> None:
        self._final_material = None
        self._crafting_env = deepcopy(crafting_env)
        self._grid = CoordinateGrid()

    @classmethod
    def from_blueprint(cls, blueprint: Blueprint, environment: CraftingEnvironment):
        builder = cls(environment)
        for obj in blueprint.objects:
            builder.add_blueprint_object(obj)

    def add_blueprint_object(self, obj: BlueprintObject):
        # todo add specialization of blueprint objects
        self._grid.place_object(obj, obj.position)

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
