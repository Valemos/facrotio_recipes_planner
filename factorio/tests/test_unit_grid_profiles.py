import unittest

from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit
from factorio.crafting_tree_builder.placeable_types.splitter_unit import SplitterUnit
from factorio.crafting_tree_builder.placeable_types.transport_belt_unit import TransportBeltUnit
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


class TestUnitGridProfiles(unittest.TestCase):

    def obj_test(self, unit, obj_cells, input_cells, output_cells):
        s = unit
        self.assertEqual(obj_cells, set(s.iter_object_cells()))
        self.assertEqual(input_cells, set(s.iter_input_cells()))
        self.assertEqual(output_cells, set(s.iter_output_cells()))

    def test_splitter_directions(self):
        obj_pos1 = Position(163.5, -23)
        h_body = {Position(163, -23), Position(163, -24)}
        h_left = {p.add_x(1) for p in h_body}
        h_right = {p.add_x(-1) for p in h_body}
        self.obj_test(SplitterUnit().set_placement(obj_pos1, DirectionType.RIGHT), h_body, h_left, h_right)
        self.obj_test(SplitterUnit().set_placement(obj_pos1, DirectionType.LEFT), h_body, h_right, h_left)

        obj_pos2 = Position(166, -23.5)
        v_body = {Position(165, -24), Position(166, -24)}
        v_up = {p.add_y(1) for p in v_body}
        v_down = {p.add_y(-1) for p in v_body}
        self.obj_test(SplitterUnit().set_placement(obj_pos2, DirectionType.UP), v_body, v_down, v_up)
        self.obj_test(SplitterUnit().set_placement(obj_pos2, DirectionType.DOWN), v_body, v_up, v_down)

    def test_belt_directions(self):
        obj_pos = Position(-120.5, 66.5)
        body = {Position(-120, 66)}
        cells_up = {obj_pos.add_y(1)}
        cells_down = {obj_pos.add_y(-1)}
        cells_right = {obj_pos.add_x(1)}
        cells_left = {obj_pos.add_x(-1)}

        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.LEFT), body, cells_right, cells_left)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.RIGHT), body, cells_left, cells_right)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.UP), body, cells_down, cells_up)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.DOWN), body, cells_up, cells_down)

    def test_pipe_directions(self):
        obj_pos = Position(-120.5, 66.5)
        body = {Position(-120, 66)}
        cells_up = {obj_pos.add_y(1)}
        cells_down = {obj_pos.add_y(-1)}
        cells_right = {obj_pos.add_x(1)}
        cells_left = {obj_pos.add_x(-1)}

        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.LEFT), body, cells_right, cells_left)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.RIGHT), body, cells_left, cells_right)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.UP), body, cells_down, cells_up)
        self.obj_test(TransportBeltUnit().set_placement(obj_pos, DirectionType.DOWN), body, cells_up, cells_down)
