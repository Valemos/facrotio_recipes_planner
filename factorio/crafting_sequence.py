
from copy import deepcopy
from factorio.types.material_collection import MaterialCollection
from .misc import to_material
from .types.crafting_step import CraftingStep
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.material import Material
from typing import Dict, List, Tuple, Union
from .recipe_collections import recipes_info


def get_crafting_tree(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT):
    material = to_material(material, float('inf'))
    
    # constrain desired craft in tree if material amount is not 0
    if material.amount != float('inf'):
        environment = deepcopy(environment)
        environment.add_constraint_amount_produced(material)
    
    crafting_tree, constrained_steps = get_crafting_subtree_recursive(material, environment)
    
    if len(constrained_steps) == 0:        
        print("WARNING! crafting tree has no constraints. add constrains to environment to get not infinite results")
        return crafting_tree

    for step in constrained_steps:
        step.propagate_output_constraints()

    crafting_tree.deduce_infinite_materials()
    
    return crafting_tree


def get_crafting_subtree_recursive(material: Material, 
                                environment: CraftingEnvironment, 
                                constrained_steps: List[CraftingStep] = None) -> Tuple[CraftingStep, List[CraftingStep]]:
    """
    gets all crafting steps from environment and connects them into one tree
    """
    assert isinstance(material, Material)

    if constrained_steps is None:
        constrained_steps = []

    recipe = recipes_info[material.id]

    config = environment.get_production_config(recipe)
    cur_step = CraftingStep(config)

    if cur_step.is_constrained():
        constrained_steps.append(cur_step)
    else:
        cur_step.config.producers_amount = float('inf')

    if environment.is_final_recipe(recipe):
        return cur_step, constrained_steps

    for ingredient in cur_step.get_required():
        # get all subtrees
        prev_step, _ = get_crafting_subtree_recursive(ingredient, environment, constrained_steps)

        # connect tree
        cur_step.previous_steps.append(prev_step)
        prev_step.next_step = cur_step

    return cur_step, constrained_steps
