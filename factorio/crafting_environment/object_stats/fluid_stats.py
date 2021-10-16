from factorio.crafting_environment.object_stats.a_stats import AStats
from factorio.types.material import Material
from serialization.string_list_json import StringListJson


class FluidStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    order: str = None
    default_temperature: int = None
    max_temperature: int = None
    fuel_value: int = None
    emissions_multiplier: float = None

    def to_object(self):
        return Material(self.name)
