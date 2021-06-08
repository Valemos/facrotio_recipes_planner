from typing import Union
from enum import Enum
from .types.material import Material
from .recipe_collections import fluid_types, basic_ore_types, oil_derived_types


class MaterialType(Enum):
    BASIC_FLUID = 0
    OIL_DERIVED = 1
    ORE = 2
    ITEM = 3


def to_material(material: Union[str, Material], default_amount: float = 1) -> Material:
    return Material(material, default_amount) if isinstance(material, str) else material


def to_material_id(material: Union[str, Material]) -> str:
    return material.id if isinstance(material, Material) else material


def get_material_type(material: Union[str, Material]):
    if to_material_id(material) in oil_derived_types:
        return MaterialType.OIL_DERIVED
    elif to_material_id(material) in fluid_types:
        return MaterialType.BASIC_FLUID
    elif to_material_id(material) in basic_ore_types:
        return MaterialType.ORE
    return MaterialType.ITEM
