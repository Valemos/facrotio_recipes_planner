from abc import ABCMeta, abstractmethod


class AJsonSavable(metaclass=ABCMeta):
    @abstractmethod
    def to_json(self):
        pass

    @staticmethod
    @abstractmethod
    def from_json(json_object):
        pass
