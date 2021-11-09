from dataclasses import dataclass, field

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable

from factorio.deterministic_hash import hash_det


@dataclass
class Material(ACompositeJsonSerializable):
    name: str = field(default="", hash=True)
    amount: float = field(default=1, hash=True)  # inf value indicates is considered an unconstrained amount

    def __mul__(self, multiplier):
        assert isinstance(multiplier, float) or isinstance(multiplier, int)
        return Material(self.name, self.amount * multiplier)

    def __add__(self, other):
        assert issubclass(other.__class__, self.__class__)
        if other.name != self.name: raise ValueError("cannot add different items")
        return Material(self.name, self.amount + other.amount)

    def __eq__(self, other):
        return other.name == self.name and other.amount == self.amount

    def __hash__(self):
        return hash_det(self.name)

    @property
    def id(self):
        return hash(self)

    @staticmethod
    def from_obj(material, default_amount: float = 1):
        return Material(material, default_amount) if isinstance(material, str) else material

    @staticmethod
    def name_from(material) -> str:
        return material.name if isinstance(material, Material) else material
