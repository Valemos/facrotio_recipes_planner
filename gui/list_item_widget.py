import tkinter as tk


class ListItemWidget(tk.Frame):

    def __init__(self, root, item_creator):
        tk.Frame.__init__(self, root)
        self.item = item_creator(self)
        self.item.pack(side=tk.LEFT)
