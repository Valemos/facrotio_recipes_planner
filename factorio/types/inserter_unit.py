from dataclasses import dataclass
from .material import Material


@dataclass(frozen=True, eq=True)
class InserterUnit(Material):
    cycle_speed: float = 0
    capacity: float = 1

    def __str__(self):
        return f"Cycle: {self.cycle_speed} Size: {self.capacity}"

    def get_item_rate(self):
        return self.cycle_speed * self.capacity
