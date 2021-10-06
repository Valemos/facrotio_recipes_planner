import tkinter as tk


class EntryWithLabel(tk.Frame):

    def __init__(self, root, label, width):
        tk.Frame.__init__(self, root)

        label_obj = tk.Label(self, text=label)
        self._str_variable = tk.StringVar(self)

        self.entry = tk.Entry(self, textvariable=self._str_variable, width=width)
        label_obj.pack(side=tk.LEFT)
        self.entry.pack(side=tk.RIGHT)

    def get(self):
        return self._str_variable.get()

    def set(self, new_content):
        self._str_variable.set(new_content)
