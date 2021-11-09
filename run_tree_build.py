import json
from pathlib import Path
from PIL import Image

from choice_form_app import ChoiceFormApp
from factorio.crafting_tree_builder.choice_collection import UserChoiceCollection
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.user_object_choice import UserObjectChoiceCollection
from factorio.production_config_builder import VirtualProductionConfigBuilder
from factorio.recipe_graph.graph import build_recipe_graph
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment


# load current choices
session_choices_path = Path("./session_choices.json")
try:
    with session_choices_path.open('r') as fin:
        choices = UserObjectChoiceCollection.from_json(json.load(fin))
    config_builder = VirtualProductionConfigBuilder(choices=UserChoiceCollection(ChoiceFormApp, choices))
except OSError:
    config_builder = None


environment = VirtualCraftingEnvironment(
    ["iron-ore", "copper-ore", "coal", "stone", "water", "crude-oil"],
    config_builder
)


image_path = Path("/home/anton/coding/Python_codes/factorio/graph/test_graph.png")
graph, tree = build_recipe_graph(Material("production-science-pack", 1), environment, image_path)
Image.open(image_path).show()

source_materials = MaterialCollection()
for source in tree.iter_sources():
    for m in source.get_output_rates():
        source_materials.add(m)

print('\n'.join(str(m) for m in source_materials))


# save choices
choices = environment.node_config_builder.choices.get_temporary().to_json()
with session_choices_path.open('w') as fout:
    json.dump(choices, fout)
