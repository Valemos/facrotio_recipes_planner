from dataclasses import dataclass, field
from .material import Material
from typing import List
from .inserter_unit import InserterUnit
from .production_unit import ProductionUnit
import math


@dataclass
class ProductionConfig:
    """represents production unit combined with input and output inserters"""

    machine: ProductionUnit
    input: List[InserterUnit] = field(default_factory=list)
    output: List[InserterUnit] = field(default_factory=list)

    # not fixed config will be updated later during execution
    machine_amount: float = float('inf')
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

    def set_material_production(self, material: Material):
        items_per_craft = self.machine.recipe.get_result_amount(material)
        self.machine_amount = math.ceil(material.amount / items_per_craft)

    def get_result(self):
        return self.machine.get_result_scaled(self.machine_amount)

    def get_recipe(self):
        return self.machine.recipe
