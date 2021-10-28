import tkinter as tk


class DeletableListItemWidget(tk.Frame):

    def __init__(self, root, item_creator):
        tk.Frame.__init__(self, root)
        self.item = item_creator(self)
        self.button_delete = tk.Button(self, text="X", command=self.destroy, takefocus=0)
        self.item.pack(side=tk.LEFT)
        self.button_delete.pack(side=tk.RIGHT)