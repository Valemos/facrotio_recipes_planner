from abc import ABCMeta, abstractmethod
from tkinter import StringVar

from gui.entry_with_label import EntryWithLabel


class EntryValidatorWithLabel(EntryWithLabel, metaclass=ABCMeta):

    def __init__(self, root, label, width):
        super().__init__(root, label, width)

    @property
    @abstractmethod
    def converter_function(self):
        """
        must return function to convert string to a specific value widget must hold
        if conversion fails function should raise ValueError
        """
        pass

    def is_valid(self, value):
        try:
            self.converter_function(value)
            return True
        except ValueError:
            return False

    def update_field(self):
        if self.str_variable.get() == "": return
        if not self.is_valid(self.str_variable.get()):
            self.str_variable.set("")

    def get(self):
        self.update_field()
        return self.converter_function(self.str_variable.get())

    def set(self, value):
        self.str_variable.set(str(value))


class EntryIntegerWithLabel(EntryValidatorWithLabel):
    @property
    def converter_function(self):
        return int

    def get(self) -> int:
        return super().get()

    def set(self, value: int):
        super().set(value)


class EntryFloatWithLabel(EntryValidatorWithLabel):
    @property
    def converter_function(self):
        return float

    def get(self) -> float:
        return super().get()

    def set(self, value: float):
        super().set(value)
