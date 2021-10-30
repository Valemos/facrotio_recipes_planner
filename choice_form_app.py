import tkinter as tk

from tkinter_extension.menu import MenuObjectSelectorWidget
from tkinter_extension.tk_context import TkContext


class ChoiceFormApp(tk.Frame):

    def __init__(self, root, **kw) -> None:
        tk.Frame.__init__(self, root, **kw)
        self.parent = root
        self.winfo_toplevel().title("Recipe Builder")
        root.configure(padx=10, pady=10)

        self.submitted = False

        self.var_is_permanent = tk.IntVar()
        self.checkbutton_permanent = tk.Checkbutton(root, text="Permanent choice", variable=self.var_is_permanent)
        self.widget_objects = MenuObjectSelectorWidget(root, 20)
        self.button_submit = tk.Button(root, text="Submit", command=self._handle_submit)
        self.button_cancel = tk.Button(root, text="Cancel", command=self._handle_cancel)

        self.checkbutton_permanent.pack(side=tk.TOP, pady=5)
        self.widget_objects.pack(side=tk.TOP, pady=5)
        self.button_submit.pack(side=tk.TOP, pady=5)

    @classmethod
    def choose(cls, collection, default_index=-1):
        with TkContext() as app:
            return ChoiceFormApp(app).choose_from_collection(collection, default_index)

    def choose_from_collection(self, collection, default_index):
        self.widget_objects.set_objects(collection)
        self.widget_objects.set(collection[default_index])

        self.wait_window()

        if self.submitted:
            return self.widget_objects.get(), self.is_permanent()
        else:
            return self.widget_objects.get(), False

    def is_permanent(self):
        return self.var_is_permanent.get() == 1

    def _handle_submit(self):
        self.submitted = True
        self.destroy()

    def _handle_cancel(self):
        self.submitted = False
        self.destroy()


if __name__ == '__main__':
    objects = ChoiceFormApp.choose([1, 2, 3])
    pass
