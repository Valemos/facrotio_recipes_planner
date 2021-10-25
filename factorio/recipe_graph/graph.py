from typing import Dict, List, Union

from graphviz.dot import Digraph

from factorio.crafting_tree_builder.virtual_tree_builder import build_for_material
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode


def build_crafting_tree_graph(cur_node: AMaterialConnectionNode, graph=None, node_clusters=None, group_ids=None):
    is_root_node = False
    if graph is None:
        is_root_node = True
        graph = Digraph()
        node_clusters: Dict[int, Digraph] = {}  # for each group save it`s cluster
        group_ids: Dict[int, List[int]] = {}  # for each step we save it`s new_id

    if cur_node.is_source_step().inputs:
        if is_root_node:
            graph.node(cur_node)
            return graph

        # for source nodes specify their total amount and no crafting time
        return _add_group_node(cur_node, _get_first_step_label(cur_node), node_clusters, group_ids)

    new_cur_node_id = _add_group_node(cur_node, _get_intermediate_step_label(cur_node), node_clusters, group_ids)

    prev_node: AMaterialConnectionNode
    for prev_node in cur_node.get_inputs():
        new_prev_node_id = build_crafting_tree_graph(prev_node, graph, node_clusters, group_ids)
        graph.edge(str(new_prev_node_id), str(new_cur_node_id), label=_get_edge_label(prev_node, cur_node))

    if not is_root_node:
        return new_cur_node_id
    
    # connect subgraphs for root node
    for cluster in node_clusters.values():
        graph.subgraph(cluster)

    return graph


def build_recipe_graph(material: Union[str, Material], environment: VirtualCraftingEnvironment):
    return build_crafting_tree_graph(build_for_material(Material.from_obj(material, float('inf')), environment))


def build_graph(root: AMaterialConnectionNode):

    graph = Digraph()
    nodes = {}

    for node in root.iter_root_to_child():
        nodes[id(node)] = node

    for parent_node, child_node, material in root.iter_connections():
        # todo finish with hidden nodes
        pass
