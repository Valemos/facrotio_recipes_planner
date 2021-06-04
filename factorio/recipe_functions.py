from typing import Union
from .types.material_collection import MaterialCollection
from .types.crafting_environment import CraftingEnvironment, DEFAULT_ENVIRONMENT
from .types.material import Material
from .crafting_sequence import get_crafting_tree
from .misc import to_material


def get_basic_materials(material: Union[str, Material], environment: CraftingEnvironment = DEFAULT_ENVIRONMENT) -> MaterialCollection:
    '''
    returns dictionary with time, yield amount and dict of (component-id: (amount, time needed for construction))
    '''

    basic_materials = MaterialCollection()
    crafting_tree = get_crafting_tree(to_material(material, 1), environment)
    for step in crafting_tree.iterate_all_steps():
        if step.is_source_step():
            basic_materials += step.get_results()

    return basic_materials
