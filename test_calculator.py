from factorio.recipe_functions import get_basic_resources, get_crafting_sequence


ready_components = ['electronic-circuit', 'copper-plate', 'iron-plate']
result = get_crafting_sequence('gun-turret', ready_components)
pass