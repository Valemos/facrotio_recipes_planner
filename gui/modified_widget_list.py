import tkinter

from gui.a_widget_list import AWidgetList
from gui.deletable_list_item_widget import DeletableListItemWidget


class DynamicWidgetList(AWidgetList):

    def __init__(self, root, widget_creator, button_name):
        super().__init__(root)

        self.widget_creator = widget_creator
        self.button_new_widget = tkinter.Button(self, text=button_name, command=self.create_empty_widget, takefocus=0)
        self.button_new_widget.pack(side=tkinter.TOP)

    @property
    def item_wrapper(self):
        return DeletableListItemWidget

    def create_empty_widget(self, widget_creator):
        wrapper = super().create_empty_widget(widget_creator)
        self.button_new_widget.lift()
        return wrapper
