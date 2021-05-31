from dataclasses import dataclass, field
from .production_unit import ProductionUnit
from typing import List


@dataclass(repr=False)
class CraftingStep:
    producer: ProductionUnit
    amount_producers: float = 1  # amount of producers on this step

    # reference to steps of type CraftingStep
    next_step: object = None
    previous_steps: List[object] = field(default_factory=list)


    def __repr__(self, level=0) -> str:
        result = "\t"*level+repr(self.producer.recipe.result)+"\n"
        for child in self.previous_steps:
            result += child.__repr__(level+1)
        return result

    def get_id(self):
        return self.producer.get_id()

    def get_result(self):
        return self.producer.craft(self.amount_producers)

    def get_requirements(self):
        return self.producer.get_requirements(self.amount_producers)
