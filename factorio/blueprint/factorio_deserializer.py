from enum import Enum
from pathlib import Path

from factorio.blueprint.objects.blueprint import Blueprint
from serialization.i_json_serializable import IJsonSerializable


class FactorioObjectTypes(Enum):
    blueprint = Blueprint


class FactorioDeserializer:

    object_stats_file = Path("recipes/stats.json")

    @staticmethod
    def from_json(json_object: dict):
        obj_type: IJsonSerializable = FactorioObjectTypes[json_object["item"]]
        return obj_type.from_json(json_object)
