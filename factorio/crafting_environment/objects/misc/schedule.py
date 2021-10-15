from factorio.crafting_environment.objects.misc.schedule_record import ScheduleRecordList
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


class Schedule(ACompositeJsonSerializable):
    schedule: ScheduleRecordList = None
    locomotives: list = None


class ScheduleList(list, AContainerJsonSerializable):
    __element_type__ = Schedule
