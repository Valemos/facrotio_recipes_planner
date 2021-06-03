from dataclasses import dataclass, field
from factorio.types.transport_belt import TransportBelt, transport_belt_1
from .item_bus import ItemBus
import math
from typing import Dict, List, Set, Union
from copy import deepcopy
from .production_config import ProductionConfig
from .recipe import Recipe
from .material import Material
from .production_unit import ProductionUnit, assembling_machine_1
from .inserter_unit import InserterUnit, inserter
from ..misc import to_material
from ..recipe_collections import recipes_info


@dataclass(init=False)
class CraftingEnvironment:
    final_recipe_ids: Set[int]
    crafting_machine: ProductionUnit
    inserter_type: InserterUnit
    transport_belt_type: TransportBelt

    def __init__(self, 
                materials: List[Union[str, Material]], 
                crafting_machine=assembling_machine_1,
                inserter_type=inserter,
                transport_belt_type=transport_belt_1) -> None:

        self.final_recipe_ids = set()
        for material in materials:
            # WARN! can cause problems if one material corresponds to multiple recipes 
            self.final_recipe_ids.add(recipes_info[to_material(material).id].global_id)
        
        self.crafting_machine = crafting_machine
        self.inserter_type = inserter_type
        self.transport_belt_type = transport_belt_type
        self.constraints: Dict[str, ProductionConfig] = {}

    def add_constraint_config(self, config: ProductionConfig):
        """constrain amount of recipe crafts that can be produced by system"""
        config.fixed = True
        self.constraints[config.get_recipe().global_id] = config

    def add_constraint_amount_produced(self, material: Material):
        recipe = recipes_info[material.id]
        config = self._get_production_config_unconstrained(recipe)
        config.set_material_rate(material)
        self.add_constraint_config(config)

    def clear_constraints(self):
        self.constraints = {}

    def _get_production_config_unconstrained(self, recipe: Recipe):
        # inserters can pick 2 items from two lanes on conveyor
        input_inserters_number = math.ceil(0.5 * len(recipe.get_required()))  
        return ProductionConfig(
                self.crafting_machine.setup(recipe),
                ItemBus([self.inserter_type] * input_inserters_number, self.transport_belt_type),
                ItemBus([self.inserter_type], self.transport_belt_type))

    def get_production_config(self, recipe: Recipe) -> ProductionConfig:
        """
        if material production is constrained, user producer config will apply
        
        WARNING! if the same config is requested multiple times, the same object will be returned
        """
        if recipe.global_id in self.constraints:
            return deepcopy(self.constraints[recipe.global_id])

        return self._get_production_config_unconstrained(recipe)

    def is_final_recipe(self, recipe: Recipe):
        if recipe.global_id in self.final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.ingredients) == 0


DEFAULT_ENVIRONMENT = CraftingEnvironment([])
