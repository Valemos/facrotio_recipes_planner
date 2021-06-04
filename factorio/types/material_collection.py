from dataclasses import dataclass, field
from typing import Dict, Union
from collections.abc import MutableMapping
from copy import deepcopy
from .material import Material


@dataclass(repr=False)
class MaterialCollection(MutableMapping):
    '''represents a collection of materials and operations with them'''

    items: Dict[str, Material] = field(default_factory=dict)

    def __getitem__(self, key):
        return self.items[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.items[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.items[self._keytransform(key)]

    def __iter__(self):
        return iter(self.items.values())
    
    def __len__(self):
        return len(self.items)

    def _keytransform(self, key: Union[str, Material]):
        if issubclass(key.__class__, Material):
            return key.id
        elif isinstance(key, str):
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
        '''returns first element from material dictionary as defined by .values()'''
        if len(self.items) == 0:
            return Material("Empty", 0)
        return next(iter(self.items.values()))

    def get_combined_name(self):
        return ';'.join(self.items.keys())

    def add(self, material: Material):
        if material.id in self.items:
            self.items[material.id] += material
        else:
            self.items[material.id] = material

    def total(self):
        return sum(m.amount for m in self)
