from dataclasses import dataclass

from factorio.game_environment.blueprint.types.schedule_record import ScheduleRecordList
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


@dataclass
class Schedule(ACompositeJsonSerializable):
    schedule: ScheduleRecordList = None
    locomotives: list = None


class ScheduleList(list, AContainerJsonSerializable):
    __element_type__ = Schedule
