from factorio.types.material import Material
from typing import Union


def to_material(obj: Union[str, Material], default_amount: float = 1) -> Material:
    return Material(obj, default_amount) if isinstance(obj, str) else obj
