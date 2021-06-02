from dataclasses import dataclass, field
from .production_config import ProductionConfig
from typing import List


@dataclass(repr=False)
class CraftingStep:
    config: ProductionConfig

    # reference to steps of type CraftingStep
    next_steps: List[object] = field(default_factory=list)
    previous_steps: List[object] = field(default_factory=list)


    def __repr__(self, level=0) -> str:
        result = "\t"*level + repr(self.get_result()) + "\n"
        for child in self.previous_steps:
            result += child.__repr__(level+1)
        return result

    def get_id(self):
        return self.config.machine.get_id()

    def get_result(self):
        return self.config.craft()

    def get_required_materials(self):
        return self.config.get_required_materials()

    def fixed_nodes_count(self):
        if len(self.previous_steps) == 0:
            # for final step check if fixed
            return 1 if self.fixed else 0

        total = 0
        for child in self.previous_steps:
            total += child.fixed_nodes_count(total)

        return total
