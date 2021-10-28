import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from factorio.crafting_tree_builder.internal_types.recipes_collection import RecipesCollection
from gui.entry_validator_with_label import EntryExistingPath
from gui.left_right_buttons import LeftRightButtons
from app_misc.a_recipe_json_editor import ARecipeJsonEditor
from app_misc.cyclic_iterator import CyclicIterator
from gui.recipe_form_widget import RecipeFormWidget
from recipe_resolver_app import RecipeResolverApp


class RecipeEditorApp(tk.Frame, ARecipeJsonEditor):

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
        self.collection_iter = CyclicIterator([])

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

        self.button_resolve = tk.Button(root, text="Resolve unknown", command=self.handle_resolve_dependencies, takefocus=0)
        self.buttons_switch = LeftRightButtons(root, 30, self.handle_show_prev, self.handler_show_next)
        self.button_find_by_name = tk.Button(root, text="Find by name", command=self.handle_find_by_name)

        # pack
        self.entry_path.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_read_file.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        self.buttons_switch.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_find_by_name.pack(side=tk.TOP, anchor=tk.CENTER, pady=5)

        self.recipe_form.pack(side=tk.TOP, anchor=tk.CENTER)

        self.frame_edit.pack(side=tk.TOP, anchor=tk.CENTER)
        self.button_resolve.pack(side=tk.TOP, anchor=tk.CENTER)

        self.read_collection_json()

    @property
    def recipe_file_path(self) -> Path:
        return self.entry_path.get()

    def set_monitored_collection(self, recipes: RecipesCollection, show_position: int = None):
        """if show position is None, collection iterator will retain previous index"""

        self.collection = recipes
        self.update_collection_iterator(show_position)  # must be called to update self.collection_iter

    def create_resolver_for_material(self, material_name):
        toplevel = tk.Toplevel(self)
        toplevel.geometry(f"+{self.parent.winfo_x()}+{self.parent.winfo_y()}")
        builder = RecipeResolverApp(toplevel, self.recipe_file_path)
        builder.recipe_form.set_basic_material(material_name)
        return builder

    def handle_find_by_name(self):
        name = self.recipe_form.get_recipe_name()

        try:
            index = list(self.collection.recipe_names_iter).index(name)
        except ValueError:
            messagebox.showinfo("Not found", f'cannot find recipe "{name}"')
            return

        self.select_recipe_by_index(index)

    def save_recipe(self):
        try:
            recipes = self.read_recipes_from_json()

            recipe_name = self.recipe_form.get_or_deduce_recipe_name()
            if recipe_name in recipes.recipe_names_iter:
                recipes.update_recipe(self.recipe_form.get_recipe())
            else:
                self.recipe_form.add_item_to_collection(recipes)

            self.set_monitored_collection(recipes)
            self.save_recipes_to_json(recipes)

        except ValueError as err:
            messagebox.showerror("Invalid recipe", str(err))

    def handle_resolve_dependencies(self):
        recipes: RecipesCollection = read_default(self.entry_path.get())
        unresolved_names = recipes.get_unresolved_names()

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

    def handle_show_prev(self):
        self.collection_iter.prev()
        self.update_recipe_entries()

    def handler_show_next(self):
        self.collection_iter.next()
        self.update_recipe_entries()

    def update_recipe_entries(self):
        recipe = self.collection_iter.get_or_none()
        if recipe is not None:
            self.recipe_form.set_recipe(recipe)

    def read_collection_json(self):
        self.set_monitored_collection(self.read_recipes_from_json(), 0)

    def update_collection_iterator(self, position: int = None):
        """if position is None, collection iterator will retain previous index"""

        if position is None:
            position = self.collection_iter.index

        self.collection_iter = CyclicIterator(self.collection.recipes)
        self.select_recipe_by_index(position)

    def remove_current_recipe(self):
        recipe_name = self.recipe_form.get_or_deduce_recipe_name()
        if messagebox.askyesno("Confirm delete", f'are you sure you want to delete recipe "{recipe_name}"'):

            self.update_recipe_entries()

    def select_recipe_by_index(self, index):
        self.collection_iter.select(index)
        self.update_recipe_entries()


if __name__ == "__main__":
    RecipeEditorApp.run()
