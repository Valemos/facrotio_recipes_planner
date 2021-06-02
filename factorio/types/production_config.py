from dataclasses import dataclass, field
from factorio.types.item_bus import ItemBus
from .material import Material
from typing import List
from .inserter_unit import InserterUnit
from .production_unit import ProductionUnit
import math


@dataclass
class ProductionConfig:
    """represents production unit combined with input and output inserters"""

    producer: ProductionUnit
    input: ItemBus
    output: ItemBus

    # not fixed config will be updated later during execution
    producers_amount: float = float('inf')
    fixed: bool = False

    def get_requirements(self):
        return self.producer.get_required_materials(self.producers_amount)

    def set_material_production(self, material_rate: Material):
        time_per_craft = self.producer.get_craft_time()
        time_input = self.get_requirements().total_items() / self.input.get_max_rate()
        time_output = self.get_craft_result().total_items() / self.output.get_max_rate()

        # these time intervals does not depend on each other
        production_cycle_time = max(time_per_craft, time_input, time_output)

        # to produce at least material_rate.amount items per second 
        # increase number of producing units to sufficient amount
        self.producers_amount = math.ceil(material_rate.amount * production_cycle_time)

    def get_craft_result(self):
        return self.producer.get_result_scaled(self.producers_amount)

    def get_productivity(self):
        return self.producer.get_productivity_scaled(self.producers_amount)

    def get_recipe(self):
        return self.producer.recipe
