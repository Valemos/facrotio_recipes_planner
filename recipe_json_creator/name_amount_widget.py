import tkinter as tk

from gui.entry_validator_with_label import EntryIntegerWithLabel
from gui.entry_with_label import EntryWithLabel


class NameAmountWidget(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, **kw)

        self.entry_name = EntryWithLabel(self, "Name:", 10)
        self.entry_amount = EntryIntegerWithLabel(self, "N:", 5, fallback_value=1)
        self.entry_name.pack(side=tk.LEFT)
        self.entry_amount.pack(side=tk.LEFT)

    def get_name(self) -> str:
        return self.entry_name.get()

    def set_name(self, new_name):
        return self.entry_name.set(new_name)

    def get_amount(self) -> int:
        return self.entry_amount.get()

    def set_amount(self, amount):
        return self.entry_amount.set(amount)

    def is_empty(self):
        return self.get_name() == ""
