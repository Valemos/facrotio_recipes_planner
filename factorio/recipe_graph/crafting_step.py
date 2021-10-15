from dataclasses import dataclass, field

from factorio.types.material_collection import MaterialCollection
from factorio.crafting_environment.crafting_environment import CraftingEnvironment
from factorio.types.production_config import ProductionConfig


@dataclass(repr=False)
class CraftingStep:
    config: ProductionConfig
    environment: CraftingEnvironment

    # reference to steps of type CraftingStep
    next_step = None
    previous_steps: list = field(default_factory=list)

    def __repr__(self, level=0) -> str:
        result = "\t" * level + repr(self.get_results()) + "\n"
        for child in self.previous_steps:
            result += child.__repr__(level + 1)
        return result

    def is_source_step(self):
        """returns True if node represents basic resourse in crafting tree"""
        return len(self.previous_steps) == 0

    def is_constrained(self):
        return self.config.constrained

    def set_constrained(self, fixed=True):
        self.config.constrained = fixed

    def set_next_step(self, next_step):
        assert isinstance(next_step, self.__class__)
        self.next_step = next_step
        next_step.previous_steps.append(self)

    def get_id(self):
        return self.config.get_recipe().get_id()

    def get_results(self):
        return self.config.get_results_rates()

    def get_required(self):
        return self.config.get_required_rates()

    def iterate_all_steps(self):
        yield self

        for prev_step in self.previous_steps:
            yield from prev_step.iterate_all_steps()

    def find_root_step(self):
        root_step = self
        while root_step.next_step is not None:
            root_step = root_step.next_step
        return root_step

    def get_source_materials(self):
        basic_materials = MaterialCollection()
        for step in self.iterate_all_steps():
            if step.is_source_step():
                basic_materials += step.config.get_results()

        return basic_materials

    def set_machine_amount_by_inputs(self):
        input_materials = MaterialCollection()
        for prev_step in self.previous_steps:
            input_materials += prev_step.get_results()

        self.config.set_maximum_consumers(input_materials)

    def propagate_output_constraints(self):
        current_step: CraftingStep = self.next_step
        while current_step is not None:
            current_step.set_machine_amount_by_inputs()
            current_step = current_step.next_step

    def deduce_infinite_materials(self):
        """
        algorithm assumes, that for each ingredient in this node, there are only one ingredient source node
        """

        required_inputs = self.config.get_required_rates()
        if len(required_inputs) == 0:
            return

        material_source_steps = {}
        for material in required_inputs:
            for step in self.previous_steps:
                if material in step.config.get_recipe().get_results():
                    material_source_steps[material] = step

        for requested_material, ingredient_step in material_source_steps.items():
            if ingredient_step.is_constrained():
                ingredient_step.deduce_infinite_materials()
                continue

            if ingredient_step.is_source_step():
                ingredient_step.config.set_basic_material_rate(requested_material)

            elif ingredient_step.config.producers_amount == float('inf'):
                ingredient_step.config.set_material_rate(requested_material)

            ingredient_step.deduce_infinite_materials()
