from dataclasses import dataclass, field

from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from .material import Material
from .material_collection import MaterialCollection
from ..crafting_environment.object_stats.crafting_category import CraftingCategory


@dataclass
class Recipe(ACompositeJsonSerializable):

    name: str = ""
    time: float = 0  # in seconds per craft
    category: CraftingCategory = CraftingCategory.NO_CATEGORY
    ingredients: MaterialCollection = field(default_factory=MaterialCollection)
    results: MaterialCollection = field(default_factory=MaterialCollection)

    def __eq__(self, other):
        return other.name == self.name and \
               other.time == self.time and \
               other.category == self.category

    def __hash__(self):
        return hash(self.name)

    def get_id(self):
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
