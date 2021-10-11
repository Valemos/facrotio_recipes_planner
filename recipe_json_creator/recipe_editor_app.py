import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from factorio.recipe_util.recipe_json_reading import read_default
from factorio.types.recipes_collection import RecipesCollection
from gui.entry_validator_with_label import EntryExistingPath
from gui.left_right_buttons import LeftRightButtons
from recipe_json_creator.a_recipe_json_saver import ARecipeJsonSaver
from recipe_json_creator.cyclic_iterator import CyclicIterator
from recipe_json_creator.recipe_form_widget import RecipeFormWidget
from recipe_json_creator.recipe_resolver_app import RecipeResolverApp


class RecipeEditorApp(tk.Frame, ARecipeJsonSaver):

    default_path = Path("./recipes/recipes.json")

    @classmethod
    def run(cls):
        root = tk.Tk()
        app = cls(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.parent = root
        self.winfo_toplevel().title("Recipe Builder")
        root.configure(padx=10, pady=10)

        self.collection = RecipesCollection()
        self.collection_iter = CyclicIterator(self.collection.recipes)

        self.entry_path = EntryExistingPath(root, "Path:", 20, self.default_path)
        self.entry_path.set(self.default_path)
        self.button_read_file = tk.Button(root, text="Read file", command=self.read_collection_json)

        self.recipe_form = RecipeFormWidget(root)
        self.recipe_form.reset()

        self.frame_edit = tk.Frame(root)
        self.button_save_recipe = tk.Button(self.frame_edit, text="Save recipe", command=self.save_recipe, takefocus=0)
        self.button_reset = tk.Button(self.frame_edit, text="Reset", command=self.recipe_form.reset, takefocus=0)
        self.button_delete = tk.Button(self.frame_edit, text="Delete", command=self.remove_current_recipe)
        self.button_save_recipe.pack(side=tk.LEFT, anchor=tk.E)
        self.button_reset.pack(side=tk.LEFT, anchor=tk.CENTER)
        self.button_delete.pack(side=tk.LEFT, anchor=tk.W)

        self.button_resolve = tk.Button(root, text="Resolve unknown", command=self.resolve_dependencies, takefocus=0)
        self.buttons_show = LeftRightButtons(root, 30, self.show_prev, self.show_next)
        self.button_show_current = tk.Button(root, text="Show current", command=self.update_recipe_entries)

        # pack
        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_read_file.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        self.recipe_form.pack(side=tk.TOP, anchor=tk.CENTER)
        self.frame_edit.pack(side=tk.TOP, anchor=tk.CENTER)
        self.buttons_show.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        self.button_show_current.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        self.button_resolve.pack(side=tk.TOP, anchor=tk.CENTER)

        self.read_collection_json()

    @property
    def recipe_file_path(self) -> Path:
        return self.entry_path.get()

    def create_resolver_for_material(self, material_name):
        toplevel = tk.Toplevel(self)
        toplevel.geometry(f"+{self.parent.winfo_x()}+{self.parent.winfo_y()}")
        builder = RecipeResolverApp(toplevel, self.recipe_file_path)
        builder.recipe_form.set_basic_material(material_name)
        return builder

    def save_recipe(self):
        try:
            recipes = self.read_recipes_from_json()

            recipe = self.recipe_form.get_recipe_name()
            self.remove_recipe_if_exists(recipe)

            self.recipe_form.add_item_to_collection(recipes)
            self.save_recipes_to_json(recipes)
            self.recipe_form.reset()

        except ValueError as err:
            messagebox.showerror("Invalid recipe", str(err))

    def resolve_dependencies(self):
        unresolved_names = set()
        recipes: RecipesCollection = read_default(self.entry_path.get())
        for recipe in recipes.recipes:
            for ingredient in recipe.get_required():
                if not recipes.is_material_known(ingredient):
                    unresolved_names.add(ingredient.name)

        if len(unresolved_names) == 0:
            messagebox.showinfo("Info", "no ingredient recipes need to be provided")
            return

        names_str = "\n".join((f"{i}. {el}" for i, el in enumerate(unresolved_names, start=1)))
        if not messagebox.askokcancel("Resolve names", f"following names will be resolved:\n{names_str}"):
            return

        for name in unresolved_names:

            resolver = self.create_resolver_for_material(name)
            resolver.wait_window()

            if resolver.cancelled: break

    def show_prev(self):
        self.collection_iter.prev()
        self.update_recipe_entries()

    def show_next(self):
        self.collection_iter.next()
        self.update_recipe_entries()

    def update_recipe_entries(self):
        recipe = self.collection_iter.get_or_none()
        if recipe is not None:
            self.recipe_form.set_recipe(recipe)

    def read_collection_json(self):
        self.collection = self.read_recipes_from_json()
        self.collection_iter = CyclicIterator(self.collection.recipes)
        self.update_recipe_entries()

    def remove_recipe_if_exists(self, recipe_name):
        if recipe_name not in (r.name for r in self.collection.recipes): return

        self.collection.remove_recipe_by_name(recipe_name)
        self.collection_iter = CyclicIterator(self.collection.recipes)

    def remove_current_recipe(self):
        recipe = self.recipe_form.get_recipe()
        if messagebox.askyesno("Confirm delete", f'are you sure you want to delete recipe "{recipe.name}"'):
            self.remove_recipe_if_exists(recipe)
            self.update_recipe_entries()


if __name__ == "__main__":
    RecipeEditorApp.run()
