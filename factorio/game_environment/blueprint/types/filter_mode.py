from serialization.enum_json import EnumByValueJson


class FilterMode(EnumByValueJson):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"
