from dataclasses import dataclass, field
from math import floor

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass(unsafe_hash=True)
class Position(ACompositeJsonSerializable):
    x: float = field(default=0, hash=True)
    y: float = field(default=0, hash=True)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.add(other.x, other.y)
        else:
            raise ValueError("incorrect point type")

    def __str__(self):
        return f'({self.x}, {self.y})'

    def add_x(self, amount):
        return self.add(x=amount)

    def add_y(self, amount):
        return self.add(y=amount)

    def add(self, x: float = 0, y: float = 0):
        return Position(self.x + x, self.y + y)

    def floor(self):
        return Position(floor(self.x), floor(self.y))
