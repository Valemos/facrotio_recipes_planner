from serialization.a_composite_json_serializable import ACompositeJsonSerializable


class Color(ACompositeJsonSerializable):
    r: float = None
    g: float = None
    b: float = None
    a: float = None