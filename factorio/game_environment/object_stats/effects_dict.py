from dataclasses import dataclass

from serialization.a_optional_json_serializable import AOptionalJsonSerializable


@dataclass
class EffectsDict(AOptionalJsonSerializable):
    consumption: bool = False
    speed: bool = False
    productivity: bool = False
    pollution: bool = False
