import inspect
from typing import Any, Type, Optional

from serialization.i_json_serializable import IJsonSerializable


class SingleTypeScheme(type):
    """holds one type for all elements in container"""

    __element_type__: Optional[Type[IJsonSerializable]]
    __scheme_initialized = {}

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        cls._initialize_scheme()

    def __call__(cls, *args, **kwds) -> Any:
        obj = type.__call__(cls, *args, **kwds)
        cls._validate_object(obj)
        return obj

    def _is_scheme_initialized(cls):
        if cls.__qualname__ not in cls.__scheme_initialized:
            return False
        else:
            return cls.__scheme_initialized[cls.__qualname__]

    def _initialize_scheme(cls):
        if hasattr(cls, "__element_type__"):
            if not IJsonSerializable.is_serializable_type(cls.__element_type__):
                raise ValueError(f'cannot serialize "{repr(cls.__element_type__)}"')
        else:
            cls.__element_type__ = None

    def _validate_object(cls, obj):
        if cls.__element_type__ is None:
            for elem in obj:
                cls._validate_element_serializable(elem)
        else:
            for elem in obj:
                cls._validate_element_type(elem)

    @staticmethod
    def _validate_element_serializable(elem):
        if not IJsonSerializable.is_serializable_type(type(elem)):
            raise ValueError(f'list type not serializable {type(elem)}')

    def _validate_element_type(cls, elem):
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
