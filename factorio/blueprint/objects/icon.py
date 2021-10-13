from dataclasses import field

from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


class SignalId(ACompositeJsonSerializable):
    name: str = ""
    type: str = ""


class Icon(ACompositeJsonSerializable):
    index: int = ""
    signal: SignalId = field(default_factory=SignalId)


class IconList(list, AContainerJsonSerializable):
    __element_type__ = Icon
