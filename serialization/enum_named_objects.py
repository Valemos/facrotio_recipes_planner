from copy import deepcopy
from enum import Enum
from typing import Union

from factorio.crafting_tree_builder.internal_types.named_item import NamedObject


class EnumNamedObjects(Enum):

    _value_: Union[NamedObject, str]

    def get_object(self):
        if hasattr(self.value, "item"):
            return deepcopy(self.value.item)
        else:
            return self.value

    @classmethod
    def has_name(cls, name):
        return any(name == key for key, _ in cls._value2member_map_.items())


if __name__ == '__main__':
    class Tester(EnumNamedObjects):
        S1 = NamedObject("item", 1000)

    print(Tester.has_name("boi"))
    print(Tester.has_name("item"))
    print(Tester.S1.get_object())
    print(Tester("item").get_object())
    pass
