from dataclasses import dataclass, field
from typing import Union


@dataclass(frozen=True, eq=True)
class Material:
    '''a bunch of items of the same type'''

    name: str = field(hash=True)
    amount: float = field(default=1, hash=False)  # inf value indicates is considered an unconstrained amount

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)
        return Material(self.name, self.amount * multiplier)

    def __add__(self, other):
        assert issubclass(other.__class__, self.__class__)
        if other.id != self.name: raise ValueError("cannot add items of different types")
        return Material(self.name, self.amount + other.amount)

    @staticmethod
    def from_dict(ingredient: dict):
        if 'id' not in ingredient or 'amount' not in ingredient:
            raise ValueError("invalid material dictionary")

        return Material(ingredient['id'], ingredient['amount'])

    @staticmethod
    def from_obj(material, default_amount: float = 1):
        return Material(material, default_amount) if isinstance(material, str) else material

    @staticmethod
    def name_from(material):
        return material.name if isinstance(material, Material) else material
