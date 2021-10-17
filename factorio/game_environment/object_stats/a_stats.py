from abc import abstractmethod

from serialization.a_optional_json_serializable import AOptionalJsonSerializable


class AStats(AOptionalJsonSerializable):

    @abstractmethod
    def to_game_object(self):
        return None
