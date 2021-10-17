from abc import abstractmethod
from dataclasses import dataclass

from factorio.blueprint_analysis.a_sized_grid_object import ASizedGridObject
from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.game_environment.object_stats.material_type import MaterialType


@dataclass
class AMaterialTransport(ASizedGridObject):
    _material_bus: AMaterialBus = None

    @property
    def material_bus(self) -> AMaterialBus:
        if self._material_bus is None:
            self._material_bus = self.create_new_bus()
            self._material_bus.try_add(self)
        return self._material_bus

    @material_bus.setter
    def material_bus(self, bus):
        if not isinstance(bus, AMaterialBus):
            raise ValueError(f'not a material bus {repr(bus)}')
        self._material_bus = bus

    @property
    @abstractmethod
    def max_rate(self):
        pass

    @property
    @abstractmethod
    def material_type(self) -> MaterialType:
        pass

    @abstractmethod
    def create_new_bus(self) -> AMaterialBus:
        pass

    def try_connect(self, other):
        """assumes other object is also AMaterialTransport"""
        if self.material_type == other.material_type:
            AMaterialBus.merge(self.material_bus, other.material_bus)
            return True
        return False
