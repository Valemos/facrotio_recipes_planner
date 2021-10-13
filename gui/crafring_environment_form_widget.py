import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from app_misc.a_recipe_json_editor import ARecipeJsonEditor
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.types.named_item import NamedItem
import configurations.vanilla_devices as devices
from gui.entry_validator_with_label import EntryExistingPath
from gui.menu_object_selector_widget import MenuObjectSelectorWidget
from gui.name_amount_widget import NameAmountWidget
from gui.widget_list import WidgetList


class CraftingEnvironmentFormWidget(tk.Frame, ARecipeJsonEditor):

    default_recipes_path = Path("./recipes/recipes.json")

    assembler_types = [NamedItem("basic", devices.assembling_machine_1),
                       NamedItem("blue", devices.assembling_machine_2),
                       NamedItem("green", devices.assembling_machine_3)]

    belt_types = [NamedItem("yellow", devices.transport_belt_1),
                  NamedItem("red", devices.transport_belt_2),
                  NamedItem("blue", devices.transport_belt_3),
                  NamedItem("belt inf", devices.transport_belt_inf)]

    furnace_types = [NamedItem("stone", devices.furnace_1),
                     NamedItem("steel", devices.furnace_2),
                     NamedItem("electric", devices.furnace_3)]

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.entry_path = EntryExistingPath(root, "Recipes path:", 20, self.default_recipes_path)
        self.entry_path.set(self.default_recipes_path)

        def create_material_name_entry(_root):
            return tk.Entry(_root, width=15)
        self.list_ready_materials = WidgetList(self, "Add ready material", create_material_name_entry)

        self.menu_assembler_type = MenuObjectSelectorWidget(self, 20, self.assembler_types)
        self.menu_furnace_type = MenuObjectSelectorWidget(self, 20, self.furnace_types)
        self.menu_belt_type = MenuObjectSelectorWidget(self, 20, self.belt_types)

        self.list_constrains = WidgetList(self, "Add constrain", NameAmountWidget)

        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_assembler_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_belt_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_furnace_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_ready_materials.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_constrains.pack(side=tk.TOP, anchor=tk.CENTER)

    @property
    def recipe_file_path(self) -> Path:
        return self.entry_path.get()

    def reset(self):
        self.menu_assembler_type.set(self.assembler_types[0])
        self.menu_furnace_type.set(self.furnace_types[0])
        self.menu_belt_type.set(self.belt_types[-1])
        self.list_ready_materials.reset()
        self.list_constrains.reset()

    def get_environment(self):

        w: tk.Label
        final_materials = [w.getvar().get() for w in self.list_ready_materials.item_widgets_iter if
                           w.getvar().get() != ""]

        return CraftingEnvironment(
            final_materials=final_materials,
            assembler_type=self.menu_assembler_type.get().item,
            furnace_type=self.menu_furnace_type.get().item,
            transport_belt_type=self.menu_belt_type.get().item,
            recipes_collection=self.read_recipes_from_json()
        )
