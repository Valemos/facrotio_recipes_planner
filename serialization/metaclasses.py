import inspect
from abc import abstractmethod
from typing import Any, Type

from serialization.dict_json import RawJson
from serialization.i_json_serializable import IJsonSerializable


class SingleTypeScheme(type):
    """holds one type for all elements in container"""

    __element_type__: Type[IJsonSerializable]
    __scheme_initialized = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        obj = type.__call__(cls, *args, **kwds)

        if not cls._is_scheme_initialized():
            cls._initialize_scheme(obj)

        return obj

    def _is_scheme_initialized(cls):
        if cls.__qualname__ not in cls.__scheme_initialized:
            return False
        else:
            return cls.__scheme_initialized[cls.__qualname__]

    def _initialize_scheme(cls, obj):
        if not hasattr(cls, "__element_type__"):
            raise ValueError('"__element_type__" was not defined')
        elem_type = cls.__element_type__
        if not issubclass(cls.__element_type__, IJsonSerializable):
            raise ValueError(f'cannot serialize "{repr(cls.__element_type__)}"')
        for elem in obj:
            if not isinstance(elem, cls.__element_type__):
                raise ValueError(f'incorrect type of elements, must be "{repr(elem_type)}"')

        cls.__scheme_initialized[cls.__qualname__] = True


class CompositeJsonScheme(type):
    __serialized__: tuple
    __ignored_fields__: tuple
    __serializable_children__: dict

    __scheme_initialized = {}

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "__ignored_fields__"):
            cls.__ignored_fields__ = tuple()

        obj = type.__call__(cls, *args, **kwargs)

        if not cls._is_scheme_initialized():
            cls._initialize_scheme(obj)

        return obj

    def _is_scheme_initialized(cls):
        if cls.__qualname__ not in cls.__scheme_initialized:
            return False
        else:
            return cls.__scheme_initialized[cls.__qualname__]

    def _initialize_scheme(cls, obj):
        cls.__serialized__ = tuple(cls._get_fields_iter(obj))
        cls.__serializable_children__ = {}
        for attr in cls.__serialized__:
            attr_value = getattr(obj, attr)
            if isinstance(attr_value, IJsonSerializable):
                cls.__serializable_children__[attr] = attr_value.__class__

        cls.__scheme_initialized[cls.__qualname__] = True

    @staticmethod
    def _get_fields_iter(obj):
        for member_name, _ in inspect.getmembers(obj, lambda x: not (inspect.isroutine(x))):
            if not member_name.startswith("__") and member_name not in obj.__class__.__ignored_fields__:
                yield member_name
