from dataclasses import dataclass

from factorio.crafting_tree_builder.placeable_types.a_sized_grid_object import ASizedGridObject
from factorio.crafting_tree_builder.placeable_types.assembling_machine_unit import AssemblingMachineUnit
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
from factorio.recipe_graph.production_node import ProductionNode
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

    def to_game_object(self, game_environment: GameEnvironment) -> ASizedGridObject:
        try:
            obj = game_environment.get_placeable_stats(self.name).to_game_object()
        except ValueError:
            obj = ManualStatsMapping(self.name).get_object()

        if isinstance(obj, ASizedGridObject):
            obj.set_placement(self.direction, self.position)

        if isinstance(obj, AssemblingMachineUnit):
            if self.recipe is not None:
                recipe = game_environment.recipe_collection.get_recipe(self.recipe)
            else:
                recipe = game_environment.recipe_collection.EMPTY_RECIPE

            obj = ProductionNode(obj, recipe)

        if hasattr(obj, "loader_type"):
            obj.loader_type = self.type

        return obj


class BlueprintObjectList(list, AContainerJsonSerializable):
    __element_type__ = BlueprintObject
