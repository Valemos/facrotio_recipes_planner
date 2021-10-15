from enum import Enum
from typing import Type

from serialization.i_json_serializable import IJsonSerializable


class EnumMappingJson(dict, IJsonSerializable):
    __element_type__: Type[IJsonSerializable]

    def to_json(self):
        e: IJsonSerializable
        return {e.to_json(): value for e, value in self.items()}

    @classmethod
    def from_json(cls, json_object: dict):
        obj = cls()
        for key, value in json_object.items():
            obj[cls.__element_type__.from_json(key)] = value
        return obj
