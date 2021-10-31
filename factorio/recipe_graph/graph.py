from typing import Union

from graphviz.dot import Digraph

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode
from factorio.crafting_tree_builder.virtual_tree_builder import build_for_material
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment


def _add_node(node: AMaterialConnectionNode, graph: Digraph):
    if node.display_compact:
        graph.node(str(id(node)), shape="point", width=0.1, height=0.1)
    else:
        graph.node(str(id(node)), node.get_node_message())


def _add_edge(node1: AMaterialConnectionNode,
              node2: AMaterialConnectionNode,
              material: Material,
              graph: Digraph):
    graph.edge(str(id(node1)), str(id(node2)), f"{material.name} x {material.amount:.1f}")


def build_graph(root: AMaterialConnectionNode):

    graph = Digraph()
    nodes = {}

    for node in root.iter_root_to_child():
        nodes[str(id(node))] = node

    for parent_node, child_node, material in root.iter_connections():

        _add_node(parent_node, graph)
        _add_node(child_node, graph)
        _add_edge(child_node, parent_node, material, graph)

    return graph


def build_recipe_graph(material: Union[str, Material], environment: VirtualCraftingEnvironment):
    return build_graph(build_for_material(Material.from_obj(material, 1), environment))
