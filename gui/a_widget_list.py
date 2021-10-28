import tkinter as tk
from abc import abstractmethod
from tkinter import Frame


class AWidgetList(Frame):

    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self._list_item_wrappers = []

    def create_empty_widget(self, widget_creator):
        wrapper = self.item_wrapper(self, widget_creator)
        self._list_item_wrappers.append(wrapper)

        wrapper.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        return wrapper

    def reset(self):
        for list_item in self._list_item_wrappers:
            list_item.destroy()
        self._list_item_wrappers = []

    def get_widget_at(self, index):
        return self._list_item_wrappers[index].item

    @property
    def item_amount(self):
        return len(self._list_item_wrappers)

    @property
    @abstractmethod
    def item_wrapper(self):
        pass

    @property
    def item_widgets_iter(self):
        return (w.item for w in self._list_item_wrappers)

    @property
    def item_widgets(self):
        return list(self.item_widgets_iter)
