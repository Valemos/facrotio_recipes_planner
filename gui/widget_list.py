import tkinter as tk


class DeletableListItemWidget(tk.Frame):

    def __init__(self, root, item_creator):
        tk.Frame.__init__(self, root)
        self.item = item_creator(self)
        self.button_delete = tk.Button(self, text="X", command=self.destroy, takefocus=0)
        self.item.pack(side=tk.LEFT)
        self.button_delete.pack(side=tk.RIGHT)


class WidgetList(tk.Frame):
    def __init__(self, root, add_button_name, widget_creator):
        tk.Frame.__init__(self, root)
        self._list_item_wrappers = []
        self._widget_creator = widget_creator

        self.button_new_widget = tk.Button(self, text=add_button_name, command=self.create_empty_widget, takefocus=0)
        self.button_new_widget.pack(side=tk.TOP)

    @property
    def item_widgets(self):
        w: DeletableListItemWidget
        return [w.item for w in self._list_item_wrappers]

    @property
    def item_amount(self):
        return len(self._list_item_wrappers)

    def create_empty_widget(self):
        wrapper = DeletableListItemWidget(self, self._widget_creator)
        self._list_item_wrappers.append(wrapper)

        wrapper.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        self.button_new_widget.lift()
        return wrapper.item

    def reset(self):
        for list_item in self._list_item_wrappers:
            list_item.destroy()
        self._list_item_wrappers = []

    def get_widget_at(self, index):
        return self._list_item_wrappers[index].item
