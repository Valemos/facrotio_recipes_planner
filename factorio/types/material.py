from dataclasses import dataclass, field
from typing import Union
from .a_json_savable import AJsonSavable


@dataclass(frozen=True)
class Material(AJsonSavable):
    """a bunch of items of the same type"""

    name: str = field(hash=True)
    amount: float = field(default=1, hash=False)  # inf value indicates is considered an unconstrained amount

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)
        return Material(self.name, self.amount * multiplier)

    def __add__(self, other):
        assert issubclass(other.__class__, self.__class__)
        if other.id != self.name: raise ValueError("cannot add items of different types")
        return Material(self.name, self.amount + other.amount)

    def __eq__(self, other):
        return other.name == self.name and other.amount == self.amount

    def __hash__(self):
        return hash(self.name)

    @property
    def id(self):
        return hash(self)

    @staticmethod
    def from_obj(material, default_amount: float = 1):
        return Material(material, default_amount) if isinstance(material, str) else material

    @staticmethod
    def name_from(material) -> str:
        return material.name if isinstance(material, Material) else material

    def to_json(self):
        return {"id": self.name, "amount": self.amount}

    @staticmethod
    def from_json(json_object):
        return Material(json_object["id"], json_object["amount"])
