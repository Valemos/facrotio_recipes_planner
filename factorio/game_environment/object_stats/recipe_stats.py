from dataclasses import dataclass
from typing import Optional

from factorio.game_environment.object_stats.a_stats import AStats
from factorio.game_environment.object_stats.crafting_category import CraftingCategory
from factorio.game_environment.object_stats.material_stats import MaterialStatsList, MaterialStats
from factorio.types.material_collection import MaterialCollection
from factorio.types.recipe import Recipe
from serialization.string_list_json import StringListJson


@dataclass
class RecipeStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    enabled: bool = None
    hidden: bool = None
    hidden_from_player_crafting: bool = None
    emissions_multiplier: float = None
    category: CraftingCategory = None
    group: str = None
    subgroup: str = None
    order: str = None
    energy: int = None
    ingredients: MaterialStatsList = None
    products: MaterialStatsList = None
    main_product: MaterialStats = None

    def to_object(self) -> Optional[Recipe]:
        if self.hidden or self.hidden_from_player_crafting:
            return None

        return Recipe(name=self.name,
                      category=self.category,
                      ingredients=MaterialCollection([m.to_object() for m in self.ingredients]),
                      results=MaterialCollection([m.to_object() for m in self.products]))
