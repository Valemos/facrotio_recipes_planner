from factorio.crafting_environment.objects.entity_specialty import EntitySpecialtyEnum
from factorio.types.named_item import NamedItem


class FluidPipeType(EntitySpecialtyEnum):
    REGULAR = NamedItem("oil-refinery")
    UNDERGROUND = NamedItem("chemical-plant")
