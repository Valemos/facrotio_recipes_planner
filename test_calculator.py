from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.recipe_graph.graph import build_recipe_graph, render
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment

environment = VirtualCraftingEnvironment(["iron-ore", "copper-ore", "stone"])
graph = build_recipe_graph(Material("electronic-circuit", 10), environment)
