from factorio.types.material import Material
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.recipe_functions import build_recipe_graph, get_basic_resources, get_crafting_sequence
import factorio.types.transport_belt as transport
from factorio.types.production_config import ProductionConfig
from factorio.recipe_collections import recipes_info
from factorio.types.production_unit import assembling_machine_1


environment = CraftingEnvironment(['electronic-circuit', 'copper-plate', 'iron-plate'])
environment.add_constraint(
    ProductionConfig(
        assembling_machine_1.setup(recipes_info['electronic-circuit']),
        machine_amount=3))

# TODO: fix incorrect crafting sequence
result = get_crafting_sequence('assembling-machine-1', environment)
print(result)

# name = "iron-stick"
# config = environment.get_production_config(recipes_info[name])
# result = config.get_producers_number(Material(name, 10))
pass