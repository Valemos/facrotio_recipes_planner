from factorio.crafting_tree_builder.internal_types.output_material_node import OutputMaterialNode
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment
from factorio.crafting_tree_builder.internal_types.material import Material


def build_for_material(material: Material, env: VirtualCraftingEnvironment):

    output = OutputMaterialNode(material)
    root_recipe = env.node_config_builder.build_material_node(material)
    root_recipe.constrained = True
    output.connect_input(root_recipe)

    root_recipe.build_subtrees(env)

    for node in root_recipe.iter_child_to_root():
        if node.constrained:
            node.handle_inputs_changed()
            node.propagate_sufficient_inputs()

    return output
