from typing import Union
from enum import Enum
from factorio.types.material import Material
from factorio.recipe_util.vanilla_collections import fluid_types, basic_ore_types, oil_recipe_types, material_ids


class MaterialType(Enum):
    BASIC_FLUID = 0
    OIL_DERIVED = 1
    ORE = 2
    ITEM = 3


def get_material_numeric_id(material: Union[str, Material]):
    return material_ids[Material.name_from(material)]


def get_material_type(material: Union[str, Material]):
    if Material.name_from(material) in oil_recipe_types:
        return MaterialType.OIL_DERIVED
    elif Material.name_from(material) in fluid_types:
        return MaterialType.BASIC_FLUID
    elif Material.name_from(material) in basic_ore_types:
        return MaterialType.ORE
    return MaterialType.ITEM
