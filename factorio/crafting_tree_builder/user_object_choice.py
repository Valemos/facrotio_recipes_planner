from dataclasses import dataclass

from json_annotated.a_composite_json_serializable import ACompositeJsonSerializable
from json_annotated.a_container_json_serializable import AContainerJsonSerializable

from factorio.deterministic_hash import hash_det


@dataclass
class CollectionHash(ACompositeJsonSerializable):

    hash: int = None

    def __hash__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash

    @classmethod
    def from_collection(cls, collection):
        return cls(hash_det(tuple(collection)))


@dataclass
class UserObjectChoice(ACompositeJsonSerializable):
    collection_id: CollectionHash = None
    choice_id: int = None

    @staticmethod
    def from_collection(collection, choice):
        return UserObjectChoice(
            CollectionHash.from_collection(collection),
            hash_det(choice),)


class UserObjectChoiceCollection(AContainerJsonSerializable):
    __element_type__ = UserObjectChoice

    def __init__(self) -> None:
        super().__init__()
        self._collection_choices = {}

    def __iter__(self):
        return iter(self._collection_choices.values())

    def __getitem__(self, item):
        if not isinstance(item, CollectionHash):
            raise ValueError("not a CollectionHash")
        return self._collection_choices[item]

    def __contains__(self, item):
        if isinstance(item, CollectionHash):
            return item in self._collection_choices
        elif isinstance(item, list):
            return CollectionHash.from_collection(item) in self._collection_choices

    def append(self, element):
        if isinstance(element, UserObjectChoice):
            self._collection_choices[element.collection_id] = element
