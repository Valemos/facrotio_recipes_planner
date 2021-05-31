from dataclasses import dataclass, field
from factorio.material import Material
from typing import Dict


@dataclass(repr=False)
class MaterialCollection:
    '''represents a collection of materials and operations with them'''

    items: Dict[str, Material] = field(default_factory=dict)

    def __add__(self, other):
        assert isinstance(other, self.__class__)

        for _id, material in other.items:
            self.items[_id] += material

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)

        new_collection = MaterialCollection()

        for item in self.items.values():
            new_collection.add(item * multiplier)

        return new_collection

    def __iter__(self):
        return iter(self.items.values())

    def __len__(self):
        return len(self.items)

    def __contains__(self, material: Material):
        if isinstance(material, Material):
            return material.id in self.items
        else:
            return False

    def __repr__(self) -> str:
        if len(self.items) > 0:
            return 'Materials ' + ("; ".join(f"{key}: {val.amount}" for key, val in self.items.items()))
        else:
            return 'Empty'

    def add(self, material: Material):
        if material.id in self.items:
            self.items[material.id] += material
        else:
            self.items[material.id] = material
