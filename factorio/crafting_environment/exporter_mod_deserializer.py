import json
from pathlib import Path

from factorio.crafting_environment.stats.assembling_machine_stats import AssemblingMachineStats
from factorio.crafting_environment.stats.fluid_stats import FluidStats
from factorio.crafting_environment.stats.inserter_stats import InserterStats
from factorio.crafting_environment.stats.item_stats import ItemStats
from factorio.crafting_environment.stats.mining_drill_stats import MiningDrillStats
from factorio.crafting_environment.stats.recipe_stats import RecipeStats
from factorio.crafting_environment.transport_belt_stats import TransportBeltStats


def read(file_path: Path) -> dict:
    with file_path.open("r") as fin:
        return json.load(fin)


def read_stats_iter(jsons_iter, stats_class):
    for stats_json in jsons_iter:
        yield stats_class.from_json(stats_json)


def read_stats(jsons_iter, stats_class):
    return list(read_stats_iter(jsons_iter, stats_class))


def read_stats_dict(jsons_iter, stats_class):
    result = {}
    for stats in read_stats_iter(jsons_iter, stats_class):
        result[stats.name] = stats
    return result


folder = Path('/home/anton/.factorio/script-output/recipe-lister/')
recipe_stats = read_stats_dict(read(folder / "recipe.json").values(), RecipeStats)
assembling_machine_stats = read_stats_dict(read(folder / "assembling-machine.json").values(), AssemblingMachineStats)
furnace_stats = read_stats_dict(read(folder / "furnace.json").values(), AssemblingMachineStats)
fluid_stats = read_stats_dict(read(folder / "fluid.json").values(), FluidStats)
item_stats = read_stats_dict(read(folder / "item.json").values(), ItemStats)
inserter_stats = read_stats_dict(read(folder / "inserter.json").values(), InserterStats)
transport_belt_stats = read_stats_dict(read(folder / "transport-belt.json").values(), TransportBeltStats)
mining_stats = read_stats_dict(read(folder / "mining-drill.json").values(), MiningDrillStats)

