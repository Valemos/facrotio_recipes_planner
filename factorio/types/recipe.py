from dataclasses import dataclass, field
from enum import Enum

from .a_json_savable import AJsonSavable
from .material_collection import MaterialCollection
from .material import Material


class CraftStationType(Enum):
    ASSEMBLING = 0
    FURNACE = 1
    CHEMICAL_PLANT = 2
    OIL_REFINERY = 3


@dataclass
class Recipe(AJsonSavable):

    name: str = ""
    time: float = 0  # in seconds per craft
    producer_type: CraftStationType = CraftStationType.ASSEMBLING
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    results: MaterialCollection = field(default_factory=MaterialCollection)

    def __eq__(self, other):
        return other.name == self.name and \
               other.time == self.time and \
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

    def to_json(self):
        return {
            "id": self.name,
            "craft_type": self.producer_type.name,
            "time": self.time,
            "ingredients": self.ingredients.to_json(),
            "products": self.results.to_json(),
        }

    @staticmethod
    def from_json(json_object):
        return Recipe(name=json_object["id"],
                      time=json_object["time"],
                      producer_type=CraftStationType[json_object["craft_type"]],
                      ingredients=MaterialCollection.from_json(json_object["ingredients"]),
                      results=MaterialCollection.from_json(json_object["products"]))
