from typing import Union
from graphviz.dot import Digraph
from .types.crafting_environment import CraftingEnvironment
from .types.production_unit import *
from .types.crafting_step import CraftingStep
from .types.material import Material
from .types.material_collection import MaterialCollection
from .recipe_collections import recipes_info
from .misc import to_material
import math


def is_final_material(material: Material, environment: CraftingEnvironment):
    if environment is not None:
        if material in environment.materials:
            return True

    # if not found in ready components, check if object is the simplest component    
    return len(recipes_info[material.id].ingredients) == 0


def get_basic_resources(material: Union[str, Material], environment: CraftingEnvironment = None) -> MaterialCollection:
    '''
    returns dictionary with time, yield amount and dict of (component-id: (amount, time needed for construction))
    '''

    material = to_material(material) # set material amount to default
    material_recipe = recipes_info[material.id]
    
    if is_final_material(material, environment):
        return material_recipe.craft(material.amount)

    basic_materials = MaterialCollection()
    basic_materials.add(material_recipe.get_time_material())

    for ingredient in material_recipe.ingredients:
        ingredient_basics = get_basic_resources(ingredient, environment)
        for basic in ingredient_basics:
            basic_materials.add(basic * material.amount)

    return basic_materials


def get_producers_number(material: Material, recipe: Recipe):
    '''calculates current material producers based on recipe output'''

    output_amount = recipe.get_result_amount(material)
    return math.ceil(material.amount / output_amount)


def get_crafting_sequence(material: Union[str, Material], environment: CraftingEnvironment) -> CraftingStep:
    
    if isinstance(material, str): 
        material = Material(material)
        
    recipe = recipes_info[material.id]

    root_step = CraftingStep(
        environment.crafting_machine.setup(recipe), 
        amount_producers = get_producers_number(material, recipe)
    )

    if is_final_material(material, environment):
        return root_step

    for ingredient in root_step.get_requirements():
        prev_step = get_crafting_sequence(ingredient, environment)
        # connect tree
        root_step.previous_steps.append(prev_step)
        prev_step.next_step = root_step

    return root_step


def get_crafting_graph(root_node: CraftingStep, graph=None, visited_nodes=None):
    if graph is None: 
        graph = Digraph()
        visited_nodes = set()

    if len(root_node.previous_steps) == 0:
        return

    root_node_id = root_node.producer.get_id()
    if root_node_id in visited_nodes:
        return

    visited_nodes.add(root_node_id)

    for prev_node in root_node.previous_steps:
        required_resource = prev_node.get_result().first()
        graph.edge(prev_node.get_id(), root_node_id, label=str(required_resource.amount))
        graph.node(root_node_id, label=f"{root_node_id}\\nx{root_node.amount_producers}\\n")
        get_crafting_graph(prev_node, graph, visited_nodes)

    return graph


def build_recipe_graph(component_id, environment: CraftingEnvironment):
    return get_crafting_graph(get_crafting_sequence(component_id, environment))

