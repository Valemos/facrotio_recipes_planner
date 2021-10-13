import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from PIL import Image

from factorio.recipe_util.recipe_graph import build_recipe_graph
from factorio.types.material import Material
from gui.crafring_environment_form_widget import CraftingEnvironmentFormWidget
from gui.name_amount_widget import NameAmountWidget


class RecipeTreeApp(tk.Frame):

    default_graph_image_path = Path("./graph/result.png")

    @classmethod
    def run(cls):
        root = tk.Tk()
        app = cls(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.winfo_toplevel().title("Tree Builder")
        root.configure(padx=10, pady=10)

        self.entry_target_recipe = NameAmountWidget(root)
        self.form_environment = CraftingEnvironmentFormWidget(root)
        self.button_build_tree = tk.Button(root, text="Build tree", command=self.show_recipe_tree)

        # pack
        tk.Label(root, text="Target recipe").pack(side=tk.TOP, anchor=tk.CENTER)
        self.entry_target_recipe.pack(side=tk.TOP, anchor=tk.CENTER)
        self.form_environment.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_build_tree.pack(side=tk.TOP, anchor=tk.CENTER)

        self.form_environment.reset()

    def show_recipe_tree(self):
        desired_material = Material(self.entry_target_recipe.get_name(), self.entry_target_recipe.get_amount())
        if desired_material.name == "":
            messagebox.showerror("Invalid form", "empty target material provided")
            return

        environment = self.form_environment.get_environment()

        graph = build_recipe_graph(desired_material, environment)
        graph.render(self.default_graph_image_path.with_suffix(""), format="png")
        image: Image.Image = Image.open(self.default_graph_image_path)
        image.show()


if __name__ == '__main__':
    RecipeTreeApp.run()
