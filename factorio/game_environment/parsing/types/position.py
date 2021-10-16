from dataclasses import dataclass

from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class Position(ACompositeJsonSerializable):
    x: float = 0
    y: float = 0
