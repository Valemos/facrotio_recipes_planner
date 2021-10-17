from dataclasses import dataclass

from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class Position(ACompositeJsonSerializable):
    x: float = 0
    y: float = 0

    def add_x(self, amount):
        return Position(self.x + amount, self.y)

    def add_y(self, amount):
        return Position(self.x, self.y + amount)
