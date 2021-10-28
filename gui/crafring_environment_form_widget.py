import tkinter as tk
from pathlib import Path

from app_misc.a_recipe_json_editor import ARecipeJsonEditor
from factorio.virtual_crafting_environment import VirtualCraftingEnvironment
from factorio.production_config_builder import VirtualProductionConfigBuilder
from factorio.crafting_tree_builder.internal_types.named_item import NamedObject
from gui.entry_validator_with_label import EntryExistingPath
from gui.menu_object_selector_widget import MenuObjectSelectorWidget
from gui.name_amount_widget import NameAmountWidget
from gui.modified_widget_list import DynamicWidgetList


class CraftingEnvironmentFormWidget(tk.Frame, ARecipeJsonEditor):

    default_recipes_path = Path("./recipes/recipes.json")

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.entry_path = EntryExistingPath(root, "Recipes path:", 20, self.default_recipes_path)
        self.entry_path.set(self.default_recipes_path)

        def create_material_name_entry(_root):
            return tk.Entry(_root, width=15)
        self.list_ready_materials = DynamicWidgetList(self, create_material_name_entry, "Add ready material")

        # todo add selection sequence for all crafting benches

        self.list_constrains = DynamicWidgetList(self, NameAmountWidget, "Add constrain")

        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_ready_materials.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_constrains.pack(side=tk.TOP, anchor=tk.CENTER)

    @property
    def recipe_file_path(self) -> Path:
        return self.entry_path.get()

    def reset(self):
        self.list_ready_materials.reset()
        self.list_constrains.reset()

    def get_environment(self):

        w: tk.Label
        final_materials = [w.getvar().get() for w in self.list_ready_materials.item_widgets_iter if
                           w.getvar().get() != ""]

        return VirtualCraftingEnvironment(
            final_materials,
            VirtualProductionConfigBuilder()
        )
