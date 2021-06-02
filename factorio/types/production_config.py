from dataclasses import dataclass, field
from .material import Material
from typing import List
from .inserter_unit import InserterUnit
from .production_unit import ProductionUnit


@dataclass
class ProductionConfig:
    """represents production unit combined with input and output inserters"""

    machine: ProductionUnit
    input: List[InserterUnit] = field(default_factory=list)
    output: List[InserterUnit] = field(default_factory=list)

    # not fixed config will be updated later during execution
    machine_amount: float = 1
    fixed: bool = False


    @staticmethod
    def _get_inserters_speed(inserters: List[InserterUnit]):
        return [inserter.get_output_speed() for inserter in inserters]

    def get_input_speed(self):
        return self._get_inserters_speed(self.input)

    def get_output_speed(self):
        return self._get_inserters_speed(self.output)

    def get_required_materials(self):
        return self.machine.get_required_materials(self.machine_amount)

    def craft(self):
        return self.machine.craft(self.machine_amount)
