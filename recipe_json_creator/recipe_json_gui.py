import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from factorio.recipe_util.recipe_json_reading import read_space_exploration
from factorio.types.recipe import CraftStationType
from factorio.types.recipes_collection import RecipesCollection
from gui.entry_validator_with_label import EntryFloatWithLabel, EntryIntegerWithLabel, EntryExistingPath
from gui.entry_with_label import EntryWithLabel
from gui.menu_with_handler import MenuWithHandler
from gui.widget_list import WidgetList
from recipe_json_creator.name_amount_widget import NameAmountWidget


class RecipeJsonBuilder(tk.Frame):
    default_path = Path("./recipes/recipes.json")
    recipe_types = [type.name for type in CraftStationType]

    @staticmethod
    def run():
        root = tk.Tk()
        app = RecipeJsonBuilder(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.parent = root
        self.winfo_toplevel().title("Recipe Builder")

        self.entry_path = EntryExistingPath(root, "Path: ", 15, self.default_path)
        self.entry_path.set(self.default_path)

        self.menu_recipe_type = MenuWithHandler(root, 15, self.recipe_types)
        self.menu_recipe_type.set(self.recipe_types[0])

        self.entry_craft_time = EntryFloatWithLabel(root, "Craft time: ", 10)
        self.widget_ingredients = WidgetList(root, "Add ingredient", NameAmountWidget)
        self.widget_products = WidgetList(root, "Add product", NameAmountWidget)
        self.entry_recipe_name = EntryWithLabel(root, "Recipe name: ", 15)

        self.reset_form()

        self.button_add_recipe = tk.Button(root, text="Append recipe", command=self.add_new_recipe)
        self.button_basic_material = tk.Button(root, text="Basic material", command=self.add_basic_material)
        self.button_reset = tk.Button(root, text="Reset", command=self.reset_form)
        self.button_resolve = tk.Button(root, text="Resolve", command=self.resolve_dependencies)

        # pack
        side_args = {"side": tk.TOP, "anchor": tk.E, "pady": 5, "padx": 10}
        center_args = {"side": tk.TOP, "anchor": tk.CENTER, "pady": 5, "padx": 10}

        self.entry_path.pack(**center_args)
        self.menu_recipe_type.pack(**center_args)
        self.entry_craft_time.pack(**side_args)
        tk.Label(root, text="Ingredients").pack(**center_args)
        self.widget_ingredients.pack(**center_args)
        tk.Label(root, text="Products").pack(**center_args)
        self.widget_products.pack(**center_args)
        self.entry_recipe_name.pack(**center_args)
        self.button_add_recipe.pack(**center_args)
        self.button_basic_material.pack(**center_args)
        self.button_reset.pack(**center_args)
        self.button_resolve.pack(**center_args)

        # tab order
        self.button_add_recipe.lift()

    def create_temporary_builder_for_material(self, material_name):
        toplevel = tk.Toplevel(self)
        toplevel.geometry(f"+{self.parent.winfo_x()}+{self.parent.winfo_y()}")
        builder = RecipeJsonBuilderTemporary(toplevel)
        builder.widget_products.widgets[0].set_name(material_name)
        return builder

    def add_new_recipe(self):
        recipes_json = self.get_recipes_json()

        try:
            recipe = self.get_recipe_from_entries()
        except ValueError:
            messagebox.showerror("Invalid recipe", "Enter one or more products")
            return

        recipes_json["composite"].append(recipe)

        self.save_recipes_json(recipes_json)
        self.reset_form()

    def add_basic_material(self):
        recipes_json = self.get_recipes_json()

        basic_material_name = self.widget_products.widgets[0].get_name()
        recipes_json["basic"].append(basic_material_name)

        self.save_recipes_json(recipes_json)
        self.reset_form()

    def save_recipes_json(self, recipes_json):
        save_path = self.entry_path.get()
        with save_path.open("w") as fout:
            json.dump(recipes_json, fout)

    def get_recipes_json(self):
        save_path = self.entry_path.get()
        with save_path.open("r") as fin:
            try:
                recipes_json = json.load(fin)
            except Exception:
                recipes_json = {"basic": [], "composite": []}

        return recipes_json

    def reset_form(self):
        self.entry_recipe_name.set("")
        self.entry_craft_time.set_raw("")

        self.widget_ingredients.reset()
        self.widget_ingredients.create_empty_widget()
        self.widget_products.reset()
        self.widget_products.create_empty_widget()

    def get_recipe_from_entries(self) -> dict:
        if len(self.widget_products.widgets) == 0:
            raise ValueError()

        if self.widget_products.widgets[0].get_name() == "":
            raise ValueError()

        products = self._get_json_from_name_amounts(self.widget_products.widgets)

        recipe_name = self.entry_recipe_name.get()
        if recipe_name == "":
            recipe_name = products[0]["id"]

        recipe_type = self.menu_recipe_type.get()
        if recipe_type == "":
            recipe_type = self.recipe_types[0]

        return {
            "id": recipe_name,
            "craft_type": recipe_type,
            "time": self.entry_craft_time.get(),
            "ingredients": self._get_json_from_name_amounts(self.widget_ingredients.widgets),
            "products": products
        }

    def resolve_dependencies(self):
        unresolved_names = []
        recipes: RecipesCollection = read_space_exploration(self.entry_path.get())
        for recipe in recipes.all_recipes:
            for ingredient in recipe.get_required():
                if not recipes.can_craft(ingredient):
                    unresolved_names.append(ingredient.name)

        if len(unresolved_names) == 0:
            messagebox.showinfo("Info", "no ingredient recipes need to be provided")
            return

        names_str = "\n".join((f"{i}. {el}" for i, el in enumerate(unresolved_names, start=1)))
        if not messagebox.askokcancel("Resolve names", f"following names will be resolved:\n{names_str}"):
            return

        for name in unresolved_names:
            builder = self.create_temporary_builder_for_material(name)
            builder.wait_window()

    @staticmethod
    def _get_json_from_name_amounts(widgets):
        w: NameAmountWidget
        return [{"id": w.get_name(), "amount": w.get_amount()} for w in widgets]


class RecipeJsonBuilderTemporary(RecipeJsonBuilder):
    def add_new_recipe(self):
        super().add_new_recipe()
        self.parent.destroy()

    def add_basic_material(self):
        super().add_basic_material()
        self.parent.destroy()


if __name__ == "__main__":
    RecipeJsonBuilder.run()
