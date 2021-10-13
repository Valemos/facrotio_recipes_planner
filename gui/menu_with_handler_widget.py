import tkinter as tk


class MenuWithHandlerWidget(tk.OptionMenu):

    default_choice = "-"

    def __init__(self, root, width, choice_list=None, handler=None):
        self.variable_menu = tk.StringVar(root)
        tk.OptionMenu.__init__(self, root, self.variable_menu, None)
        self.configure(width=width)

        self.choice_handler = handler
        if handler is not None and not callable(handler):
            raise ValueError("choice function handler must be a callable object")

        self.choice_list = []
        self.update_choices(choice_list)

    def update_choices(self, new_choices: list[str]):
        """
        Values in dict_manager will be passed to handler function
        """

        self['menu'].delete(0, 'end')  # delete all elements from menu

        if new_choices is None:
            self.variable_menu.set(self.default_choice)
            return

        for name in new_choices:
            self['menu'].add_command(
                label=name,
                command=lambda n=name: self.choose_name(n))

        self.choice_list = new_choices

    def set_string(self, value: str):
        self.variable_menu.set(value if value is not None and value != "" else self.default_choice)

    def get_string(self):
        return self.variable_menu.get()

    def choose_name(self, name: str):
        self.set_string(name)
        if self.choice_handler is not None:
            self.choice_handler(name)
