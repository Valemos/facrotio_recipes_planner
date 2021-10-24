from abc import abstractmethod

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe


class IAssemblerConfig:

    @abstractmethod
    @property
    def recipe(self) -> Recipe:
        pass

    @abstractmethod
    @property
    def constrained(self) -> bool:
        pass

    @abstractmethod
    @constrained.setter
    def constrained(self, value: bool):
        pass

    @abstractmethod
    def get_required_rates(self) -> MaterialCollection:
        pass

    @abstractmethod
    def set_material_rate(self, material: Material):
        pass
