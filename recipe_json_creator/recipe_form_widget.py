import tkinter as tk

from factorio.types.material import Material
from factorio.types.material_collection import MaterialCollection
from factorio.types.recipe import CraftStationType, Recipe
from factorio.types.recipes_collection import RecipesCollection
from gui.entry_validator_with_label import EntryFloatWithLabel
from gui.entry_with_label import EntryWithLabel
from gui.menu_with_handler import MenuWithHandler
from gui.widget_list import WidgetList
from recipe_json_creator.name_amount_widget import NameAmountWidget


class RecipeFormWidget(tk.Frame):

    recipe_types = [type.name for type in CraftStationType]

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.menu_recipe_type = MenuWithHandler(self, 15, self.recipe_types)
        self.menu_recipe_type.set(self.recipe_types[0])

        self.entry_craft_time = EntryFloatWithLabel(self, "Craft time: ", 10)
        self.widget_ingredients = WidgetList(self, "Add ingredient", NameAmountWidget)
        self.widget_products = WidgetList(self, "Add product", NameAmountWidget)
        self.entry_recipe_name = EntryWithLabel(self, "Recipe name: ", 15)

        _left_args = {"side": tk.TOP, "anchor": tk.W, "pady": 5, "padx": 10}
        _right_args = {"side": tk.TOP, "anchor": tk.E, "pady": 5, "padx": 10}
        _center_args = {"side": tk.TOP, "anchor": tk.CENTER, "pady": 5, "padx": 10}

        self.menu_recipe_type.pack(**_center_args)
        self.entry_craft_time.pack(**_right_args)

        tk.Label(self, text="Ingredients").pack(**_center_args)
        self.widget_ingredients.pack(**_center_args)

        tk.Label(self, text="Products").pack(**_center_args)
        self.widget_products.pack(**_center_args)

        self.entry_recipe_name.pack(**_center_args)

    def reset(self):
        self.entry_recipe_name.set("")
        self.entry_craft_time.set_raw("")

        self.widget_ingredients.reset()
        self.widget_ingredients.create_empty_widget()
        self.widget_products.reset()
        self.widget_products.create_empty_widget()

    def set_basic_material(self, material_name):
        self.widget_products.get_widget_at(0).set_name(material_name)

    def is_basic_material(self):
        return len(self.get_nonempty_widgets(self.widget_ingredients.item_widgets)) == 0

    def get_basic_material_name(self):
        if len(self.get_nonempty_widgets(self.widget_products.item_widgets)) == 0:
            raise ValueError("no products provided")
        return self.widget_products.get_widget_at(0).get_name()

    def get_recipe(self) -> Recipe:
        if self.widget_products.item_amount:
            raise ValueError()

        if self.widget_products.get_widget_at(0).get_name() == "":
            raise ValueError()

        ingredients = self.get_materials_from_name_amount_widgets(self.widget_ingredients.item_widgets)
        results = self.get_materials_from_name_amount_widgets(self.widget_products.item_widgets)

        name = self.entry_recipe_name.get()
        if name == "":
            name = results[0].name

        recipe_type = self.menu_recipe_type.get()
        if recipe_type == "":
            recipe_type = self.recipe_types[0]

        recipe = Recipe(name=name,
                        time=self.entry_craft_time.get(),
                        producer_type=CraftStationType[recipe_type],
                        ingredients=ingredients,
                        results=results)
        return recipe

    def set_recipe(self, recipe: Recipe):
        self.entry_recipe_name.set(recipe.name)
        self.entry_craft_time.set(recipe.time)
        self.menu_recipe_type.set(recipe.producer_type.name)

        self.widget_ingredients.reset()
        for ingredient in recipe.get_required():
            widget = self.widget_ingredients.create_empty_widget()
            widget.set_name(ingredient.name)
            widget.set_amount(ingredient.amount)

        self.widget_products.reset()
        for result in recipe.get_results():
            widget = self.widget_products.create_empty_widget()
            widget.set_name(result.name)
            widget.set_amount(result.amount)

    def add_item_to_collection(self, recipes: RecipesCollection):
        """Adds basic material or composite recipe to RecipesCollection"""
        if self.is_basic_material():
            material_name = self.get_basic_material_name()
            recipes.add_unique_basic_material(material_name)
        else:
            recipes.add_unique_recipe(self.get_recipe())

    @classmethod
    def get_materials_from_name_amount_widgets(cls, widgets):
        nonempty = cls.get_nonempty_widgets(widgets)
        return MaterialCollection([Material(w.get_name(), w.get_amount()) for w in nonempty])

    @staticmethod
    def get_nonempty_widgets(widgets):
        return list(w for w in widgets if not w.is_empty())

    def get_recipe_name(self):
        if self.is_basic_material():
            return self.get_basic_material_name()
        else:
            return self.entry_recipe_name.get()
