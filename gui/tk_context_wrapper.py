import gc
import tkinter as tk


class TkContextWrapper:

    def __init__(self, child_class):
        self._child_class = child_class
        self._tk_context: tk.Tk

    def __enter__(self):
        self._tk_context = tk.Tk()
        return self._child_class(self._tk_context)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._tk_context.destroy()
        self._tk_context = None
        gc.collect()
