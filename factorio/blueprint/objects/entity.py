from dataclasses import dataclass

from factorio.blueprint.objects.SidePriority import SidePriority
from factorio.blueprint.objects.color import Color
from factorio.blueprint.objects.filter_mode import FilterMode
from factorio.blueprint.objects.inventory import Inventory
from factorio.blueprint.objects.item_filter import ItemFilterList
from factorio.blueprint.objects.loader_type import LoaderType
from factorio.blueprint.objects.logistic_filter import LogisticFilter
from factorio.blueprint.objects.position import Position
from serialization.a_container_json_serializable import AContainerJsonSerializable
from serialization.a_optional_json_serializable import AOptionalJsonSerializable


@dataclass(eq=True)
class Entity(AOptionalJsonSerializable):
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


class EntityList(list, AContainerJsonSerializable):
    __element_type__ = Entity
