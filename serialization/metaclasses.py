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
            cls._initialize_scheme(obj)

        cls._validate_object(obj)

        return obj

    def _is_scheme_initialized(cls):
        if cls.__qualname__ not in cls.__scheme_initialized:
            return False
        else:
            return cls.__scheme_initialized[cls.__qualname__]

    def _initialize_scheme(cls, obj):
        if not hasattr(cls, "__element_type__"):
            raise ValueError('"__element_type__" was not defined')

        if not issubclass(cls.__element_type__, IJsonSerializable):
            raise ValueError(f'cannot serialize "{repr(cls.__element_type__)}"')

        cls.__scheme_initialized[cls.__qualname__] = True

    def _validate_object(cls, obj):
        for elem in obj:
            if not isinstance(elem, cls.__element_type__):
                raise ValueError(f'incorrect type of elements, must be "{repr(cls.__element_type__)}"')


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
            attr_type = cls._get_annotation_type(attr)
            if attr_type is None:
                attr_type = getattr(obj, attr).__class__

            if issubclass(attr_type, IJsonSerializable):
                cls.__serializable_children__[attr] = attr_type

        cls.__scheme_initialized[cls.__qualname__] = True

    @staticmethod
    def _get_fields_iter(obj):
        for member_name, _ in inspect.getmembers(obj, lambda x: not (inspect.isroutine(x))):
            if not member_name.startswith("__") and member_name not in obj.__class__.__ignored_fields__:
                yield member_name

    def _get_annotation_type(cls, attribute) -> Optional[Type]:
        # try to use annotations
        if attribute in cls.__annotations__:
            return cls.__annotations__[attribute]
        return None
