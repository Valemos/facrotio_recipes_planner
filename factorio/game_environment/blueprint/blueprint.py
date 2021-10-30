from dataclasses import dataclass, field

from json_automatic.a_optional_json_serializable import AOptionalJsonSerializable

from .blueprint_object import BlueprintObjectList
from .types.icon import IconList
from .types.tile import TileList
from ..factorio_serialization_format import deserialize_factorio_format, serialize_factorio_format


@dataclass
class Blueprint(AOptionalJsonSerializable):
    item: str = None
    label: str = None
    label_color: dict = None
    entities: BlueprintObjectList = field(default_factory=BlueprintObjectList)
    tiles: TileList = None
    icons: IconList = None
    schedules: list = None
    version: int = None

    def to_json(self):
        return {"blueprint": super().to_json()}

    @classmethod
    def from_json(cls, json_object: dict):
        return super().from_json(json_object["blueprint"])

    @classmethod
    def from_factorio_string(cls, string):
        return cls.from_json(deserialize_factorio_format(string))

    def to_factorio_string(self):
        return serialize_factorio_format(self.to_json())
