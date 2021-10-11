import tkinter as tk


class MenuWithHandler(tk.OptionMenu):

    default_choice = "-"

    def __init__(self, root, width, choice_list=None, handler=None):
        self.variable_menu = tk.StringVar(root)
        tk.OptionMenu.__init__(self, root, self.variable_menu, None)
        self.configure(width=width)

        if handler is None:
            self.choice_handler = self.handle_option_changed
        elif callable(handler):
            self.choice_handler = handler
        else:
            raise ValueError("menu must have choice function handler")

        self.choice_list = []
        self.update_choices(choice_list)

    def handle_option_changed(self, choice_index):
        if 0 <= choice_index < len(self.choice_list):
            self.set(self.choice_list[choice_index])
        else:
            self.set(choice_index)

    def update_choices(self, new_choices: list):
        """
        Values in dict_manager will be passed to handler function
        """

        self['menu'].delete(0, 'end')  # delete all elements from menu

        if new_choices is None:
            self.variable_menu.set(self.default_choice)
            return

        for index, name in enumerate(new_choices):
            self['menu'].add_command(
                label=name,
                command=lambda i=index: self.choice_handler(i))

        self.choice_list = new_choices

    def set(self, value):
        self.variable_menu.set(value if value is not None and value != "" else self.default_choice)

    def get(self):
        return self.variable_menu.get()
