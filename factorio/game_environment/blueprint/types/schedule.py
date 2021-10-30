from dataclasses import dataclass

from json_automatic.a_composite_json_serializable import ACompositeJsonSerializable
from json_automatic.a_container_json_serializable import AContainerJsonSerializable

from factorio.game_environment.blueprint.types.schedule_record import ScheduleRecordList


@dataclass
class Schedule(ACompositeJsonSerializable):
    schedule: ScheduleRecordList = None
    locomotives: list = None


class ScheduleList(list, AContainerJsonSerializable):
    __element_type__ = Schedule
