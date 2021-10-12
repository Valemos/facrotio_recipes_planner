from factorio.recipe_util.recipe_json_reading import read_vanilla_database

fluid_types = set()
basic_ore_types = {"copper-ore", "iron-ore"}
furnace_recipe_types = {"iron-plate", "copper-plate", "steel-plate"}
oil_recipe_types = {"light-oil", "heavy-oil", "petroleum-gas"}
chemical_recipe_types = oil_recipe_types.union({"solid-fuel", "plastic"})

recipes_vanilla = read_vanilla_database("factorio/recipes.json")
