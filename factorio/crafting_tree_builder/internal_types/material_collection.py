from copy import deepcopy
from typing import Dict, Union

from serialization.a_container_json_serializable import AContainerJsonSerializable
from .material import Material


class MaterialCollection(AContainerJsonSerializable):
    """represents a collection of materials and operations with them"""

    __element_type__ = Material

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

    def __eq__(self, other):
        return set(self.items.keys()) == set(other.items.keys())

    def __repr__(self) -> str:
        if len(self.items) > 0:
            return 'Materials ' + ("; ".join(f"{key}: {val.amount}" for key, val in self.items.items()))
        else:
            return 'Empty'

    def __add__(self, other):
        assert isinstance(other, self.__class__)

        new_collection = deepcopy(self)

        for material in other:
            new_collection.add(material)

        return new_collection

    # custom Material operations

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)

        if multiplier == 1:
            return self

        new_collection = MaterialCollection()
        for item in self:
            new_collection.add(item * multiplier)

        return new_collection

    def __truediv__(self, divider):
        assert isinstance(divider, float) or isinstance(divider, int)
        return self * (1 / divider)

    @staticmethod
    def _keytransform(key: Union[str, Material]):
        if issubclass(key.__class__, Material):
            return key.name
        if isinstance(key, str):
            return key
        raise ValueError("invalid key type")

    def first(self):
        """returns first element from material dictionary as defined by .values()"""
        if len(self.items) == 0:
            raise ValueError("trying to access first material in empty collection")
        return next(iter(self.items.values()))

    def add(self, material: Material):
        if material.name in self.items:
            self.items[material.name] += material
        else:
            self.items[material.name] = material

    def total(self):
        return sum(m.amount for m in self)

    def append(self, element: Material):
        if not isinstance(element, Material):
            raise ValueError("not a material")

        self.items[element.name] = element

    def common_with(self, other):
        if not isinstance(other, MaterialCollection):
            raise ValueError(f"not a material collection {repr(other)}")

        new = MaterialCollection()
        for material in self:
            if material in other:
                new.add(material)

        for material in other:
            if material in self:
                new.add(material)

        return new
