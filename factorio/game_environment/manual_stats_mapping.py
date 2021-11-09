from json_automatic.enum_named_objects import EnumNamedObjects
from json_automatic.i_json_serializable import IJsonSerializable

from factorio.crafting_tree_builder.internal_types.named_item import NamedObject
from factorio.crafting_tree_builder.placeable_types.pipe_unit import PipeUnit
from factorio.crafting_tree_builder.placeable_types.splitter_unit import SplitterUnit
from factorio.crafting_tree_builder.placeable_types.underground_pipe_unit import UndergroundPipeUnit
from factorio.crafting_tree_builder.placeable_types.underground_belt_unit import UndergroundBeltUnit


class ManualStatsMapping(IJsonSerializable, EnumNamedObjects):

    SPLITTER = NamedObject("splitter", SplitterUnit(item_rate=15))
    UNDERGROUND_BELT = NamedObject("underground-belt", UndergroundBeltUnit(item_rate=15))
    PIPE = NamedObject("pipe", PipeUnit())
    UNDERGROUND_PIPE = NamedObject("underground-pipe", UndergroundPipeUnit())

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json_object: dict):
        return cls(json_object)
