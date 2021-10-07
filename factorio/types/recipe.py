from dataclasses import dataclass, field
from enum import Enum
from .material_collection import MaterialCollection
from .material import Material


class CraftStationType(Enum):
    ASSEMBLING = 0
    FURNACE = 1
    CHEMICAL_PLANT = 2
    OIL_REFINERY = 3


@dataclass
class Recipe:
    time: float  # second per craft
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    results: MaterialCollection = field(default_factory=MaterialCollection)
    producer_type: CraftStationType = CraftStationType.ASSEMBLING
    name: str = ""

    def __eq__(self, other):
        return other.name == self.name and \
               other.time == self.time and \
               other.ingridients == self.ingredients and \
               other.results == self.results and \
               other.producer_type == self.producer_type

    def __hash__(self):
        return hash(self.name)

    @property
    def id(self):
        return hash(self)

    def get_time_material(self):
        return Material('time', self.time)

    def add_ingredient(self, material):
        self.ingredients.add(material)

    def add_result(self, material):
        self.results.add(material)

    def get_result_amount(self, material: Material) -> float:
        if material not in self.results:
            raise ValueError(f'no such result "{material.name}" for recipe {self.results}')
        
        return self.results.items[material.name].amount

    def get_required(self) -> MaterialCollection:
        return self.ingredients

    def get_results(self) -> MaterialCollection:
        return self.results
