
from .misc import to_material
from .types.crafting_step import CraftingStep
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.material import Material
from typing import Dict, Union
from .recipe_collections import recipes_info


def get_crafting_sequence(material: Union[str, Material], 
                        environment: CraftingEnvironment = DEFAULT_ENVIRONMENT,
                        visited_nodes: Dict[str, CraftingStep] = None) -> CraftingStep:
    """
    this function gets all crafting steps from environment, connects them into tree
    as the final step, all unconstrained tree nodes update their config considering all previous connections
    """
    
    if visited_nodes is None:
        visited_nodes = {}

    material = to_material(material)
    recipe = recipes_info[material.id]

    # repeating resources must connect into one node
    cur_step_id = recipe.global_id
    if cur_step_id in visited_nodes:
        # return already visited node as subtree to update 
        return visited_nodes[cur_step_id]

    config = environment.get_production_config(recipe)
    config.machine_amount = recipe.get_result_amount(material)
    cur_step = CraftingStep()
    visited_nodes[cur_step_id] = cur_step

    for ingredient in cur_step.get_required_materials():
        # get all subtrees
        prev_step = get_crafting_sequence(ingredient, environment, visited_nodes)

        # connect tree
        cur_step.previous_steps.append(prev_step)
        prev_step.next_steps.append(cur_step)

    add_tree_producers_constraints(cur_step)
    return cur_step


def add_tree_producers_constraints(root_step: CraftingStep):
    """calculate all not fixed nodes in tree"""

    if root_step.fixed_nodes_count() == 0:
        root_step.config.fixed = True
