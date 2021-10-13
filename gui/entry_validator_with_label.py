from abc import ABCMeta, abstractmethod
from pathlib import Path
from tkinter import StringVar

from gui.entry_with_label import EntryWithLabel


class EntryValidatorWithLabel(EntryWithLabel, metaclass=ABCMeta):

    def __init__(self, root, label, width, fallback_value):
        super().__init__(root, label, width)
        self._fallback_value = fallback_value

    @property
    @abstractmethod
    def convert_function(self):
        """
        must return function to convert string to a specific value widget must hold
        if conversion fails function should raise ValueError
        """
        pass

    def update_field(self):
        if super().get() == "": return
        try:
            self.convert_function(super().get())
        except ValueError:
            super().set(self._fallback_value)

    def get(self):
        self.update_field()
        try:
            return self.convert_function(super().get())
        except ValueError:
            return self._fallback_value

    def set(self, value):
        super().set(str(value))


class EntryIntegerWithLabel(EntryValidatorWithLabel):

    def __init__(self, root, label, width, fallback_value=0):
        super().__init__(root, label, width, fallback_value)

    @property
    def convert_function(self):
        return int

    def get(self) -> int:
        return super().get()

    def set(self, value: int):
        super().set(value)


class EntryFloatWithLabel(EntryValidatorWithLabel):
    def __init__(self, root, label, width):
        super().__init__(root, label, width, 0.0)

    @property
    def convert_function(self):
        return float

    def get(self) -> float:
        return super().get()

    def set(self, value: float):
        super().set(value)

    def set_raw(self, value):
        super().set(value)


class EntryExistingPath(EntryValidatorWithLabel):
    def __init__(self, root, label, width, default_path: Path):
        super().__init__(root, label, width, default_path)

    @property
    def convert_function(self):
        return Path

    def get(self) -> Path:
        try:
            path = self.convert_function(super().get())
            if path.is_dir(): raise ValueError

            if not path.exists():
                path.parent.mkdir(parents=True)
                path.touch()
            return path
        except Exception:
            return self._fallback_value

    def set(self, value):
        super().set(value)
