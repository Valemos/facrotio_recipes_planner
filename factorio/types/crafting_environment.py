from dataclasses import dataclass, field
from .material import Material
from .material_collection import MaterialCollection
from .production_unit import ProductionUnit, assembling_machine_1
from ..misc import to_material
from typing import List, Union


@dataclass(init=False)
class CraftingEnvironment:
    materials: MaterialCollection
    crafting_machine: ProductionUnit

    def __init__(self, materials: List[Union[str, Material]], crafting_machine=assembling_machine_1) -> None:
        self.materials = MaterialCollection()
        for elem in materials:
            self.materials.add(to_material(elem))
        
        self.crafting_machine = crafting_machine
