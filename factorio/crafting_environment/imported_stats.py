from itertools import chain
from pathlib import Path
from typing import Union

from factorio.crafting_environment.object_stats.assembling_machine_stats import AssemblingMachineStats
from factorio.crafting_environment.object_stats.crafting_category import CraftingCategory
from factorio.crafting_environment.object_stats.fluid_stats import FluidStats
from factorio.crafting_environment.object_stats.inserter_stats import InserterStats
from factorio.crafting_environment.object_stats.item_stats import ItemStats
from factorio.crafting_environment.object_stats.material_type import MaterialType
from factorio.crafting_environment.object_stats.mining_drill_stats import MiningDrillStats
from factorio.crafting_environment.object_stats.recipe_stats import RecipeStats
from factorio.crafting_environment.object_stats.transport_belt_stats import TransportBeltStats
from factorio.crafting_environment.stats_reading import read_stats_dict
from factorio.types.material import Material
from factorio.types.recipes_collection import RecipesCollection

folder = Path('/home/anton/.factorio/script-output/recipe-lister/')
recipe_stats = read_stats_dict(folder / "recipe.json", RecipeStats)
assembling_stats = read_stats_dict(folder / "assembling-machine.json", AssemblingMachineStats)
furnace_stats = read_stats_dict(folder / "furnace.json", AssemblingMachineStats)
fluid_stats = read_stats_dict(folder / "fluid.json", FluidStats)
item_stats = read_stats_dict(folder / "item.json", ItemStats)
inserter_stats = read_stats_dict(folder / "inserter.json", InserterStats)
transport_belt_stats = read_stats_dict(folder / "transport-belt.json", TransportBeltStats)
mining_stats = read_stats_dict(folder / "mining-drill.json", MiningDrillStats)

import pyperclip
pyperclip.copy(','.join(i.inserter_rotation_speed for i in inserter_stats.values()))

_stats_dicts = [
    assembling_stats,
    furnace_stats,
    mining_stats,
    fluid_stats,
    item_stats,
    inserter_stats,
    transport_belt_stats,
]

_name_to_stats: dict = {}
for d in _stats_dicts:
    _name_to_stats = dict(_name_to_stats, **d)


def get_stats(item_name: str):
    if not isinstance(item_name, str):
        raise ValueError("provide name string")
    return _name_to_stats[item_name]


recipes_collection = RecipesCollection()
for _stats in recipe_stats:
    _recipe = _stats.to_object()
    if _recipe is not None:
        recipes_collection.add_unique_recipe(_recipe)

for _unresolved_material in recipes_collection.get_unresolved_names():
    recipes_collection.add_unique_basic_material(_unresolved_material)


_category_to_assembler_map = {}
_assembler: AssemblingMachineStats
for _assembler in chain(assembling_stats.values(), furnace_stats.values(), mining_stats.values()):
    for _category in _assembler.crafting_categories.keys():
        if _category not in _category_to_assembler_map:
            _category_to_assembler_map[_category] = []
        _category_to_assembler_map[_category].append(_assembler.name)


def category_to_assemblers(category: CraftingCategory):
    craft_stations = [get_stats(a.name).to_object() for a in _category_to_assembler_map[category]]
    return craft_stations


def get_material_type(material: Union[str, Material]):
    name = Material.name_from(material)
    if name in item_stats:
        return MaterialType.ITEM
    if name in fluid_stats:
        return MaterialType.FLUID
    raise ValueError("material not found")
