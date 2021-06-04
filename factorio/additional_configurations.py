from factorio.types.recipe import Recipe
from .types.production_config import ProductionConfig
from .types.item_bus import ItemBus
from .types.production_unit import assembling_machine_inf
from .types.inserter_unit import InserterUnit, inserter_fast
from .types.transport_belt import TransportBelt, transport_belt_inf


# this config must only be used for source belts
def compressed_belt_config(belt_type: TransportBelt):
    return ProductionConfig(
        assembling_machine_inf,
        ItemBus([InserterUnit("", cycle_speed=belt_type.item_rate)], belt_type),
        ItemBus([InserterUnit("", cycle_speed=belt_type.item_rate)], belt_type)
    )


config_infinite_input_output = compressed_belt_config(transport_belt_inf).copy_with_recipe(Recipe(0))
