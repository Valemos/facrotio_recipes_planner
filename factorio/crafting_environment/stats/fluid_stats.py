from factorio.crafting_environment.stats.a_stats import AStats
from serialization.string_list_json import StringListJson


class FluidStats(AStats):
    name: str = None
    localised_name: StringListJson = None
    order: str = None
    default_temperature: int = None
    max_temperature: int = None
    fuel_value: int = None
    emissions_multiplier: float = None

    def to_object(self) -> Optional[object]:
        return None