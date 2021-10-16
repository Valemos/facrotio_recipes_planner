from dataclasses import field

from factorio.crafting_environment.objects.misc.item_filter import ItemFilterList


class Inventory:
    filters: ItemFilterList = field(default_factory=ItemFilterList)
    bar: int = 0