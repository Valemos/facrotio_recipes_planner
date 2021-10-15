from abc import abstractmethod
from typing import Optional

from serialization.a_optional_json_serializable import AOptionalJsonSerializable


class AStats(AOptionalJsonSerializable):

    @abstractmethod
    def to_object(self) -> Optional[object]:
        return None
