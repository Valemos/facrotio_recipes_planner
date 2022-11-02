from factorio.crafting_tree_builder.i_assembler_config import IAssemblerConfig
from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.placeable_types.a_material_connection_node import AMaterialConnectionNode
from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit


class ProductionNode(IAssemblerConfig, AMaterialConnectionNode):

    def __init__(self, assembler: AssemblingMachineUnit, recipe: Recipe) -> None:
        super().__init__()
        self._assembler = assembler
        self._recipe = recipe

    @property
    def recipe(self) -> Recipe:
        return self._recipe

    @property
    def constrained(self) -> bool:
        return False

    @property
    def is_hidden_node(self) -> bool:
        return False

    def get_required_rates(self) -> MaterialCollection:
        return self._recipe.ingredient_rates * self._assembler.crafting_speed

    def set_max_consumers(self, input_materials: MaterialCollection):
        return

    def set_result_rate(self, material: Material):
        pass

    def get_source_materials(self):
        basic_materials = MaterialCollection()
        for step in self.iter_root_to_child():
            if step.is_source_step:
                basic_materials += step.config.recipe.get_results()

        return basic_materials

    def set_machine_amount_by_inputs(self):
        input_materials = MaterialCollection()
        for prev_step in self.get_inputs():
            input_materials += prev_step.recipe.results

        self.set_max_consumers(input_materials)

    def propagate_output_constraints(self):
        current_step: ProductionNode = self.outputs
        while current_step is not None:
            current_step.set_machine_amount_by_inputs()
            current_step = current_step.outputs

    def deduce_infinite_materials(self):
        """
        algorithm assumes, that for each ingredient in this node, there are only one ingredient source node
        """
        # todo rework this if necessary
        required_inputs = self.get_required_rates()
        if len(required_inputs) == 0:
            return

        material_source_steps = self.get_material_source_steps(required_inputs)

        ingredient_step: ProductionNode
        for requested_material, ingredient_step in material_source_steps.items():
            if not ingredient_step.constrained:
                ingredient_step.set_result_rate(requested_material)

            ingredient_step.deduce_infinite_materials()
