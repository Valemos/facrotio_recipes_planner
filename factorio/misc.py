from factorio.types.material import Material
from typing import Union


def to_material(obj: Union[str, Material]) -> Material:
    return Material(obj) if isinstance(obj, str) else obj
