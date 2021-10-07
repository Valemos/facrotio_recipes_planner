from typing import Union
from factorio.types.material import Material
from configurations.vanilla_collections import fluid_types, basic_ore_types, oil_recipe_types
from factorio.types.material_type import MaterialType


def get_material_type(material: Union[str, Material]):
    if Material.name_from(material) in oil_recipe_types:
        return MaterialType.OIL_DERIVED
    elif Material.name_from(material) in fluid_types:
        return MaterialType.BASIC_FLUID
    elif Material.name_from(material) in basic_ore_types:
        return MaterialType.ORE
    return MaterialType.ITEM
