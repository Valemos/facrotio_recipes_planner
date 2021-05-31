from factorio.production_unit import *
from factorio.crafting_step import CraftingStep
from typing import Union
from factorio.material import Material
from factorio.material_collection import MaterialCollection
from graphviz.dot import Digraph
from .recipe_collections import recipes_info


def is_final_material(material: Material, ready_components: list = None):
    if ready_components is not None:
        if material.id in ready_components:
            return True

    # if not found in ready components, check if object is the simplest component    
    return len(recipes_info[material.id].ingredients) == 0


def get_basic_resources(material: Union[str, Material], ready_components=None) -> MaterialCollection:
    '''
    returns dictionary with time, yield amount and dict of (component-id: (amount, time needed for construction))
    '''

    if isinstance(material, str): 
        material = Material(material) # set material amount to default
    
    material_recipe = recipes_info[material.id]
    
    if is_final_material(material, ready_components):
        return material_recipe.craft(material.amount)

    basic_materials = MaterialCollection()
    basic_materials.add(material_recipe.get_time_material())

    for ingredient in material_recipe.ingredients:
        ingredient_basics = get_basic_resources(ingredient, ready_components)
        for basic in ingredient_basics:
            basic_materials.add(basic * material.amount)

    return basic_materials


def build_recipe_graph(component_id, ready_components=None, graph=None):
    if graph is None:
        graph = Digraph()

    recipe = recipes_info[component_id]

    if is_final_material(Material(component_id), ready_components):
        return graph

    for ingredient in recipe.ingredients:
        graph.edge(ingredient.id, component_id)
        build_recipe_graph(ingredient.id, ready_components, graph)

    return graph


def get_crafting_sequence(material: Union[str, Material], ready_components=None, crafting_machine: ProductionUnit = assembling_machine_1):
    
    if isinstance(material, str): 
        material = Material(material) # set material amount to default
        
    recipe = recipes_info[material.id]

    root_step = CraftingStep(crafting_machine.setup(recipe), recipe.get_result_amount(material))

    if is_final_material(material, ready_components):
        return root_step

    for ingredient in recipe.get_requirements(material.amount):
        prev_step = get_crafting_sequence(ingredient, ready_components, crafting_machine)
        # connect tree
        root_step.previous_steps.append(prev_step)
        prev_step.next_step = root_step

    return root_step


def get_crafting_graph(crafting_sequence: CraftingStep, graph=None, visited_nodes=None):
    if graph is None: 
        graph = Digraph()
        visited_nodes = set()

    if len(crafting_sequence.previous_steps) == 0:
        return

    node_id = crafting_sequence.producer.get_id()
    if node_id in visited_nodes:
        return

    visited_nodes.add(node_id)

    for prev_node in crafting_sequence.previous_steps:
        graph.edge(prev_node.producer.get_id(), crafting_sequence.producer.get_id())
        get_crafting_sequence(prev_node, graph, visited_nodes)

    return graph
