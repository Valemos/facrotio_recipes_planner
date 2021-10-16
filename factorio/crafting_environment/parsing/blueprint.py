from dataclasses import dataclass, field

from .blueprint_object import BlueprintObjectList, BlueprintObject
from serialization.a_optional_json_serializable import AOptionalJsonSerializable
from .types.icon import IconList
from .types.tile import TileList
from factorio.crafting_environment.imported_stats import get_stats


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

    @staticmethod
    def try_specialize_object(obj: BlueprintObject):
        return get_stats(obj.name).to_object()
