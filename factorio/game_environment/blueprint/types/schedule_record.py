from dataclasses import dataclass

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable
from json_automatic.a_container_json_serializable import AContainerJsonSerializable

from factorio.game_environment.blueprint.types.wait_condition import WaitConditionList


@dataclass
class ScheduleRecord(ACompositeJsonSerializable):
    station: str = None
    wait_conditions: WaitConditionList = None


class ScheduleRecordList(list, AContainerJsonSerializable):
    __element_type__ = ScheduleRecord
