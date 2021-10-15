from factorio.types.recipe import Recipe
from factorio.types.production_config import SourceProductionConfig
from factorio.crafting_environment.objects.transporters.item_bus import FixedMaterialBus
from factorio.types.transport_belt_unit import TransportBeltUnit
from configurations.vanilla_devices import transport_belt_inf


# this config must only be used for source belts
def compressed_belt_config(recipe: Recipe, belt_type: TransportBeltUnit, is_constrained=False):
    return SourceProductionConfig(recipe, FixedMaterialBus(max_rate=belt_type.item_rate), is_constrained)


config_infinite_input_output = compressed_belt_config(Recipe(0), transport_belt_inf, False)
