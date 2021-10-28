from factorio.crafting_tree_builder.placeable_types.a_sized_grid_object import ASizedGridObject
from factorio.deterministic_hash import hash_det


class AssemblingMachineUnit(ASizedGridObject):
    """represents one unit of crafting machinery, that can be placed on object grid"""

    def __init__(self, name: str = "", crafting_speed: float = 0):
        super().__init__()
        self.name = name
        self.crafting_speed = crafting_speed  # amount of work / time unit
        self.time_multiplier = 1 / crafting_speed  # coefficient to multiply recipe crafting time

    def __str__(self):
        return f"{self.name}: {self.crafting_speed} work/s"

    def __hash__(self):
        return hash_det((self.position, self.direction, self.name))

    def get_id(self):
        return hash(self.name)

    def iter_object_cells(self):
        # assume it's 3x3 and position is in center
        pos = self.grid_position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                yield pos.add(dx, dy)

    def connect_on_grid(self, grid):
        pass

    def iter_input_cells(self):
        yield from []

    def iter_output_cells(self):
        yield from []
