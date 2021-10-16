from enum import Enum

from serialization.i_json_serializable import IJsonSerializable


class EnumByNameJson(IJsonSerializable, Enum):

    def to_json(self):
        return self.name

    @classmethod
    def from_json(cls, json_object: str):
        return cls[json_object]


class EnumByValueJson(IJsonSerializable, Enum):

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json_object):
        return cls(json_object)
