from abc import ABC, abstractmethod

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection


class AMaterialConnectionNode(ABC):

    def __init__(self) -> None:
        self._inputs: list[AMaterialConnectionNode] = []
        self._outputs: list[AMaterialConnectionNode] = []

    @abstractmethod
    def set_input_rates(self, new_rates: MaterialCollection):
        pass

    @abstractmethod
    def get_output_rates(self) -> MaterialCollection:
        pass

    @abstractmethod
    def get_input_rates(self) -> MaterialCollection:
        pass

    @abstractmethod
    def is_producer(self):
        """
        returns True if this node should be displayed as graph node,
        otherwise it will be considered a connection
        """
        pass

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def is_source_step(self):
        """returns True if node represents basic resource in crafting tree"""
        return len(self._inputs) == 0

    def connect_input(self, input_object):
        if not isinstance(input_object, AMaterialConnectionNode):
            raise ValueError("object is not a AMaterialTransport")
        self._inputs.append(input_object)
        input_object._outputs.append(self)

    def connect_output(self, output_object):
        if not isinstance(output_object, AMaterialConnectionNode):
            raise ValueError("object is not a AMaterialTransport")
        self._outputs.append(output_object)
        output_object._inputs.append(self)

    def remove_input(self, input_object):
        self._inputs.remove(input_object)

    def remove_output(self, output_object):
        self._outputs.remove(output_object)

    def handle_inputs_changed(self):
        new_inputs = MaterialCollection()

        for inp in self._inputs:
            for rate in inp.get_output_rates():
                new_inputs.add(rate)

        self.set_input_rates(new_inputs)

        for out in self._outputs:
            out.handle_inputs_changed()

    def iterate_root_to_child(self):
        yield self
        for step in self._inputs:
            yield from step.iterate_root_to_child()

    def iterate_child_to_root(self):
        yield self
        for step in self._outputs:
            yield from step.iterate_child_to_root()

    def iterate_all_sources(self):
        for step in self.iterate_root_to_child():
            if step.is_source_step():
                yield step

    def find_material_producers(self, material_name: str):
        for inp in self._inputs:
            if inp.is_producer():
                output_rates = inp.get_output_rates()
                if material_name in output_rates:
                    return inp, output_rates[material_name]

    def iterate_connections(self):
        """returns tuple of parent_node, child_node and material, that is connecting them"""

        inp: AMaterialConnectionNode
        for inp in self._inputs:
            child_outputs = inp.get_output_rates()

        # todo skip non producing nodes
        # todo create result nodes for each unconnected node
        # todo create node connections for each parent node and child
