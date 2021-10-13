from serialization.a_composite_json_serializable import ACompositeJsonSerializable


class LogisticFilter(ACompositeJsonSerializable):
    name: str = None
    index: int = None
    count: int = None
