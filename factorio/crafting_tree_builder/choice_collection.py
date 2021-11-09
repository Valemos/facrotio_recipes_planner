from pathlib import Path
import json

from factorio.crafting_tree_builder.user_object_choice import UserObjectChoiceCollection, UserObjectChoice, \
    CollectionHash
from factorio.deterministic_hash import hash_det


class UserChoiceCollection:

    choice_save_file = Path("./object_choices.json")

    def __init__(self, dialog_handler=None, made_choices=None) -> None:
        self._dialog_handler = dialog_handler
        self._temporary_choices = made_choices if made_choices is not None else UserObjectChoiceCollection()
        self._permanent_choices = self._load_permanent_choices()

    def choose_from(self, collection):
        if len(collection) == 0:
            raise ValueError("collection has no elements to choose from")

        if len(collection) == 1:
            return collection[0]

        objects_id = CollectionHash.from_collection(collection)
        if objects_id in self._permanent_choices:
            choice = self._permanent_choices[objects_id]
            return self._get_object_by_id(choice.choice_id, collection)

        if objects_id in self._temporary_choices:
            choice = self._temporary_choices[objects_id]
            return self._get_object_by_id(choice.choice_id, collection)

        return self._choose_from_dialog(collection)

    def get_temporary(self):
        return self._temporary_choices

    @staticmethod
    def _get_object_by_id(object_id, collection):
        for obj in collection:
            if hash_det(obj) == object_id:
                return obj

        raise ValueError("cannot find")

    def _choose_from_dialog(self, collection):
        if self._dialog_handler is None:
            return collection[0]

        chosen_obj, is_permanent = self._dialog_handler.choose(collection)
        choice = UserObjectChoice.from_collection(collection, chosen_obj)
        if is_permanent:
            self._permanent_choices.append(choice)
            self._save_permanent_choices()
        else:
            self._temporary_choices.append(choice)

        return chosen_obj

    @staticmethod
    def _save_dict(dct: dict, save_file):
        with save_file.open("w") as fout:
            json.dump(dct, fout)

    def _save_permanent_choices(self):
        with self.choice_save_file.open("w") as fout:
            json.dump(self._permanent_choices.to_json(), fout)

    def _load_permanent_choices(self):
        try:
            with self.choice_save_file.open("r") as fin:
                return UserObjectChoiceCollection.from_json(json.load(fin))
        except Exception as exc:
            return UserObjectChoiceCollection()
