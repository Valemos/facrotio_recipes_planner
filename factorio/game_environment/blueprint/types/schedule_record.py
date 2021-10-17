from dataclasses import dataclass

from factorio.game_environment.blueprint.types.wait_condition import WaitConditionList
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class ScheduleRecord(ACompositeJsonSerializable):
    station: str = None
    wait_conditions: WaitConditionList = None


class ScheduleRecordList(list, AContainerJsonSerializable):
    __element_type__ = ScheduleRecord
