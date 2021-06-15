from factorio.types.recipe import Recipe
from .types.production_config import ProductionConfig, SourceProductionConfig
from .types.item_bus import FixedItemBus, ItemBus
from .types.production_unit import ProductionUnit, assembling_machine_inf
from .types.inserter_unit import InserterUnit, inserter_fast
from .types.transport_belt import TransportBelt, transport_belt_inf
from .recipe_collections import EMPTY_RECIPE


# this config must only be used for source belts
def compressed_belt_config(recipe: Recipe, belt_type: TransportBelt, is_constrained=False):
    return SourceProductionConfig(recipe, FixedItemBus(max_rate=belt_type.item_rate), is_constrained)


config_infinite_input_output = compressed_belt_config(EMPTY_RECIPE, transport_belt_inf, False)
