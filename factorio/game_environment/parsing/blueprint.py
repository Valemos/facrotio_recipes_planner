from dataclasses import dataclass, field

from serialization.a_optional_json_serializable import AOptionalJsonSerializable
from .blueprint_object import BlueprintObjectList
from .types.icon import IconList
from .types.tile import TileList


@dataclass
class Blueprint(AOptionalJsonSerializable):
    item: str = None
    label: str = None
    label_color: dict = None
    objects: BlueprintObjectList = field(default_factory=BlueprintObjectList)
    tiles: TileList = None
    icons: IconList = None
    schedules: list = None
    version: int = None

    def to_json(self):
        return {"blueprint": super().to_json()}

    @classmethod
    def from_json(cls, json_object: dict):
        return super().from_json(json_object["blueprint"])
