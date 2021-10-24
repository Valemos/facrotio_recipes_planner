from factorio.crafting_tree_builder.placeable_types.a_item_bus_unit import AItemBusUnit


class TransportBeltUnit(AItemBusUnit):
    def __init__(self, item_rate: float = 0):
        super().__init__()
        self.item_rate = item_rate

    def __str__(self):
        return f"Rate: {self.item_rate} Pos: {self.position}"

    @property
    def max_rate(self):
        return self.item_rate

    def iter_object_cells(self):
        yield self.grid_position

    def iter_input_cells(self):
        yield from self.iter_cell_backward(self.grid_position)

    def iter_output_cells(self):
        yield from self.iter_cell_forward(self.grid_position)
