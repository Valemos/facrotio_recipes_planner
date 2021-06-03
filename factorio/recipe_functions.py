from typing import Union
from graphviz.dot import Digraph
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.production_unit import *
from .types.crafting_step import CraftingStep
from .types.material import Material
from .types.material_collection import MaterialCollection
from .recipe_collections import recipes_info
from .misc import to_material
from factorio.crafting_sequence import get_crafting_subtree_recursive, get_crafting_tree


def get_basic_materials(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT) -> MaterialCollection:
    '''
    returns dictionary with time, yield amount and dict of (component-id: (amount, time needed for construction))
    '''

    basic_materials = MaterialCollection()
    crafting_tree = get_crafting_tree(to_material(material, 1), environment)
    for step in crafting_tree.iterate_all_steps():
        if step.is_start_step():
            basic_materials += step.get_results()

    return basic_materials


def get_crafting_graph(cur_node: CraftingStep, graph=None):
    if graph is None: 
        graph = Digraph()

    cur_node_id = str(cur_node.get_id())
    cur_node_name = cur_node.get_results().first().id
    if len(cur_node.previous_steps) == 0:
        # for basic nodes specify their total amount and no crafting time
        graph.node(cur_node_id, label=f"{cur_node_name}\\n x{cur_node.config.producers_amount}\\n")
        return

    # put label on current node
    production_rate = cur_node.config.get_production_rate()
    node_label = f"{cur_node_name}\\n{production_rate} items/s\\n"
    if cur_node.config.producers_amount != float('inf'):
        node_label += f"x{cur_node.config.producers_amount}\\n"
    graph.node(cur_node_id, label=node_label)

    for prev_node in cur_node.previous_steps:
        required_resources = prev_node.get_results()
        prev_node_id = str(prev_node.get_id())

        graph.edge(prev_node_id, cur_node_id, label=str(required_resources.first().amount))
        
        get_crafting_graph(prev_node, graph)

    return graph


def build_recipe_graph(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT):
    return get_crafting_graph(get_crafting_tree(to_material(material, float('inf')), environment))

