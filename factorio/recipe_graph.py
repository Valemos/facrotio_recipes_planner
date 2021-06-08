from typing import Dict, List, Tuple, Union
from graphviz.dot import Digraph
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.production_unit import *
from .types.crafting_step import CraftingStep
from .types.material import Material
from .types.material_collection import MaterialCollection
from .recipe_collections import recipes_info
from .misc import to_material
from .crafting_sequence import get_crafting_tree



def _get_next_node_id(group_id, group_ids, increment=1000):
    if group_id in group_ids:
        return max(group_ids[group_id]) + increment
    else:
        return group_id + increment 


def _add_group_node_id(group_id, node_id, group_ids):
    if group_id in group_ids:
        group_ids[group_id].append(node_id)
    else:
        group_ids[group_id] = [node_id]


def _add_node_to_cluster(group_id, new_node_id, label, node_clusters: Dict[int, Digraph]):
    if group_id not in node_clusters:
        node_clusters[group_id] = Digraph()

    cluster = node_clusters[group_id]
    if new_node_id is None:
        print(group_id)
    cluster.node(str(new_node_id), label)


def _add_group_node(node: CraftingStep, label: str, node_clusters: Dict[int, Digraph], group_ids: Dict[int, List[int]]):
    group_id = node.get_id()
    new_node_id = _get_next_node_id(group_id, group_ids)

    _add_group_node_id(group_id, new_node_id, group_ids)

    _add_node_to_cluster(group_id, new_node_id, label, node_clusters)
    return new_node_id


def _get_intermediate_step_label(step: CraftingStep):
    if step.is_source_step():
        production_rate = step.config.producers_amount
    else:
        production_rate = step.config.get_production_rate()
    
    step_label = f"{step.get_results().first().id}\\n{round(production_rate, 3)} items/s\\n"
    if step.config.producers_amount != float('inf'):
        step_label += f"x{step.config.producers_amount}\\n"

    return step_label

def _get_first_step_label(step):
    return f"{step.get_results().first().id}\\n {round(step.config.producers_amount, 3)} items/s\\n"


def _get_edge_label(prev_node: CraftingStep, cur_node: CraftingStep):
    return f" {round(prev_node.get_results().first().amount, 3)} "


def build_crafting_tree_graph(cur_node: CraftingStep, graph=None, node_clusters=None, group_ids=None):
    is_root_node = False
    if graph is None:
        is_root_node = True
        graph = Digraph()
        node_clusters: Dict[int, Digraph] = {}  # for each group save it`s cluster
        group_ids: Dict[int, List[int]] = {}  # for each step we save it`s new_id

    if len(cur_node.previous_steps) == 0:
        # for basic nodes specify their total amount and no crafting time
        return _add_group_node(cur_node, _get_first_step_label(cur_node), node_clusters, group_ids)

    new_cur_node_id = _add_group_node(cur_node, _get_intermediate_step_label(cur_node), node_clusters, group_ids)

    for prev_node in cur_node.previous_steps:
        new_prev_node_id = build_crafting_tree_graph(prev_node, graph, node_clusters, group_ids)
        graph.edge(str(new_prev_node_id), str(new_cur_node_id), label=_get_edge_label(prev_node, cur_node))

    if not is_root_node:
        return new_cur_node_id
    
    # connect subgraphs for root node
    for cluster in node_clusters.values():
        graph.subgraph(cluster)

    return graph


def build_recipe_graph(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT):
    return build_crafting_tree_graph(get_crafting_tree(to_material(material, float('inf')), environment))

