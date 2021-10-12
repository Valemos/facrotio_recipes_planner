from factorio.types.inserter_unit import InserterUnit
from factorio.types.production_unit import ProductionUnit
from factorio.types.transport_belt import TransportBelt

assembling_machine_inf = ProductionUnit(float('inf'))
assembling_machine_1 = ProductionUnit(0.5)
assembling_machine_2 = ProductionUnit(0.75)
assembling_machine_3 = ProductionUnit(1.25)

furnace_1 = ProductionUnit(1)
furnace_2 = ProductionUnit(2)
furnace_3 = ProductionUnit(2)

chemical_plant = ProductionUnit(1)
oil_refinery = ProductionUnit(1)

transport_belt_inf = TransportBelt(item_rate=float('inf'), name="")
transport_belt_1 = TransportBelt(item_rate=15, name="transport-belt")
transport_belt_2 = TransportBelt(item_rate=30, name="fast-transport-belt")
transport_belt_3 = TransportBelt(item_rate=45, name="express-transport-belt")

inserter_inf = InserterUnit("", cycle_speed=float('inf'), capacity=1)
inserter = InserterUnit("inserter", cycle_speed=0.83, capacity=1)
inserter_long = InserterUnit("long-handed-inserter", cycle_speed=1.20, capacity=1)
inserter_fast = InserterUnit("fast-inserter", cycle_speed=2.31, capacity=1)
inserter_filter = InserterUnit("filter-inserter", cycle_speed=2.31, capacity=1)
inserter_stack = InserterUnit("stack-inserter", cycle_speed=2.31, capacity=2)
inserter_stack_filter = InserterUnit("stack-filter-inserter", cycle_speed=2.31, capacity=2)
