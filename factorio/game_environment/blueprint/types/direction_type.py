from serialization.enum_json import EnumByValueJson


class DirectionType(EnumByValueJson):
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7
    NO_DIRECTION = None
