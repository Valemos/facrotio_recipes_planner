from serialization.a_composite_json_serializable import ACompositeJsonSerializable


class Position(ACompositeJsonSerializable):
    x: float = 0
    y: float = 0
