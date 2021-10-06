import json
import tkinter as tk
from pathlib import Path

from gui.entry_validator_with_label import EntryFloatWithLabel, EntryIntegerWithLabel
from gui.entry_with_label import EntryWithLabel
from gui.menu_with_handler import MenuWithHandler
from gui.widget_list import WidgetList
from recipe_json_creator.name_amount_widget import NameAmountWidget


class RecipeJsonBuilder(tk.Frame):

    recipes_path = Path("test/recipes.json")
    recipe_types = ["Assembling", "Furnace", "Chemical"]

    @staticmethod
    def run():
        root = tk.Tk()
        app = RecipeJsonBuilder(root)
        app.mainloop()

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.entry_recipe_name = EntryWithLabel(root, "Name: ", 10)
        self.menu_recipe_type = MenuWithHandler(root, 10, self.recipe_types)
        self.menu_recipe_type.handle_option_changed(0)
        self.entry_craft_time = EntryFloatWithLabel(root, "Craft time: ", 10)
        self.entry_yield_amount = EntryIntegerWithLabel(root, "Yield: ", 10)
        self.widget_ingredients = WidgetList(root, "Add ingredient", NameAmountWidget)
        self.widget_products = WidgetList(root, "Add product", NameAmountWidget)

        self.button_add_recipe = tk.Button(root, text="Append recipe", command=self.add_new_recipe)

        # pack
        left_args = {"side": tk.TOP, "anchor": tk.E, "pady": 5}
        center_args = {"side": tk.TOP, "anchor": tk.CENTER, "pady": 5}
        self.entry_recipe_name.pack(**left_args)
        self.menu_recipe_type.pack(**center_args)
        self.entry_craft_time.pack(**left_args)
        self.entry_yield_amount.pack(**left_args)
        self.widget_ingredients.pack(**left_args)
        self.widget_products.pack(**left_args)

        self.button_add_recipe.pack(**center_args)

    def add_new_recipe(self):
        if self.recipes_path.exists():
            with self.recipes_path.open("r") as fin:
                initial_json = json.load(fin)
        else:
            initial_json = []

        recipe = self.get_recipe_from_entries()
        initial_json.append(recipe)

        with self.recipes_path.open("w") as fout:
            json.dump(initial_json, fout)

    def reset_form(self):
        self.entry_recipe_name.set("")
        self.entry_craft_time.set(0)
        self.entry_yield_amount.set(0)
        self.menu_recipe_type.set(self.recipe_types[0])

        self.widget_ingredients.reset()
        self.widget_products.reset()
        self.widget_products.create_empty_widget()

    def get_recipe_from_entries(self) -> dict:
        w: NameAmountWidget
        return {
            "id": self.entry_recipe_name.get(),
            "craft_type": self.menu_recipe_type.get(),
            "time": self.entry_craft_time.get(),
            "ingredients": [{"name": w.get_name(), "amount": w.get_amount()}
                            for w in self.widget_ingredients.widgets],
            "products": [{"name": w.get_name(), "amount": w.get_amount()}
                         for w in self.widget_products.widgets]
        }


if __name__ == "__main__":
    RecipeJsonBuilder.run()
