import tkinter as tk

from gui.entry_validator_with_label import EntryIntegerWithLabel
from gui.entry_with_label import EntryWithLabel


class NameAmountWidget(tk.Frame):
    def __init__(self, root, **kw):
        super().__init__(root, **kw)

        self.entry_name = EntryWithLabel(self, "Name:", 10)
        self.entry_amount = EntryIntegerWithLabel(self, "N:", 5)
        self.entry_name.pack(side=tk.LEFT)
        self.entry_amount.pack(side=tk.LEFT)

    def get_name(self):
        return self.entry_name.get()

    def get_amount(self):
        return self.entry_amount.get()
