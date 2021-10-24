from abc import abstractmethod

from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.crafting_tree_builder.placeable_types.a_sized_grid_object import ASizedGridObject
from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode
from factorio.game_environment.object_stats.material_type import MaterialType


class AMaterialBusUnit(AMaterialConnectionNode, ASizedGridObject):

    def __init__(self):
        AMaterialConnectionNode.__init__(self)
        ASizedGridObject.__init__(self)
        self._material_bus: AMaterialBus = self.create_new_bus()
        self._material_bus.try_add_part(self)

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

    @property
    def material_bus(self) -> AMaterialBus:
        return self._material_bus

    @material_bus.setter
    def material_bus(self, bus):
        if not isinstance(bus, AMaterialBus):
            raise ValueError(f'not a material bus {repr(bus)}')
        self._material_bus = bus
        self._material_bus.try_add_part(self)

    def connect_input(self, input_object):
        if isinstance(input_object, AMaterialBusUnit):
            self.connect_bus(input_object)
        else:
            self.material_bus.connect_input(input_object)

    def connect_output(self, output_object):
        if isinstance(output_object, AMaterialBusUnit):
            self.connect_bus(output_object)
        else:
            self.material_bus.connect_output(output_object)

    def connect_bus(self, other):
        if self.__class__ == other.__class__:
            AMaterialBus.merge(self.material_bus, other.material_bus)

    def connect_on_grid(self, grid: ObjectCoordinateGrid):
        for cell in self.iter_input_cells():
            grid_obj = grid.get(cell)
            if grid_obj is not None:
                self.connect_input(grid_obj)

        for cell in self.iter_output_cells():
            grid_obj = grid.get(cell)
            if grid_obj is not None:
                self.connect_output(grid_obj)
