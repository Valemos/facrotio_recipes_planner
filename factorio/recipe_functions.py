from typing import Union
from graphviz.dot import Digraph
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.production_unit import *
from .types.crafting_step import CraftingStep
from .types.material import Material
from .types.material_collection import MaterialCollection
from .recipe_collections import recipes_info
from .misc import to_material
from factorio.crafting_sequence import get_crafting_sequence


def get_basic_resources(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT) -> MaterialCollection:
    '''
    returns dictionary with time, yield amount and dict of (component-id: (amount, time needed for construction))
    '''

    material = to_material(material) # set material amount to default
    recipe = recipes_info[material.id]
    
    if environment.is_final_recipe(recipe):
        return recipe.craft(material.amount)

    basic_materials = MaterialCollection()
    basic_materials.add(recipe.get_time_material())

    for ingredient in recipe.ingredients:
        ingredient_basics = get_basic_resources(ingredient, environment)
        for basic in ingredient_basics:
            basic_materials.add(basic * material.amount)

    return basic_materials


def get_crafting_graph(cur_node: CraftingStep, graph=None, visited_nodes=None):
    if graph is None: 
        graph = Digraph()
        visited_nodes = {}

    cur_node_id = cur_node.get_id()
    if len(cur_node.previous_steps) == 0:
        # for basic nodes specify their total amount and no crafting time
        graph.node(cur_node_id, label=f"{cur_node_id}\\nx{cur_node.amount_producers}\\n")
        return

    # avoid cycles
    if cur_node_id in visited_nodes:
        return
    visited_nodes[cur_node_id] = cur_node

    # put label on current node
    craft_time = cur_node.config.machine.get_craft_time()
    graph.node(cur_node_id, label=f"{cur_node_id}\\n{craft_time}s x{cur_node.amount_producers}\\n")

    for prev_node in cur_node.previous_steps:
        required_resources = prev_node.get_result()
        prev_node_id = prev_node.get_id()

        graph.edge(prev_node_id, cur_node_id, label=str(required_resources.first().amount))
        
        get_crafting_graph(prev_node, graph, visited_nodes)

    return graph


def build_recipe_graph(component_id, environment: CraftingEnvironment = DEFAULT_ENVIRONMENT):
    return get_crafting_graph(get_crafting_sequence(component_id, environment))

