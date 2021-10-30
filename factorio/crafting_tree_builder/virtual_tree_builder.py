from factorio.virtual_crafting_environment import VirtualCraftingEnvironment
from factorio.crafting_tree_builder.internal_types.material import Material


def build_for_material(material: Material, env: VirtualCraftingEnvironment):

    root = env.node_config_builder.build_material_node(material)
    root.constrained = True
    root.build_subtrees(env)

    for node in root.iter_child_to_root():
        if node.get_output_rates().first().amount == float("inf"):
            print(f'source material has infinite output "{node.recipe.name}"')

        if node.constrained:
            node.handle_inputs_changed()
            node.propagate_sufficient_inputs()

    return root
