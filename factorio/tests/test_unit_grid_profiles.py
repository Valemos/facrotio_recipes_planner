import unittest

from factorio.crafting_tree_builder.placeable_types.splitter_unit import SplitterUnit
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


class TestUnitGridProfiles(unittest.TestCase):

    def obj_test(self, unit, obj_cells, connection_cells):
        s = unit
        self.assertEqual(obj_cells, set(s.iterate_object_cells()))
        self.assertEqual(connection_cells, set(s.iterate_connection_cells()))

    def test_splitter_directions(self):
        horizontal_body = {Position(163, -23), Position(163, -24)}
        horizontal_conn = {Position(162, -23), Position(162, -24), Position(164, -23), Position(164, -24)}
        self.obj_test(SplitterUnit(DirectionType.RIGHT, Position(163.5, -23)), horizontal_body, horizontal_conn)
        self.obj_test(SplitterUnit(DirectionType.LEFT, Position(163.5, -23)), horizontal_body, horizontal_conn)

        vertical_body = {Position(165, -24), Position(166, -24)}
        vertical_conn = {Position(165, -25), Position(166, -25), Position(165, -23), Position(166, -23)}
        self.obj_test(SplitterUnit(DirectionType.UP, Position(166, -23.5)), vertical_body, vertical_conn)
        self.obj_test(SplitterUnit(DirectionType.DOWN, Position(166, -23.5)), vertical_body, vertical_conn)

    def test_belt_directions(self):
        pass
