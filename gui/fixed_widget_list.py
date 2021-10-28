from gui.list_item_widget import ListItemWidget
from gui.a_widget_list import AWidgetList


class FixedWidgetList(AWidgetList):

    def __init__(self, root):
        super().__init__(root)

    @property
    def item_wrapper(self):
        return ListItemWidget

    def set_objects(self, collection, widget_creator):
        for obj in collection:
            widget = self.create_empty_widget(widget_creator)
            widget.name = str(obj)
            widget.item = obj
