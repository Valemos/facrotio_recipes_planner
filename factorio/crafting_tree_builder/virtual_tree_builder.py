from factorio.virtual_crafting_environment import VirtualCraftingEnvironment
from factorio.crafting_tree_builder.internal_types.material import Material


def build_for_material(material: Material, env: VirtualCraftingEnvironment):

    root = env.node_config_builder.build_material(material)
    root.build_subtrees(env.node_config_builder)

    for node in root.iter_sources():
        if node.get_output_rates().first().amount == float("inf"):
            print(f'source material has infinite output "{node.recipe.name}"')
        node.handle_inputs_changed()

    return root
