import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from PIL import Image

import configurations.vanilla_devices as devices
from factorio.recipe_util.recipe_graph import build_recipe_graph
from factorio.types.crafting_environment import CraftingEnvironment
from factorio.types.material import Material
from factorio.types.named_item import NamedItem
from gui.entry_validator_with_label import EntryExistingPath
from gui.menu_object_selector_widget import MenuObjectSelectorWidget
from gui.name_amount_widget import NameAmountWidget
from gui.widget_list import WidgetList
from recipe_json_creator.a_recipe_json_saver import ARecipeJsonEditor


class RecipeTreeApp(tk.Frame, ARecipeJsonEditor):

    default_path = Path("./recipes/recipes.json")
    default_graph_image_path = Path("./graph/result.png")

    assembler_types = [NamedItem("regular", devices.assembling_machine_1),
                       NamedItem("fast", devices.assembling_machine_2),
                       NamedItem("advanced", devices.assembling_machine_3)]

    belt_types = [NamedItem("yellow", devices.transport_belt_1),
                  NamedItem("red", devices.transport_belt_2),
                  NamedItem("blue", devices.transport_belt_3),
                  NamedItem("inf", devices.transport_belt_inf)]

    furnace_types = [NamedItem("stone", devices.furnace_1),
                     NamedItem("steel", devices.furnace_2),
                     NamedItem("electric", devices.furnace_3)]

    @classmethod
    def run(cls):
        root = tk.Tk()
        app = cls(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.winfo_toplevel().title("Tree Builder")
        root.configure(padx=10, pady=10)

        self.entry_path = EntryExistingPath(root, "Path:", 20, self.default_path)
        self.entry_path.set(self.default_path)
        self.entry_target_recipe = NameAmountWidget(root)

        def create_material_name_entry(_entry_root):
            return tk.Entry(_entry_root, width=15)
        self.list_ready_materials = WidgetList(root, "Add ready material", create_material_name_entry)

        self.menu_assembler_type = MenuObjectSelectorWidget(root, 20, self.assembler_types)
        self.menu_furnace_type = MenuObjectSelectorWidget(root, 20, self.furnace_types)
        self.menu_belt_type = MenuObjectSelectorWidget(root, 20, self.belt_types)

        self.list_constrains = WidgetList(root, "Add constrain", NameAmountWidget)
        self.button_build_tree = tk.Button(root, text="Build tree", command=self.show_recipe_tree)

        # pack
        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        tk.Label(root, text="Target recipe").pack(side=tk.TOP, anchor=tk.CENTER)
        self.entry_target_recipe.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_assembler_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_belt_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.menu_furnace_type.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_ready_materials.pack(side=tk.TOP, anchor=tk.CENTER)
        self.list_constrains.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_build_tree.pack(side=tk.TOP, anchor=tk.CENTER)

        self.reset_form()

    @property
    def recipe_file_path(self) -> Path:
        return self.entry_path.get()

    def reset_form(self):
        self.menu_assembler_type.set(self.assembler_types[0])
        self.menu_furnace_type.set(self.furnace_types[0])
        self.menu_belt_type.set(self.belt_types[-1])
        self.list_ready_materials.reset()
        self.list_constrains.reset()

    def show_recipe_tree(self):
        recipes = self.read_recipes_from_json()
        desired_material = Material(self.entry_target_recipe.get_name(), self.entry_target_recipe.get_amount())
        if desired_material.name == "":
            messagebox.showerror("Invalid form", "empty target material provided")
            return

        w: tk.Label
        final_materials = [w.getvar().get() for w in self.list_ready_materials.item_widgets_iter if w.getvar().get() != ""]
        environment = CraftingEnvironment(
            final_materials=final_materials,
            assembler_type=self.menu_assembler_type.get().item,
            furnace_type=self.menu_furnace_type.get().item,
            transport_belt_type=self.menu_belt_type.get().item,
            recipes_collection=recipes
        )

        graph = build_recipe_graph(desired_material, environment)
        graph.render(self.default_graph_image_path.with_suffix(""), format="png")
        image: Image.Image = Image.open(self.default_graph_image_path)
        image.show()


if __name__ == '__main__':
    RecipeTreeApp.run()
