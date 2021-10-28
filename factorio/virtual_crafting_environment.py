from copy import deepcopy, copy
from typing import Dict, List
from typing import Union

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.virtual_assembler_group import VirtualAssemblerGroup
from factorio.game_environment.game_environment import GameEnvironment
from factorio.production_config_builder import VirtualProductionConfigBuilder


class VirtualCraftingEnvironment:

    def __init__(self,
                 ready_materials: List[Union[str, Material]] = None,
                 builder: VirtualProductionConfigBuilder = None, ) -> None:

        if builder is None:
            self.node_config_builder = VirtualProductionConfigBuilder(GameEnvironment.load_default())
        else:
            self.node_config_builder = builder

        self.game_env = self.node_config_builder.game_env
        self._constrains: Dict[str, VirtualAssemblerGroup] = {}

        self._ready_materials = MaterialCollection()
        for m in ready_materials:
            self._ready_materials.add(Material.from_obj(m, default_amount=float("inf")))

    def __copy__(self):
        shallow = copy(self)
        shallow.game_env = self.game_env
        shallow.node_config_builder = deepcopy(self.node_config_builder)
        shallow._constrains = deepcopy(self._constrains)
        shallow._final_recipe_ids = deepcopy(self._ready_materials)
        return shallow

    def add_constrain_config(self, config: VirtualAssemblerGroup):
        """constrain amount of recipe crafts that can be produced by system"""
        config.constrained = True
        self._constrains[config.recipe.get_id()] = config

    def constrain_material_rate(self, material: Union[str, Material]):
        config = self.build_material_node(material)
        config.set_result_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.game_env.recipe_collection.get_recipe(recipe_name)
        config = self.node_config_builder.build_recipe_node(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self._constrains = {}

    def build_material_node(self, material: Material) -> VirtualAssemblerGroup:
        """
        if material production is constrained, user producer config will apply
        """

        if material in self._ready_materials:
            return self.node_config_builder.build_source_node(self._ready_materials[material])

        config = self.node_config_builder.build_material_node(material)
        if config.recipe.get_id() in self._constrains:
            return deepcopy(self._constrains[config.recipe.get_id()])

        return config
