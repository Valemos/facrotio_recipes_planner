import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from factorio.types.recipe import CraftStationType
from gui.entry_validator_with_label import EntryFloatWithLabel, EntryIntegerWithLabel, EntryExistingPath
from gui.entry_with_label import EntryWithLabel
from gui.menu_with_handler import MenuWithHandler
from gui.widget_list import WidgetList
from recipe_json_creator.name_amount_widget import NameAmountWidget


class RecipeJsonBuilder(tk.Frame):
    default_path = Path("./test/recipes.json")
    recipe_types = [type.name for type in CraftStationType]

    @staticmethod
    def run():
        root = tk.Tk()
        app = RecipeJsonBuilder(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)
        self.winfo_toplevel().title("Recipe Builder")

        self.entry_path = EntryExistingPath(root, "Path: ", 15, self.default_path)
        self.entry_path.set(self.default_path)

        self.menu_recipe_type = MenuWithHandler(root, 15, self.recipe_types)
        self.entry_craft_time = EntryFloatWithLabel(root, "Craft time: ", 10)
        self.widget_ingredients = WidgetList(root, "Add ingredient", NameAmountWidget)
        self.widget_products = WidgetList(root, "Add product", NameAmountWidget)
        self.entry_recipe_name = EntryWithLabel(root, "Recipe name: ", 15)

        self.reset_form()

        self.button_add_recipe = tk.Button(root, text="Append recipe", command=self.add_new_recipe)
        self.button_reset = tk.Button(root, text="Reset", command=self.reset_form)

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
        self.button_reset.pack(**center_args)

        # tab order
        self.button_add_recipe.lift()

    def add_new_recipe(self):
        save_path = self.entry_path.get()
        with save_path.open("r") as fin:
            try:
                initial_json = json.load(fin)
            except Exception:
                initial_json = []

        try:
            recipe = self.get_recipe_from_entries()
        except ValueError:
            messagebox.showerror("Invalid recipe", "Enter one or more products")
            return

        initial_json.append(recipe)
        self.reset_form()

        with save_path.open("w") as fout:
            json.dump(initial_json, fout)

    def reset_form(self):
        self.entry_recipe_name.set("")
        self.menu_recipe_type.handle_option_changed(0)
        self.entry_craft_time.set(0)

        self.widget_ingredients.reset()
        self.widget_products.reset()
        self.widget_products.create_empty_widget()

    def get_recipe_from_entries(self) -> dict:
        if len(self.widget_products.widgets) == 0:
            raise ValueError()

        if self.widget_products.widgets[0].get_name() == "":
            raise ValueError()

        products = self._get_json_from_name_amounts(self.widget_products.widgets)
        if self.entry_recipe_name.get() != "":
            recipe_name = self.entry_recipe_name.get()
        else:
            recipe_name = products[0]["name"]

        return {
            "id": recipe_name,
            "craft_type": self.menu_recipe_type.get(),
            "time": self.entry_craft_time.get(),
            "ingredients": self._get_json_from_name_amounts(self.widget_ingredients.widgets),
            "products": products
        }

    @staticmethod
    def _get_json_from_name_amounts(widgets):
        w: NameAmountWidget
        return [{"name": w.get_name(), "amount": w.get_amount()} for w in widgets]


if __name__ == "__main__":
    RecipeJsonBuilder.run()
