from serialization.enum_json import EnumByValueJson
from serialization.enum_mapping_json import EnumMappingJson


class ResourceCategory(EnumByValueJson):
    BASIC_SOLID = "basic-solid"
    SE_CORE_MINING = "se-core-mining"
    BASIC_FLUID = "basic-fluid"
    HARD_RESOURCE = "hard-resource"


class ResourceCategoryMapping(EnumMappingJson):
    __element_type__ = ResourceCategory
