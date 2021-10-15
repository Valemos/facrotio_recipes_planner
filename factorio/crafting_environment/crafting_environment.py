import math
from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Set
from typing import Union

from factorio.types.material import Material
from factorio.types.material_type import MaterialType
from factorio.types.inserter_unit import InserterUnit
from factorio.crafting_environment.objects.transporters.item_bus import MaterialBus
from factorio.types.production_config import ProductionConfig
from factorio.crafting_environment.objects.craft_stations.craft_station import CraftStation
from factorio.types.recipe import Recipe
from factorio.crafting_environment.objects.craft_stations.craft_station_type import CraftStationType
from factorio.types.recipes_collection import RecipesCollection
from factorio.types.transport_belt_unit import TransportBeltUnit


# todo add env builder



@dataclass(init=False)
class CraftingEnvironment:
    final_recipe_ids: Set[int]
    assembler_type: CraftStation
    inserter_type: InserterUnit
    transport_belt_type: TransportBeltUnit

    def __init__(self,
                 final_materials: List[Union[str, Material]] = None,
                 assembler_type=assembling_machine_1,
                 furnace_type=furnace_1,
                 inserter_type=inserter,
                 transport_belt_type=transport_belt_1,
                 recipes_collection: RecipesCollection = None) -> None:

        if recipes_collection is not None:
            self.recipes_collection = recipes_collection
        else:
            from configurations.vanilla_collections import recipes_vanilla
            self.recipes_collection = recipes_vanilla

        self.final_recipe_ids = set()
        if final_materials is not None:
            for material in final_materials:
                self.add_final_recipe_name(Material.name_from(material))

        self.assembler_type: CraftStation = assembler_type
        self.furnace_type: CraftStation = furnace_type
        self.inserter_type: InserterUnit = inserter_type
        self.transport_belt_type: TransportBeltUnit = transport_belt_type
        self.constraints: Dict[str, ProductionConfig] = {}

    def add_final_recipe_name(self, recipe_name: str):
        recipe = self.recipes_collection.get_recipe(recipe_name)
        self.final_recipe_ids.add(recipe.get_id())

    def remove_final_recipe(self, recipe_name: str):
        self.final_recipe_ids.remove(self.recipes_collection.get_recipe_id(recipe_name))

    def add_constrain_config(self, config: ProductionConfig):
        """constrain amount of recipe crafts that can be produced by system"""
        config.constrained = True
        self.constraints[config.get_recipe().get_id()] = config

    def constrain_material_rate(self, material: Material):
        assert issubclass(material.__class__, Material)
        recipe = self.recipes_collection[material.name]
        config = self.get_recipe_config_unconstrained(recipe)
        config.set_material_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.recipes_collection.get_material_recipe(recipe_name)
        config = self.get_recipe_config_unconstrained(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self.constraints = {}

    def get_production_config(self, recipe: Recipe) -> ProductionConfig:
        """
        if material production is constrained, user producer config will apply
        
        WARNING! if the same config is requested multiple times, the same object will be returned
        """

        if recipe.get_id() in self.constraints:
            return deepcopy(self.constraints[recipe.get_id()])

        if self.is_final_recipe(recipe):
            # todo add source config object according to item type
            pass

        return self.get_recipe_config_unconstrained(recipe)

    def is_final_recipe(self, recipe: Recipe):
        if recipe.get_id() in self.final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.get_required()) == 0

    def get_recipe_config_unconstrained(self, recipe: Recipe):
        # todo create mapping of crafting stations to recipe categories
        if recipe.category == CraftStationType.ASSEMBLING:
            return self._get_production_config_unconstrained(recipe)

        if recipe.category == CraftStationType.CHEMICAL_PLANT:
            return self._get_chemical_config_unconstrained(recipe)

        if recipe.category == CraftStationType.FURNACE:
            return self._get_smelting_config_unconstrained(recipe)

        raise ValueError(f"unknown crafting type for recipe {recipe.get_results().get_combined_name()}")

    def _get_default_item_bus(self, inserters_amount: int = 1):
        return MaterialBus([self.inserter_type] * inserters_amount, self.transport_belt_type)

    def _get_production_config_unconstrained(self, recipe: Recipe):
        # inserters can pick 2 items from two lanes on conveyor
        input_inserters_number = math.ceil(0.5 * len(recipe.get_required()))
        return ProductionConfig(
            self.assembler_type.setup(recipe),
            self._get_default_item_bus(input_inserters_number),
            self._get_default_item_bus())

    def _get_smelting_config_unconstrained(self, recipe: Recipe):
        return ProductionConfig(
            self.furnace_type.setup(recipe),
            self._get_default_item_bus(),
            self._get_default_item_bus())

    def _get_chemical_config_unconstrained(self, recipe):
        return ProductionConfig(
            chemical_plant.setup(recipe),
            self._get_default_item_bus(),
            self._get_default_item_bus())

    def get_material_recipe(self, material: Material):
        return self.recipes_collection.get_material_recipe(material)


DEFAULT_ENVIRONMENT = CraftingEnvironment([])
FINAL_ENVIRONMENT = CraftingEnvironment([], assembling_machine_3, furnace_3, inserter_stack, transport_belt_3)
