import tkinter as tk


class WidgetList(tk.Frame):
    def __init__(self, root, add_button_name, widget_class, **child_widget_args):
        tk.Frame.__init__(self, root)
        self.widgets = []
        self.widget_class = widget_class
        self.widget_args = child_widget_args

        self.button_new_widget = tk.Button(self, text=add_button_name, command=self.create_empty_widget)
        self.button_new_widget.pack(side=tk.TOP)

    def create_empty_widget(self):
        new_widget = self.widget_class(self, **self.widget_args)
        new_widget.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        self.widgets.append(new_widget)
        self.button_new_widget.lift()

    def reset(self):
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []
