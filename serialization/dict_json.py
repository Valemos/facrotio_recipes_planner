from serialization.i_json_serializable import IJsonSerializable


class RawJson(IJsonSerializable):

    def __init__(self, value=None):
        self.value = value if value is not None else {}

    def __eq__(self, other):
        return self.value == other.value

    def to_json(self):
        return self.value

    @classmethod
    def from_json(cls, json_object: dict):
        return RawJson(json_object)
