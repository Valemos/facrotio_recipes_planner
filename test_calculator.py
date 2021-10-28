from factorio.recipe_graph.graph import build_recipe_graph
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment

environment = VirtualCraftingEnvironment(["iron-plate", "copper-plate", "stone"])
graph = build_recipe_graph("electronic-circuit", environment)

graph.render("test_graph", "/media/data/coding/Python_codes/factorio/graph", format="png")
