import unittest

from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.game_environment.parsing.types.position import Position


class TestGrid(unittest.TestCase):

    def test_empty_grid_created(self):
        grid = ObjectCoordinateGrid()
        self.assertEqual(grid.size_x, 0)
        self.assertEqual(grid.size_y, 0)

    def test_grid_resized_first_object_to_1x1(self):
        grid = ObjectCoordinateGrid()
        grid.place_object(1, Position(4, 6))
        self.assertEqual(grid.size_x, 1)
        self.assertEqual(grid.size_y, 1)
        self.assertEqual(grid.get(Position(4, 6)), 1)

    def test_grid_place_multiple_negative_coordinates(self):
        grid = ObjectCoordinateGrid()
        grid.place_object(10, Position(-1, -2))
        grid.place_object(100, Position(-1, -3))
        self.assertEqual(grid.size_x, 1)
        self.assertEqual(grid.size_y, 2)
        self.assertEqual(grid.get(Position(-1, -3)), 100)

    def test_different_extension_modes_negative(self):
        """
         2|-|5|-|-|-|
         1|-|-|-|-|-|
         0|-|-|-|-|-|
        -1|-|-|-|-|-|
        -2|2|1|-|-|4|
        -3|-|3|-|-|-|
          -2-1 0 1 2
        """
        grid = ObjectCoordinateGrid()
        grid.place_object(1, Position(-1, -2))
        grid.place_object(2, Position(-2, -2))
        grid.place_object(3, Position(-1, -3))
        grid.place_object(4, Position(2, -2))
        grid.place_object(5, Position(-1, 2))
        self.assertEqual(grid.get(Position(-1, -2)), 1)
        self.assertEqual(grid.get(Position(-2, -2)), 2)
        self.assertEqual(grid.get(Position(-1, -3)), 3)
        self.assertEqual(grid.get(Position(2, -2)), 4)
        self.assertEqual(grid.get(Position(-1, 2)), 5)

    def test_different_extension_modes_positive(self):
        grid = ObjectCoordinateGrid()
        grid.place_object(1, Position(1, 2))
        grid.place_object(2, Position(2, 2))
        grid.place_object(3, Position(1, 3))
        grid.place_object(4, Position(-2, 2))
        grid.place_object(5, Position(1, -2))
        self.assertEqual(grid.get(Position(1, 2)), 1)
        self.assertEqual(grid.get(Position(2, 2)), 2)
        self.assertEqual(grid.get(Position(1, 3)), 3)
        self.assertEqual(grid.get(Position(-2, 2)), 4)
        self.assertEqual(grid.get(Position(1, -2)), 5)
