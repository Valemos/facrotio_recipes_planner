from abc import abstractmethod


class IJsonSerializable:
    """Interface without serialization scheme to use as child custom object"""

    @staticmethod
    def is_basic_type(t):
        return t is str or \
               t is int or \
               t is float or \
               t is bool or \
               t is None

    @staticmethod
    def is_serializable_type(t):
        return IJsonSerializable.is_basic_type(t) or issubclass(t, IJsonSerializable)

    @abstractmethod
    def to_json(self):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, json_object: dict):
        pass
