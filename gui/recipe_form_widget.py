import tkinter as tk

from factorio.crafting_tree_builder.internal_types.material import Material
from factorio.crafting_tree_builder.internal_types.material_collection import MaterialCollection
from factorio.crafting_tree_builder.internal_types.recipe import Recipe
from factorio.crafting_tree_builder.internal_types.recipes_collection import RecipesCollection
from factorio.game_environment.object_stats.crafting_category import CraftingCategory
from gui.entry_validator_with_label import EntryFloatWithLabel
from gui.entry_with_label import EntryWithLabel
from gui.menu_object_selector_widget import MenuObjectSelectorWidget
from gui.modified_widget_list import DynamicWidgetList
from gui.name_amount_widget import NameAmountWidget


class RecipeFormWidget(tk.Frame):

    def __init__(self, root, **kw):
        tk.Frame.__init__(self, root, **kw)

        self.menu_recipe_type = MenuObjectSelectorWidget(self, 15, {t.name: t for t in CraftingCategory})
        self.menu_recipe_type.set(CraftingCategory.ASSEMBLING)

        self.entry_craft_time = EntryFloatWithLabel(self, "Craft time: ", 10)
        self.widget_ingredients = DynamicWidgetList(self, NameAmountWidget, "Add ingredient")
        self.widget_products = DynamicWidgetList(self, NameAmountWidget, "Add product")
        self.entry_recipe_name = EntryWithLabel(self, "Recipe name: ", 15)

        self.entry_recipe_name.pack(side=tk.TOP, anchor=tk.CENTER, pady=5, padx=5)
        self.menu_recipe_type.pack(side=tk.TOP, anchor=tk.CENTER, pady=5, padx=5)
        self.entry_craft_time.pack(side=tk.TOP, anchor=tk.E, pady=5, padx=5)

        self.widget_ingredients.pack(side=tk.TOP, anchor=tk.CENTER, pady=5, padx=5)
        self.widget_products.pack(side=tk.TOP, anchor=tk.CENTER, pady=5, padx=5)

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
        return len(self.get_nonempty_widgets(self.widget_ingredients.item_widgets_iter)) == 0

    def get_first_product_name(self) -> str:
        if len(self.get_nonempty_widgets(self.widget_products.item_widgets_iter)) == 0:
            raise ValueError("no products provided")
        return self.widget_products.get_widget_at(0).get_name()

    def get_recipe(self) -> Recipe:
        if self.widget_products.item_amount == 0:
            raise ValueError("no products provided for recipe")

        name = self.get_or_deduce_recipe_name().strip()
        recipe_type = self.menu_recipe_type.get()

        ingredients = self.get_materials_from_name_amount_widgets(self.widget_ingredients.item_widgets_iter)
        results = self.get_materials_from_name_amount_widgets(self.widget_products.item_widgets_iter)

        recipe = Recipe(name=name,
                        time=self.entry_craft_time.get(),
                        category=recipe_type,
                        ingredients=ingredients,
                        results=results)
        return recipe

    def set_recipe(self, recipe: Recipe):
        self.entry_recipe_name.set(recipe.name)
        self.entry_craft_time.set(recipe.time)
        self.menu_recipe_type.set_string(recipe.category.name)

        self.widget_ingredients.reset()
        for ingredient in recipe.ingredients:
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
            material_name = self.get_first_product_name()
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

    def get_or_deduce_recipe_name(self) -> str:
        recipe_name = self.get_recipe_name()
        if recipe_name == "":
            if self.is_basic_material():
                return self.get_first_product_name()
            else:
                raise ValueError("cannot deduce recipe name from entries")
        else:
            return recipe_name

    def get_recipe_name(self):
        return self.entry_recipe_name.get()
