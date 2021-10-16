from copy import deepcopy
from copy import deepcopy
from typing import Dict, List, Set
from typing import Union

from factorio.crafting_environment.object_stats.material_type import MaterialType
from factorio.entity_network.material_transport import FixedMaterialTransport
from factorio.types.material import Material
from factorio.types.production_config import ProductionConfig
from factorio.types.recipe import Recipe
from factorio.types.recipes_collection import RecipesCollection
from factorio.types.source_production_config import SourceProductionConfig
import imported_stats


class CraftingEnvironment:
    # todo add environment builder
    # todo add builder
    _final_recipe_ids: Set[int]

    def __init__(self,
                 final_materials: List[Union[str, Material]] = None,
                 recipes_collection: RecipesCollection = None) -> None:

        if recipes_collection is not None:
            self.recipes_collection = recipes_collection
        else:
            self.recipes_collection = imported_stats.recipes_collection

        self._final_recipe_ids = set()
        if final_materials is not None:
            for material in final_materials:
                self.add_final_recipe_name(Material.name_from(material))

        # todo add current technology level selection
        self.constrains: Dict[str, ProductionConfig] = {}

    def add_final_recipe_name(self, recipe_name: str):
        recipe = self.recipes_collection.get_recipe(recipe_name)
        self._final_recipe_ids.add(recipe.get_id())

    def remove_final_recipe(self, recipe_name: str):
        self._final_recipe_ids.remove(self.recipes_collection.get_recipe_id(recipe_name))

    def add_constrain_config(self, config: ProductionConfig):
        """constrain amount of recipe crafts that can be produced by system"""
        config.constrained = True
        self.constrains[config.get_recipe().get_id()] = config

    def constrain_material_rate(self, material: Material):
        assert issubclass(material.__class__, Material)
        recipe = self.recipes_collection[material.name]
        config = self.get_config_unconstrained(recipe)
        config.set_material_rate(material)
        self.add_constrain_config(config)

    def constrain_producers_amount(self, recipe_name: str, amount: float):
        recipe = self.recipes_collection.get_material_recipe(recipe_name)
        config = self.get_config_unconstrained(recipe)
        config.producers_amount = amount
        self.add_constrain_config(config)

    def clear_constraints(self):
        self.constrains = {}

    def get_production_config(self, recipe: Recipe) -> ProductionConfig:
        """
        if material production is constrained, user producer config will apply
        
        WARNING! if the same config is requested multiple times, the same object will be returned
        """

        if recipe.get_id() in self.constrains:
            return deepcopy(self.constrains[recipe.get_id()])

        if self.is_final_recipe(recipe):
            result_material = recipe.get_results().first()
            material_type = imported_stats.get_material_type(result_material)
            if MaterialType.ITEM == material_type:
                return SourceProductionConfig(result_material, FixedMaterialTransport(self.get_belt_type()))
            elif MaterialType.FLUID == material_type:
                return SourceProductionConfig(result_material, FixedMaterialTransport(float("inf")))

        return self.get_config_unconstrained(recipe)

    def is_final_recipe(self, recipe: Recipe):
        if recipe.get_id() in self._final_recipe_ids:
            return True

        # if not found in ready components, check if object is the simplest component    
        return len(recipe.get_required()) == 0

    def get_config_unconstrained(self, recipe: Recipe):
        # todo add selection of assembler
        assembler = self.get_assembler(recipe)
        print(f'selected category "{recipe.category.name}"')
        return ProductionConfig(assembler, self._get_inf_item_bus(), self._get_inf_item_bus())

    def get_assembler(self, recipe):
        return imported_stats.category_to_assemblers(recipe.category)[0]

    def get_material_recipe(self, material: Material):
        return self.recipes_collection.get_material_recipe(material)

    def get_belt_type(self):
        # todo add selection of belt
        return imported_stats.get_stats("transport-belt")

    @staticmethod
    def _get_inf_item_bus():
        # todo get item bus objects from blueprint object grid
        return FixedMaterialTransport(max_rate=float("inf"))


DEFAULT_ENVIRONMENT = CraftingEnvironment([])
