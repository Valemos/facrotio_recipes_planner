from abc import ABC

from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid


class AMaterialConnectionNode(ABC):

    def __init__(self) -> None:
        self._inputs: list[AMaterialConnectionNode] = []
        self._outputs: list[AMaterialConnectionNode] = []

    def notify_inputs_changed(self):
        pass

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

    def get_inputs(self):
        return list(self._inputs)

    def get_outputs(self):
        return list(self._outputs)

    def is_source_step(self):
        """returns True if node represents basic resource in crafting tree"""
        return len(self._inputs) == 0

    def iterate_up_to_bottom(self):
        yield self
        for prev_step in self._inputs:
            yield from prev_step.iterate_up_to_bottom()

    def iterate_bottom_to_up(self):
        for prev_step in self._inputs:
            yield from prev_step.iterate_bottom_to_up()
        yield self

    def get_root_step(self):
        root_step = self
        while root_step.outputs is not None:
            root_step = root_step.outputs
        return root_step
