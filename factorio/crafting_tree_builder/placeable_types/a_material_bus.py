from abc import abstractmethod, ABC

from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialConnectionNode
from factorio.game_environment.object_stats.material_type import MaterialType


class AMaterialBus(AMaterialConnectionNode, ABC):
    """collection of objects that deliver materials to assemblers"""

    def __init__(self) -> None:
        super().__init__()
        self._transport_objects: list = []

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all(id(o1) == id(o2) for o1, o2 in zip(iter(self._transport_objects), iter(other._transport_objects)))
        else:
            return False

    def __len__(self):
        return len(self._transport_objects)

    def iter_parts(self):
        yield from self._transport_objects

    def try_add_part(self, obj) -> None:
        if obj.material_type != self.material_type:
            return

        if obj not in self._transport_objects:
            obj._material_bus = self
            self._transport_objects.append(obj)

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

        for part in second.iter_parts():
            first.try_add_part(part)

        for inp in second.get_inputs():
            first.connect_input(inp)

        for out in second.get_outputs():
            first.connect_output(out)

        for out in first.get_outputs():
            out.notify_inputs_changed()
