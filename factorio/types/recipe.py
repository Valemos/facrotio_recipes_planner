from dataclasses import dataclass, field
from factorio.misc import to_material
from .material_collection import MaterialCollection
from .material import Material
from typing import List


@dataclass
class Recipe:
    time: float  # second per craft
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    result: MaterialCollection = field(default_factory=MaterialCollection)
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

    def get_required_materials(self, amount = 1) -> MaterialCollection:
        return self.ingredients * amount if amount != 1 else self.ingredients

    def craft(self, amount = 1) -> MaterialCollection:
        return self.result * amount if amount != 1 else self.result
