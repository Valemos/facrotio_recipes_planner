from dataclasses import dataclass

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable
from json_automatic.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class WaitCondition(ACompositeJsonSerializable):
    type: str = None
    compare_type: str = None
    ticks: int = None
    condition: dict = None


class WaitConditionList(list, AContainerJsonSerializable):
    __element_type__ = WaitCondition

