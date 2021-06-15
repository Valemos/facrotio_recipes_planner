from dataclasses import dataclass, field
from enum import Enum
from .material_collection import MaterialCollection
from .material import Material
from typing import List


class CraftStationType(Enum):
    ASSEMBLING = 0
    FURNACE = 1
    CHEMICAL_PLANT = 2
    OIL_REFINERY = 3


@dataclass
class Recipe:
    time: float  # second per craft
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    result: MaterialCollection = field(default_factory=MaterialCollection)
    producer_type: CraftStationType = CraftStationType.ASSEMBLING
    global_id: int = None  # must remain constant 

    def get_time_material(self):
        return Material('time', self.time)

    def add_ingredient(self, material):
        self.ingredients.add(material)

    def add_result(self, material):
        self.result.add(material)

    def get_result_amount(self, material: Material) -> float:
        if material not in self.result:
            raise ValueError(f'no such result "{material.id}" for recipe {self.result}')
        
        return self.result.items[material.id].amount

    def get_required(self) -> MaterialCollection:
        return self.ingredients

    def get_results(self) -> MaterialCollection:
        return self.result
