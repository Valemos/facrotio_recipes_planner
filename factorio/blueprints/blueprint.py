from dataclasses import dataclass

from factorio.blueprints.entity_factorio import EntityFactorio
from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class Blueprint(ACompositeJsonSerializable):
    entities: list[EntityFactorio]

    def to_json(self):
        return {}

    @classmethod
    def from_json(cls, json_object: dict):
        return super().from_json(json_object)


