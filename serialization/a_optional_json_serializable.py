from serialization.i_json_serializable import IJsonSerializable
from serialization.metaclasses import CompositeJsonScheme


class AOptionalJsonSerializable(IJsonSerializable, metaclass=CompositeJsonScheme):
    """if field is optional to serialize, it must be set by default to None"""

    def to_json(self):
        result = {}
        for attr in self.__class__.__serialized__:
            value = getattr(self, attr)
            if value is None:
                continue

            result[attr] = self._try_serialize(value, attr)
        return result

    @classmethod
    def from_json(cls, json_object: dict):
        obj = cls()
        for attr in cls.__serialized__:
            if attr not in json_object: continue
            json_child = json_object[attr]
            setattr(obj, attr, cls.deserialize(attr, json_child))
        return obj

    def _try_serialize(self, value, attribute_name):
        if attribute_name in self.__serializable_children__:
            return value.to_json()
        elif IJsonSerializable.is_basic_type(type(value)):
            return value
        else:
            raise ValueError(f'cannot serialize "{attribute_name}"')

    @classmethod
    def deserialize(cls, attribute_name, json_child):
        if attribute_name in cls.__serializable_children__:
            return cls.__serializable_children__[attribute_name].from_json(json_child)
        else:
            return json_child
