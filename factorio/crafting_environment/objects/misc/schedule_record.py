from factorio.crafting_environment.objects.misc.wait_condition import WaitConditionList
from serialization.a_composite_json_serializable import ACompositeJsonSerializable
from serialization.a_container_json_serializable import AContainerJsonSerializable


class ScheduleRecord(ACompositeJsonSerializable):
    station: str = None
    wait_conditions: WaitConditionList = None


class ScheduleRecordList(list, AContainerJsonSerializable):
    __element_type__ = ScheduleRecord
