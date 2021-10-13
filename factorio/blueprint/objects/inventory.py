from dataclasses import field

from factorio.blueprint.objects.item_filter import ItemFilterList


class Inventory:
    filters: ItemFilterList = field(default_factory=ItemFilterList)
    bar: int = 0