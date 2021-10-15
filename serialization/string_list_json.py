from serialization.a_container_json_serializable import AContainerJsonSerializable


class StringListJson(list, AContainerJsonSerializable):
    __element_type__ = str
