import unittest

from factorio.crafting_tree_builder.placeable_types.a_material_bus import AMaterialBus
from factorio.crafting_tree_builder.placeable_types.material_buses import ItemBus, FluidBus
from factorio.crafting_tree_builder.placeable_types.transport_belt_unit import TransportBeltUnit
from factorio.game_environment.blueprint.types.direction_type import DirectionType


class TestMaterialBus(unittest.TestCase):

    def test_material_bus_empty_created(self):
        bus = ItemBus()
        self.assertEqual(len(bus), 0)

    def test_cannot_connect_different_type_buses(self):
        bus1 = ItemBus()
        bus2 = FluidBus()

        self.assertRaises(ValueError, lambda: AMaterialBus.merge(bus1, bus2))

    def test_add_transport(self):
        bus = ItemBus()
        transport = TransportBeltUnit(DirectionType.UP, item_rate=20)
        bus.try_add(transport)

        self.assertEqual(bus[0], transport)
        self.assertEqual(bus, transport.material_bus)

    def test_cannot_add_incorrect_type_transport(self):
        bus = FluidBus()
        transport = TransportBeltUnit(DirectionType.UP, item_rate=20)
        bus.try_add(transport)

        self.assertEqual(len(bus), 0)
        self.assertNotEqual(bus, transport.material_bus)

    def test_create_and_merge_buses(self):
        transports1 = [TransportBeltUnit(DirectionType.UP, item_rate=20) for _ in range(3)]
        transports2 = [TransportBeltUnit(DirectionType.UP, item_rate=10) for _ in range(3)]

        transports1[0].try_connect(transports1[1])
        transports1[1].try_connect(transports1[2])

        transports2[0].try_connect(transports2[1])
        transports2[1].try_connect(transports2[2])

        self.assertEqual(transports1[0].material_bus, transports1[1].material_bus)
        self.assertEqual(transports1[0].material_bus, transports1[2].material_bus)

        self.assertNotEqual(transports1[0].material_bus, transports2[0].material_bus)

        self.assertEqual(transports2[0].material_bus, transports2[1].material_bus)
        self.assertEqual(transports2[0].material_bus, transports2[2].material_bus)

        AMaterialBus.merge(transports1[2].material_bus, transports2[2].material_bus)

        self.assertEqual(transports1[0].material_bus, transports2[0].material_bus)

        for el in transports1[0].material_bus:
            self.assertTrue(el in transports1 or el in transports2)
