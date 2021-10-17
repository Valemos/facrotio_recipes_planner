from dataclasses import dataclass, field

from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass(unsafe_hash=True)
class Position(ACompositeJsonSerializable):
    x: float = field(default=0, hash=True)
    y: float = field(default=0, hash=True)

    def add_x(self, amount):
        return Position(self.x + amount, self.y)

    def add_y(self, amount):
        return Position(self.x, self.y + amount)

    def round(self):
        return Position(round(self.x), round(self.y))
