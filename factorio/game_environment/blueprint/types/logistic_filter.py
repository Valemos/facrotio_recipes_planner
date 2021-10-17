from dataclasses import dataclass

from serialization.a_composite_json_serializable import ACompositeJsonSerializable


@dataclass
class LogisticFilter(ACompositeJsonSerializable):
    name: str = None
    index: int = None
    count: int = None
