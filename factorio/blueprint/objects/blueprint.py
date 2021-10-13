from dataclasses import dataclass, field

from factorio.blueprint.objects.entity import EntityList
from factorio.blueprint.objects.icon import IconList
from factorio.blueprint.objects.tile import TileList
from serialization.a_optional_json_serializable import AOptionalJsonSerializable


@dataclass
class Blueprint(AOptionalJsonSerializable):
    item: str = None
    label: str = None
    label_color: dict = None
    entities: EntityList = field(default_factory=EntityList)
    tiles: TileList = None
    icons: IconList = None
    schedules: list = None
    version: int = None

    def to_json(self):
        return {"blueprint": super().to_json()}

    @classmethod
    def from_json(cls, json_object: dict):
        return super().from_json(json_object["blueprint"])


