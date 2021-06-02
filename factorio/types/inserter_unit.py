from dataclasses import dataclass, field
from factorio.types.material_collection import MaterialCollection
from .material import Material


@dataclass(frozen=True, eq=True)
class InserterUnit(Material):
    cycle_speed: float = 0
    capacity: float = 1
    

    def get_item_rate(self):
        return self.cycle_speed * self.capacity


inserter = InserterUnit("inserter", cycle_speed=0.83, capacity=1)
inserter_long = InserterUnit("long-handed-inserter", cycle_speed=1.20, capacity=1)
inserter_fast = InserterUnit("fast-inserter", cycle_speed=2.31, capacity=1)
inserter_filter = InserterUnit("filter-inserter", cycle_speed=2.31, capacity=1)
inserter_stack = InserterUnit("stack-inserter", cycle_speed=2.31, capacity=2)
inserter_stack_filter = InserterUnit("stack-filter-inserter", cycle_speed=2.31, capacity=2)
