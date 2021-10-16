from dataclasses import field, dataclass

from factorio.crafting_tree_builder.objects import ItemFilterList


@dataclass
class Inventory:
    filters: ItemFilterList = field(default_factory=ItemFilterList)
    bar: int = 0
