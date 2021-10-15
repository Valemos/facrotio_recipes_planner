from .exporter_mod_deserializer import *
from ..types.recipe import Recipe
from ..types.recipes_collection import RecipesCollection

_stats_dicts = [
    assembling_machine_stats,
    furnace_stats,
    fluid_stats,
    item_stats,
    inserter_stats,
    transport_belt_stats,
    mining_stats,
]

_name_to_stats: dict = {}
for d in _stats_dicts:
    _name_to_stats = dict(_name_to_stats, **d)


def get_object_stats(item_name):
    return _name_to_stats[item_name]


recipes_collection = RecipesCollection()
for _stats in recipe_stats:
    _recipe = _stats.to_object()
    if _recipe is not None:
        recipes_collection.add_unique_recipe(_recipe)

for _unresolved_material in recipes_collection.get_unresolved_names():
    recipes_collection.add_unique_basic_material(_unresolved_material)
