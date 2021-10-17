from dataclasses import field, dataclass

from factorio.game_environment.blueprint.types.item_filter import ItemFilterList


@dataclass
class Inventory:
    filters: ItemFilterList = field(default_factory=ItemFilterList)
    bar: int = 0
