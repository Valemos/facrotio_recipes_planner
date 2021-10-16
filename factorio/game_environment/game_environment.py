from itertools import chain
from pathlib import Path
from typing import Union

from factorio.game_environment.object_stats.a_stats import AStats
from factorio.game_environment.object_stats.assembling_machine_stats import AssemblingMachineStats
from factorio.game_environment.object_stats.crafting_category import CraftingCategory
from factorio.game_environment.object_stats.fluid_stats import FluidStats
from factorio.game_environment.object_stats.inserter_stats import InserterStats
from factorio.game_environment.object_stats.item_stats import ItemStats
from factorio.game_environment.object_stats.material_type import MaterialType
from factorio.game_environment.object_stats.mining_drill_stats import MiningDrillStats
from factorio.game_environment.object_stats.recipe_stats import RecipeStats
from factorio.game_environment.object_stats.transport_belt_stats import TransportBeltStats
from factorio.game_environment.stats_reading import read_stats_dict
from factorio.types.material import Material
from factorio.types.recipes_collection import RecipesCollection


class GameEnvironment:

    def __init__(self, load_folder: Path):
        self.recipe_stats = read_stats_dict(load_folder / "recipe.json", RecipeStats)
        self.assembling_stats = read_stats_dict(load_folder / "assembling-machine.json", AssemblingMachineStats)
        self.furnace_stats = read_stats_dict(load_folder / "furnace.json", AssemblingMachineStats)
        self.fluid_stats = read_stats_dict(load_folder / "fluid.json", FluidStats)
        self.item_stats = read_stats_dict(load_folder / "item.json", ItemStats)
        self.inserter_stats = read_stats_dict(load_folder / "inserter.json", InserterStats)
        self.transport_belt_stats = read_stats_dict(load_folder / "transport-belt.json", TransportBeltStats)
        self.mining_stats = read_stats_dict(load_folder / "mining-drill.json", MiningDrillStats)

        self._category_map: dict[CraftingCategory, list[str]] = {}
        self._init_categories()
        self._stats_map: dict[str, AStats] = {}

        for stats in [self.assembling_stats,
                      self.furnace_stats,
                      self.mining_stats,
                      self.fluid_stats,
                      self.item_stats,
                      self.inserter_stats,
                      self.transport_belt_stats]:
            self._stats_map = dict(self._stats_map, **stats)

        self.recipe_collection: RecipesCollection = self.create_recipes_collection()

    def get_stats(self, item_name: str):
        if not isinstance(item_name, str):
            raise ValueError("provide name string")
        return self._stats_map[item_name]

    def category_to_assemblers(self, category: CraftingCategory):
        return [self.get_stats(name).to_object() for name in self._category_map[category]]

    def get_material_type(self, material: Union[str, Material]):
        name = Material.name_from(material)
        if name in self.item_stats:
            return MaterialType.ITEM
        if name in self.fluid_stats:
            return MaterialType.FLUID
        raise ValueError("material not found")

    def _init_categories(self):
        assembler: AssemblingMachineStats
        assemblers = chain(self.assembling_stats.values(), self.furnace_stats.values(), self.mining_stats.values())
        for assembler in assemblers:
            for _category in assembler.crafting_categories.keys():
                if _category not in self._category_map:
                    self._category_map[_category] = []
                self._category_map[_category].append(assembler.name)

    def create_recipes_collection(self):
        recipes_collection = RecipesCollection()
        for _stats in self.recipe_stats:
            _recipe = _stats.to_object()
            if _recipe is not None:
                recipes_collection.add_unique_recipe(_recipe)

        for _unresolved_material in recipes_collection.get_unresolved_names():
            recipes_collection.add_unique_basic_material(_unresolved_material)

        return recipes_collection


if __name__ == '__main__':
    game_environment = GameEnvironment(Path('/home/anton/.factorio/script-output/recipe-lister/'))

    import pyperclip

    pyperclip.copy(','.join(i.inserter_rotation_speed for i in game_environment.inserter_stats.values()))
