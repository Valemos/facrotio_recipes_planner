from factorio.types.crafting_environment import CraftingEnvironment
from factorio.recipe_functions import build_recipe_graph, get_basic_resources, get_crafting_sequence
import factorio.types.transport_unit as transport

crafting_environment = CraftingEnvironment(['electronic-circuit', 'copper-plate', 'iron-plate'])

result = get_basic_resources(transport.transport_belt_1, crafting_environment)
print(result)
pass