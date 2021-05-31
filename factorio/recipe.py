from dataclasses import dataclass, field
from factorio.material_collection import MaterialCollection
from factorio.material import Material
from typing import List


@dataclass
class Recipe:
    time: float
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    result: MaterialCollection = field(default_factory=MaterialCollection)

    def get_time_material(self):
        return Material('time', self.time)

    def add_ingredient(self, material):
        self.ingredients.add(material)

    def add_result(self, material):
        self.result.add(material)

    def get_result_amount(self, material: Material) -> float:
        if material not in self.result:
            return 0
        
        return self.result.items[material.id].amount

    def get_requirements(self, amount) -> MaterialCollection:
        return self.ingredients * amount

    def craft(self, amount) -> MaterialCollection:
        return self.result * amount

    def craft_with_time(self, amount: float = 1, speed: float = 1) -> MaterialCollection:    
        results = self.result * amount
        results.add(self.get_time_material() * speed)
        return results

