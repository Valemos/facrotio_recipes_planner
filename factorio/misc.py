from typing import Union
from enum import Enum
from .types.material import Material
from .recipe_collections import fluid_types


class MaterialType(Enum):
    FLUID = 0
    ITEM = 1


def to_material(material: Union[str, Material], default_amount: float = 1) -> Material:
    return Material(material, default_amount) if isinstance(material, str) else material


def get_material_type(material: Union[str, Material]):
    if to_material(material).id in fluid_types:
        return MaterialType.FLUID
    return MaterialType.ITEM
