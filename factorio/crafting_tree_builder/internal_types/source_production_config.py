from factorio.crafting_tree_builder.placeable_types.assembling_machine import AssemblingMachineUnit
from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialTransport
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.production_config import ProductionConfig
from factorio.crafting_tree_builder.internal_types.recipe import Recipe


class SourceProductionConfig(ProductionConfig):

    def __init__(self, material: Material, item_bus: AMaterialTransport, is_constrained=False):
        self.material = material
        super().__init__(None, item_bus, item_bus, item_bus.max_rate(), is_constrained)

    def get_id(self):
        return self.material

    def get_results_rates(self):
        collection = MaterialCollection()
        collection.add(Material(self.material.name, self.output.max_rate()))
        return collection

    def get_production_rate(self):
        return self.producers_amount

    def set_material_rate(self, material_rate: Material):
        assert self.material.name == material_rate.name
        self.producers_amount = material_rate.amount

    def set_basic_material_rate(self, material_rate: Material):
        self.set_material_rate(material_rate)

    def set_max_consumers(self, input_material_rates: MaterialCollection):
        print("WARN! trying to deduce producers amount for source material")
