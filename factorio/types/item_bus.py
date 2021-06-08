from dataclasses import dataclass, field
from typing import List
from .transport_belt import TransportBelt
from .inserter_unit import InserterUnit
from .material_collection import MaterialCollection
from ..misc import MaterialType, get_material_type


@dataclass
class ItemBus:
    """represents conveyor belt <-> inserter or inserter alone"""
    inserters: List[InserterUnit] = field(default_factory=list)
    transport_belt: TransportBelt = None 

    def get_max_rate(self, amount_units: int = 1):
        """
        amount_units represents how much machines 
        are connected to the same transport belt with the same inserter setup
        """
        belt_rate = self.transport_belt.item_rate if self.transport_belt is not None else float('inf') 
        inserters_rate = amount_units * sum(inserter.get_item_rate() for inserter in self.inserters)
        return min(belt_rate, inserters_rate)

    def get_transport_rate(self, materials_rate: MaterialCollection):
        # inserters sorted by their output rate rising for best distribution

        materials_total = 0
        for material_rate in materials_rate:
            material_type = get_material_type(material_rate)
            if material_type != MaterialType.FLUID:
                materials_total += material_rate.amount

        inserter_rate_total = self.get_max_rate()
        if materials_total > inserter_rate_total:
            return inserter_rate_total
        else:
            return materials_total
