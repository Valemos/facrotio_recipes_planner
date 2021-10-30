from abc import ABC, abstractmethod

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection


class AMaterialConnectionNode(ABC):

    def __init__(self) -> None:
        self._inputs: list[AMaterialConnectionNode] = []
        self._source_rates = MaterialCollection()
        self._source_nodes: dict[Material, list[AMaterialConnectionNode]] = {}
        self._outputs: list[AMaterialConnectionNode] = []

    @property
    @abstractmethod
    def is_hidden_node(self) -> bool:
        pass

    @property
    def display_compact(self) -> bool:
        """this node will be displayed as point without any """
        return False

    @property
    def is_source_step(self):
        """returns True if node represents basic resource in crafting tree"""
        return False

    @abstractmethod
    def get_node_message(self) -> str:
        pass

    def get_input_rates(self) -> MaterialCollection:
        return self._source_rates

    def get_output_rates(self) -> MaterialCollection:
        return self._source_rates

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def iter_material_sources(self):
        for material, nodes in self._source_nodes.items():
            for source_node in nodes:
                yield self._source_rates[material], source_node

    def _add_material_source(self, input_node, material: Material):
        self._source_rates.add(material)
        if material not in self._source_nodes:
            self._source_nodes[material] = [input_node]
        else:
            self._source_nodes[material].append(input_node)

    def connect_input(self, input_object):
        if not isinstance(input_object, AMaterialConnectionNode):
            raise ValueError("object is not a AMaterialTransport")
        self._inputs.append(input_object)
        input_object._outputs.append(self)
        for material in input_object.get_output_rates():
            self._add_material_source(input_object, material)

    def connect_output(self, output_object):
        if not isinstance(output_object, AMaterialConnectionNode):
            raise ValueError("object is not a AMaterialTransport")
        self._outputs.append(output_object)
        output_object._inputs.append(self)

    def remove_input(self, input_object):
        self._inputs.remove(input_object)

    def remove_output(self, output_object):
        self._outputs.remove(output_object)

    def set_input_rates(self, new_rates: MaterialCollection):
        pass

    def set_output_rates(self, new_rates: MaterialCollection):
        pass

    def handle_inputs_changed(self):
        input_rates = MaterialCollection()
        for inp in self._inputs:
            for rate in inp.get_output_rates():
                input_rates.add(rate)

        self.set_input_rates(input_rates)

        for out in self._outputs:
            out.handle_inputs_changed()

    def iter_root_to_child(self):
        yield self
        for step in self._inputs:
            yield from step.iter_root_to_child()

    def iter_child_to_root(self):
        yield self
        for step in self._outputs:
            yield from step.iter_child_to_root()

    def iter_sources(self):
        for step in self.iter_root_to_child():
            if step.is_source_step:
                yield step

    def iter_connections(self):
        """returns tuple of parent_node, child_node, material and hidden flag"""

        for material, source in self.iter_material_sources():
            if source.is_hidden_node:
                for _, child_source, _ in source.iter_connections():
                    yield self, child_source, material
            else:
                yield self, source, material

        for inp in self._inputs:
            yield from inp.iter_connections()
