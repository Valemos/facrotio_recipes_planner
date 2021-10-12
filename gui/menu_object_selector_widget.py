from typing import Union

from gui.menu_with_handler_widget import MenuWithHandlerWidget


class MenuObjectSelectorWidget(MenuWithHandlerWidget):
    def __init__(self, root, width, choices: Union[list, dict[str, any]] = None):
        if isinstance(choices, list):
            self._choice_mapping = {str(c): c for c in choices}
        if isinstance(choices, dict):
            self._choice_mapping = choices

        super().__init__(root, width, list(self._choice_mapping.keys()), self._handle_object_selected)

        self._selected_object = None

    def set(self, new_choice):
        for choice_name, choice in self._choice_mapping.items():
            if choice == new_choice:
                self.choose_name(choice_name)
                return
        raise ValueError("unknown object selected")

    def get(self):
        return self._selected_object

    def _handle_object_selected(self, selected: str):
        self._selected_object = self._choice_mapping[selected]
