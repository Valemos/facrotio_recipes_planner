from enum import Enum

from serialization.i_json_serializable import IJsonSerializable


class EnumJson(IJsonSerializable, Enum):

    def to_json(self):
        return self.name

    @classmethod
    def from_json(cls, json_object: str):
        return cls[json_object]
