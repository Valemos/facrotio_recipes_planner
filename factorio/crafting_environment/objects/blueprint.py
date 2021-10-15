from dataclasses import dataclass, field

from .craft_stations import try_or_ignore_specialize_entity
from .entity import EntityList
from factorio.crafting_environment.objects.misc.icon import IconList
from factorio.crafting_environment.objects.misc.tile import TileList
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

    def specialize_entities(self):
        for i, entity in enumerate(self.entities):
            self.entities[i] = try_or_ignore_specialize_entity(entity)

    def to_json(self):
        return {"crafting_environment": super().to_json()}

    @classmethod
    def from_json(cls, json_object: dict):
        return super().from_json(json_object["crafting_environment"])


