import itertools
import unittest

from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.material_buses import ItemBus, FluidBus
from factorio.crafting_tree_builder.placeable_types.pipe_unit import PipeUnit
from factorio.crafting_tree_builder.placeable_types.transport_belt_unit import TransportBeltUnit
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.position import Position


class TestMaterialBus(unittest.TestCase):

    def assertAllEqual(self, it):
        first = next(it)
        self.assertTrue(all(obj == first for obj in it))

    def test_material_bus_empty_created(self):
        bus = ItemBus()
        self.assertEqual(len(list(bus.iter_parts())), 0)

    def test_cannot_connect_different_type_buses(self):
        bus1 = ItemBus()
        bus2 = FluidBus()

        self.assertRaises(ValueError, lambda: AMaterialBus.merge(bus1, bus2))

    def test_add_transport(self):
        bus = ItemBus()
        transport = TransportBeltUnit(item_rate=20).set_placement(direction=DirectionType.UP)
        bus.try_add_part(transport)

        self.assertEqual(list(bus.iter_parts())[0], transport)
        self.assertEqual(bus, transport.material_bus)

    def test_cannot_add_incorrect_type_transport(self):
        bus = FluidBus()
        transport = TransportBeltUnit(item_rate=20).set_placement(direction=DirectionType.UP)
        bus.try_add_part(transport)

        self.assertEqual(len(list(bus.iter_parts())), 0)
        self.assertNotEqual(bus, transport.material_bus)

    def test_belts_connected(self):
        grid = ObjectCoordinateGrid()
        belt1 = TransportBeltUnit().set_placement(Position(0, 0), DirectionType.UP)
        belt2 = TransportBeltUnit().set_placement(Position(0, 1), DirectionType.UP)
        belt3 = TransportBeltUnit().set_placement(Position(0, 2), DirectionType.UP)

        belt1.place_on_grid(grid)
        belt2.place_on_grid(grid)
        belt3.place_on_grid(grid)

        self.assertAllEqual((b.material_bus for b in (belt1, belt2, belt3)))

    def test_underground_belts(self):
        # todo finish test
        pass

    def test_create_merge_buses_after_new_elements_inserted(self):
        grid = ObjectCoordinateGrid()
        pos = Position(0, 0)
        transports1 = [TransportBeltUnit().set_placement(pos.add_x(i), DirectionType.RIGHT) for i in range(3)]
        transports2 = [TransportBeltUnit().set_placement(pos.add_y(i), DirectionType.DOWN) for i in range(1, 4)]

        for t in transports1:
            t.place_on_grid(grid)

        self.assertAllEqual((t.material_bus for t in transports1))

        self.assertNotEqual(transports1[0].material_bus, transports2[0].material_bus)

        for t in transports2:
            t.place_on_grid(grid)

        self.assertAllEqual(itertools.chain((t.material_bus for t in transports1),
                                            (t.material_bus for t in transports2)))

        for el in transports1[0].material_bus.iter_parts():
            self.assertTrue(el in transports1 or el in transports2)

    def test_pipe_bus(self):
        grid = ObjectCoordinateGrid()
        pos = Position()
        points = [pos.add_x(p) for p in range(4)]
        points2 = [points[-1].add_y(p) for p in range(1, 4)]
        points.extend(points2)
        pipes = [PipeUnit().set_placement(position=p) for p in points]

        for pipe in pipes:
            pipe.place_on_grid(grid)

        self.assertAllEqual(pipe.material_bus for pipe in pipes)

        bus_pipes = list(pipes[0].material_bus.iter_parts())
        self.assertTrue(all(pipe in bus_pipes for pipe in pipes))

    def test_underground_pipes(self):
        # todo finish test
        pass
