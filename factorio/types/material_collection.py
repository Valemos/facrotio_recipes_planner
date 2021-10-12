from typing import Dict, Union
from collections.abc import MutableMapping
from copy import deepcopy

from .a_json_savable import AJsonSavable
from .material import Material


class MaterialCollection(MutableMapping, AJsonSavable):
    """represents a collection of materials and operations with them"""

    def __init__(self, initial_elements: list = None) -> None:
        initial_elements = initial_elements if initial_elements is not None else []

        if not isinstance(initial_elements, list):
            raise ValueError("input materials not a list")
        
        self.items: Dict[str, Material] = {}

        for elem in initial_elements:
            self.add(elem)

    def __getitem__(self, key) -> Material:
        return self.items[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.items[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.items[self._keytransform(key)]

    def __iter__(self):
        return iter(self.items.values())
    
    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return self._keytransform(item) in self.items

    @staticmethod
    def _keytransform(key: Union[str, Material]):
        if issubclass(key.__class__, Material):
            return key.name
        if isinstance(key, str):
            return key
        raise ValueError("invalid key type")

    def __repr__(self) -> str:
        if len(self.items) > 0:
            return 'Materials ' + ("; ".join(f"{key}: {val.amount}" for key, val in self.items.items()))
        else:
            return 'Empty'

    # custom Material operations

    def __add__(self, other):
        assert isinstance(other, self.__class__)

        new_collection = deepcopy(self)

        for material in other:
            new_collection.add(material)

        return new_collection

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)

        new_collection = MaterialCollection()

        for item in self:
            new_collection.add(item * multiplier) 

        return new_collection

    def first(self):
        """returns first element from material dictionary as defined by .values()"""
        if len(self.items) == 0:
            raise ValueError("trying to access first material in empty collection")
        return next(iter(self.items.values()))

    def get_combined_name(self):
        return ';'.join(self.items.keys())

    def add(self, material: Material):
        if material.name in self.items:
            self.items[material.name] += material
        else:
            self.items[material.name] = material

    def total(self):
        return sum(m.amount for m in self)

    def to_json(self):
        return [material.to_json() for material in self.items.values()]

    @staticmethod
    def from_json(json_object):
        if not isinstance(json_object, list):
            raise ValueError("incorrect json for material collection")
        return MaterialCollection([Material.from_json(json_material) for json_material in json_object])
