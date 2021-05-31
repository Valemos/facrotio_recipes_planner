from dataclasses import dataclass, field
from factorio.production_unit import ProductionUnit
from typing import List


@dataclass(repr=False)
class CraftingStep:
    # reference to next step of type CraftingStep
    producer: ProductionUnit
    amount: float
    next_step: object = None
    previous_steps: List[object] = field(default_factory=list)


    def __repr__(self, level=0) -> str:
        result = "\t"*level+repr(self.producer.recipe.result)+"\n"
        for child in self.previous_steps:
            result += child.__repr__(level+1)
        return result

    def get_result(self):
        return self.producer.craft()
