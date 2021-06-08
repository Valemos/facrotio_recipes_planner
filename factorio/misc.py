from typing import Union
from enum import Enum
from .types.material import Material
from .recipe_collections import fluid_types, ore_types


class MaterialType(Enum):
    FLUID = 0
    ORE = 1
    ITEM = 2


def to_material(material: Union[str, Material], default_amount: float = 1) -> Material:
    return Material(material, default_amount) if isinstance(material, str) else material


def to_material_id(material: Union[str, Material]) -> str:
    return material.id if isinstance(material, Material) else material


def get_material_type(material: Union[str, Material]):
    if to_material_id(material) in fluid_types:
        return MaterialType.FLUID
    elif to_material_id(material) in ore_types:
        return MaterialType.ORE
    return MaterialType.ITEM
