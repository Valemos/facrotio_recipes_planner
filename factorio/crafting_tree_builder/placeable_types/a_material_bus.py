from abc import abstractmethod, ABC

from factorio.game_environment.object_stats.material_type import MaterialType


class AMaterialBus(list, ABC):
    """collection of objects that deliver materials to assemblers"""

    def try_add(self, obj) -> None:
        if obj.material_type != self.material_type:
            return
        obj._material_bus = self
        super().append(obj)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(id(o1) == id(o2) for o1, o2 in zip(iter(self), iter(other)))
        else:
            return False

    @property
    @abstractmethod
    def material_type(self) -> MaterialType:
        pass

    @staticmethod
    def merge(first, second):
        if not isinstance(second, AMaterialBus):
            raise ValueError(f'incorrect bus object type {repr(second)}')

        if first.__class__ != second.__class__:
            raise ValueError("bus types does not match")

        if len(first) < len(second):
            first, second = second, first

        for obj in second:
            first.try_add(obj)
