from abc import abstractmethod, ABCMeta

from factorio.crafting_tree_builder.internal_types.recipe import Recipe


class IAssemblerConfig(metaclass=ABCMeta):

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
