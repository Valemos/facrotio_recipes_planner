import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from recipe_json_creator.a_recipe_json_saver import ARecipeJsonEditor
from gui.recipe_form_widget import RecipeFormWidget


class RecipeResolverApp(tk.Frame, ARecipeJsonEditor):

    def __init__(self, root, save_path: Path, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.parent = root
        self.save_path = save_path
        self.cancelled = False

        self.winfo_toplevel().title("Resolver")
        root.configure(padx=10, pady=10)

        self.recipe_form = RecipeFormWidget(root)
        self.recipe_form.reset()

        self.button_save = tk.Button(root, text="Save", command=self.save_new_recipe)
        self.button_cancel = tk.Button(root, text="Cancel", command=self.handle_cancel)

        tk.Label(root, text=f"will be saved to {str(save_path)}").pack(side=tk.TOP, anchor=tk.CENTER)
        self.recipe_form.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_save.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_cancel.pack(side=tk.TOP, anchor=tk.CENTER)

    @property
    def recipe_file_path(self) -> Path:
        return self.save_path

    def save_new_recipe(self):
        recipes = self.read_recipes_from_json()

        try:
            self.recipe_form.add_item_to_collection(recipes)
        except ValueError as err:
            messagebox.showerror("Invalid recipe", str(err))
            self.parent.destroy()
            return

        self.save_recipes_to_json(recipes)
        self.parent.destroy()

    def handle_cancel(self):
        self.cancelled = True
        self.parent.destroy()
