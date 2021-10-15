from enum import Enum
from typing import Union

from factorio.types.named_item import NamedItem


class EntitySpecialtyEnum(Enum):

    _value_: Union[NamedItem, str]

    def get_specialized(self):
        if hasattr(self.value, "item"):
            return self.value.item
        else:
            return self.value

    @classmethod
    def has_name(cls, name):
        return any(name == key for key, _ in cls._value2member_map_.items())


if __name__ == '__main__':
    class Tester(EntitySpecialtyEnum):
        S1 = NamedItem("item", 1000)

    print(Tester.has_name("boi"))
    print(Tester.has_name("item"))
    print(Tester.S1.get_specialized())
    print(Tester("item").get_specialized())
    pass
