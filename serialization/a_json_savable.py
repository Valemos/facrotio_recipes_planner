from dataclasses import dataclass, is_dataclass, fields, field
import inspect


class JsonSchemeCreator(type):

    __serialized__: tuple
    __ignored_fields__: tuple
    __serializable_children__: dict

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "__ignored_fields__"):
            cls.__ignored_fields__ = tuple()

        obj = type.__call__(cls, *args, **kwargs)

        cls.__serialized__ = tuple(cls._get_fields_iter(obj))
        cls.__serializable_children__ = cls._get_serializable_dict(obj)
        return obj

    @staticmethod
    def _get_fields_iter(obj):
        for member_name, _ in inspect.getmembers(obj, lambda x: not (inspect.isroutine(x))):
            if not member_name.startswith("__") and member_name not in obj.__class__.__ignored_fields__:
                yield member_name

    @staticmethod
    def _get_serializable_dict(obj):
        obj: AJsonSerializable
        scheme = {}
        for var in obj.__class__.__serialized__:
            if isinstance(getattr(obj, var), AJsonSerializable):
                scheme[var] = getattr(obj, var).__class__
        return scheme


class AJsonSerializable(metaclass=JsonSchemeCreator):

    def to_json(self):
        result = {}
        for var in self.__class__.__serialized__:
            if var in self.__serializable_children__:
                result[var] = getattr(self, var).to_json()
            else:
                result[var] = getattr(self, var)
        return result

    @classmethod
    def from_json(cls, json_object: dict):
        obj: AJsonSerializable = cls()
        for attr in cls.__serialized__:
            json_child = json_object[attr]
            if attr in cls.__serializable_children__:
                setattr(obj, attr, cls.__serializable_children__[attr].from_json(json_child))
            else:
                setattr(obj, attr, json_child)
        return obj
