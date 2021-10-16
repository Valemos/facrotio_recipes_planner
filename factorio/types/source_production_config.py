from factorio.entity_network.assembling_machine import AssemblingMachine
from factorio.entity_network.material_transport import FixedMaterialTransport
from factorio.types.material import Material
from factorio.types.material_collection import MaterialCollection
from factorio.types.production_config import ProductionConfig
from factorio.types.recipe import Recipe


class SourceProductionConfig(ProductionConfig):

    def __init__(self, material: Material, item_bus: FixedMaterialTransport, is_constrained=False):
        self.material = material
        super().__init__(AssemblingMachine(1, recipe), item_bus, item_bus, item_bus.max_rate, is_constrained)

    def get_id(self):
        return self.material

    def get_results_rates(self):
        collection = MaterialCollection()
        collection.add(Material(self.material.name, self.output.get_max_rate()))
        return collection

    def get_production_rate(self):
        return self.producers_amount

    def set_recipe(self, recipe: Recipe):
        """Must only be valid recipe on input. NOT empty recipe or else cannot assign valid material for this source"""
        self.material = recipe.results.first()
        self.producer = self.producer.setup(recipe)

    def set_material_rate(self, material_rate: Material):
        assert self.material.name == material_rate.name
        self.producers_amount = material_rate.amount

    def set_basic_material_rate(self, material_rate: Material):
        self.set_material_rate(material_rate)

    def set_max_consumers(self, input_material_rates: MaterialCollection):
        print("WARN! trying to deduce producers amount for source material")
