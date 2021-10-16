import tkinter as tk
from pathlib import Path

from app_misc.a_recipe_json_editor import ARecipeJsonEditor
from factorio.crafting_environment import CraftingEnvironment
from factorio.production_config_builder import ProductionConfigBuilder
from factorio.types.named_item import NamedItem
from gui.entry_validator_with_label import EntryExistingPath
from gui.menu_object_selector_widget import MenuObjectSelectorWidget
from gui.name_amount_widget import NameAmountWidget
from gui.widget_list import WidgetList


class CraftingEnvironmentFormWidget(tk.Frame, ARecipeJsonEditor):

    default_recipes_path = Path("./recipes/recipes.json")

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.entry_path = EntryExistingPath(root, "Recipes path:", 20, self.default_recipes_path)
        self.entry_path.set(self.default_recipes_path)

        def create_material_name_entry(_root):
            return tk.Entry(_root, width=15)
        self.list_ready_materials = WidgetList(self, "Add ready material", create_material_name_entry)

        # todo create popup window for each unresolved choice in ProductionConfigBuilder
        self.menu_assembler_type = MenuObjectSelectorWidget(self, 20, self.assembler_types)

        self.list_constrains = WidgetList(self, "Add constrain", NameAmountWidget)

        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_assembler_type.pack(side=tk.TOP, anchor=tk.CENTER)
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
            final_materials,
            ProductionConfigBuilder()
        )
