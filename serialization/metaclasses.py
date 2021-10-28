import inspect
from typing import Any, Type, Optional

from serialization.i_json_serializable import IJsonSerializable


class SingleTypeScheme(type):
    """holds one type for all elements in container"""

    __element_type__: Type[IJsonSerializable]
    __scheme_initialized = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        obj = type.__call__(cls, *args, **kwds)

        if not cls._is_scheme_initialized():
            cls._initialize_scheme()

        cls._validate_object(obj)

        return obj

    def _is_scheme_initialized(cls):
        if cls.__qualname__ not in cls.__scheme_initialized:
            return False
        else:
            return cls.__scheme_initialized[cls.__qualname__]

    def _initialize_scheme(cls):
        if not hasattr(cls, "__element_type__"):
            raise ValueError('"__element_type__" was not defined')

        if IJsonSerializable.is_serializable_type(cls.__element_type__):
            cls.__scheme_initialized[cls.__qualname__] = True
        else:
            raise ValueError(f'cannot serialize "{repr(cls.__element_type__)}"')

    def _validate_object(cls, obj):
        for elem in obj:
            if not isinstance(elem, cls.__element_type__):
                raise ValueError(f'incorrect type of elements, must be "{repr(cls.__element_type__)}"')


class CompositeJsonScheme(type):
    __serialized__: tuple
    __ignored__: tuple
    __serializable_children__: dict

    def __init__(cls, name, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "__ignored__"):
            cls.__ignored__ = tuple()

        cls._initialize_scheme()

    def _initialize_scheme(cls):
        cls.__serialized__ = tuple(cls.__annotations__.keys())
        cls.__serializable_children__ = {}
        for attr in cls.__serialized__:
            if attr in cls.__ignored__: continue
            attr_type = cls._get_annotation_type(attr)

            if issubclass(attr_type, IJsonSerializable):
                cls.__serializable_children__[attr] = attr_type

    @staticmethod
    def _get_fields_iter(obj):
        for member_name, _ in inspect.getmembers(obj, lambda x: not (inspect.isroutine(x))):
            if not member_name.startswith("__") and member_name not in obj.__class__.__ignored__:
                yield member_name

    def _get_annotation_type(cls, attribute) -> Optional[Type]:
        if attribute in cls.__annotations__:
            return cls.__annotations__[attribute]
        return None
