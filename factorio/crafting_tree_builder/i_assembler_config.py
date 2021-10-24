from abc import abstractmethod

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe


class IAssemblerConfig:

    @property
    @abstractmethod
    def recipe(self) -> Recipe:
        pass

    @property
    @abstractmethod
    def constrained(self) -> bool:
        pass

    @constrained.setter
    @abstractmethod
    def constrained(self, value: bool):
        pass

    @abstractmethod
    def set_result_rate(self, material: Material):
        pass
