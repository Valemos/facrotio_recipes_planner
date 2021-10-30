from json_automatic.enum_json import EnumByValueJson


class FilterMode(EnumByValueJson):
    WHITELIST = "whitelist"
    BLACKLIST = "blacklist"
