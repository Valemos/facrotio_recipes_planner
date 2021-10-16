from dataclasses import dataclass

from factorio.game_environment.parsing.types.color import Color
from factorio.game_environment.parsing.types.filter_mode import FilterMode
from factorio.game_environment.parsing.types.inventory import Inventory
from factorio.game_environment.parsing.types.item_filter import ItemFilterList
from factorio.game_environment.parsing.types.loader_type import LoaderType
from factorio.game_environment.parsing.types.logistic_filter import LogisticFilter
from factorio.game_environment.parsing.types.position import Position
from factorio.game_environment.parsing.types.side_priority import SidePriority
from serialization.a_container_json_serializable import AContainerJsonSerializable
from serialization.a_optional_json_serializable import AOptionalJsonSerializable


@dataclass(eq=True)
class BlueprintObject(AOptionalJsonSerializable):
    entity_number: int = None
    name: str = None
    position: Position = None
    direction: int = None
    orientation: float = None
    connections: dict = None
    control_behaviour: dict = None
    items: dict = None
    recipe: str = None
    bar: int = None
    inventory: Inventory = None
    infinity_settings: dict = None
    type: LoaderType = None
    input_priority: SidePriority = None
    output_priority: SidePriority = None
    filter: str = None
    filters: ItemFilterList = None
    filter_mode: FilterMode = None
    override_stack_size: int = None
    drop_position: Position = None
    pickup_position: Position = None
    request_filters: LogisticFilter = None
    request_from_buffers: bool = None
    parameters: dict = None
    alert_parameters: dict = None
    auto_launch: bool = None
    variation: dict = None
    color: Color = None
    station: str = None


class BlueprintObjectList(list, AContainerJsonSerializable):
    __element_type__ = BlueprintObject
