from dataclasses import dataclass

from factorio.types.material import Material


@dataclass(eq=True, unsafe_hash=True)
class InserterUnit(Material):
    cycle_speed: float = 1
    capacity: float = 1

    def __str__(self):
        return f"Cycle: {self.cycle_speed} Size: {self.capacity}"

    def get_item_rate(self):
        return self.cycle_speed * self.capacity
