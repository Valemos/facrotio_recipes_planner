from dataclasses import dataclass

from factorio.game_environment.manual_stats_mapping import ManualStatsMapping
from factorio.game_environment.blueprint.types.color import Color
from factorio.game_environment.blueprint.types.direction_type import DirectionType
from factorio.game_environment.blueprint.types.filter_mode import FilterMode
from factorio.game_environment.blueprint.types.inventory import Inventory
from factorio.game_environment.blueprint.types.item_filter import ItemFilterList
from factorio.game_environment.blueprint.types.loader_type import LoaderType
from factorio.game_environment.blueprint.types.logistic_filter import LogisticFilter
from factorio.game_environment.blueprint.types.position import Position
from factorio.game_environment.blueprint.types.side_priority import SidePriority
from factorio.game_environment.game_environment import GameEnvironment
from serialization.a_container_json_serializable import AContainerJsonSerializable
from serialization.a_optional_json_serializable import AOptionalJsonSerializable


@dataclass(eq=True)
class BlueprintObject(AOptionalJsonSerializable):
    entity_number: int = None
    name: str = None
    position: Position = None
    direction: DirectionType = None
    orientation: float = None  # only for cargo wagon or locomotive, value 0 to 1
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

    def to_game_object(self, game_environment: GameEnvironment):
        try:
            obj = game_environment.get_placeable_stats(self.name).to_game_object()
        except ValueError:
            obj = ManualStatsMapping(self.name).get_object()

        if self.direction is not None:
            if not hasattr(obj, "direction"):
                raise ValueError(f'object {repr(obj)} has no attribute "direction"')
            obj.direction = self.direction

        return obj


class BlueprintObjectList(list, AContainerJsonSerializable):
    __element_type__ = BlueprintObject
