from dataclasses import dataclass, field
from typing import List
from factorio.types.transport_belt_unit import TransportBeltUnit
from factorio.types.inserter_unit import InserterUnit


@dataclass
class MaterialBus:
    """represents conveyor belt <-> inserter or inserter alone"""
    inserters: List[InserterUnit] = field(default_factory=list)
    transport_belt: TransportBeltUnit = None

    def get_max_rate(self, amount_units: int = 1):
        """
        amount_units represents how much machines 
        are connected to the same transport belt with the same inserter setup
        """
        belt_rate = self.transport_belt.item_rate if self.transport_belt is not None else float('inf') 
        inserters_rate = amount_units * sum(inserter.get_item_rate() for inserter in self.inserters)
        return min(belt_rate, inserters_rate)


@dataclass
class FixedMaterialBus(MaterialBus):
    max_rate: float = 0

    def get_max_rate(self, amount_units: int = 1):
        return self.max_rate
