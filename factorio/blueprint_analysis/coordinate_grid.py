from factorio.game_environment.parsing.types.position import Position


class CoordinateGrid:

    def __init__(self):
        self._objects: list[list[object]] = []
        self._array_start_shift = Position(0, 0)

    @property
    def size_x(self):
        return len(self._objects)

    @property
    def size_y(self):
        if len(self._objects) == 0:
            return 0
        return len(self._objects[0])

    @property
    def min_x(self):
        return - self._array_start_shift.x

    @property
    def max_x(self):
        return self.size_x - 1 - self._array_start_shift.x

    @property
    def min_y(self):
        return - self._array_start_shift.y

    @property
    def max_y(self):
        return self.size_y - 1 - self._array_start_shift.y

    def place_object(self, obj, position: Position):
        if self.size_x == 0 and self.size_y == 0:
            self._objects = [[None]]
            self._array_start_shift = Position(-position.x, -position.y)
        self._extend_grid_for_position(position)
        self._set_at_position(obj, position)

    def remove_object_from_position(self, position: Position):
        self._set_at_position(None, position)

    def get(self, position: Position):
        return self._objects[self._get_x(position.x)][self._get_y(position.y)]

    def _get_x(self, x):
        return x + self._array_start_shift.x

    def _get_y(self, y):
        return y + self._array_start_shift.y

    def _extend_grid_for_position(self, position: Position):
        # order is important. at first extend rows, than columns in that rows
        self._extend_to_fit_x(position.x)
        self._extend_to_fit_y(position.y)

    def _set_at_position(self, obj, position):
        self._objects[self._get_x(position.x)][self._get_y(position.y)] = obj

    def _extend_to_fit_x(self, x):
        min_x = self.min_x
        max_x = self.max_x

        if x < min_x:
            self._extend_x(min_x - x, 0)
            self._array_start_shift.x = -x
        elif x > max_x:
            self._extend_x(x - max_x, self.size_y)

    def _extend_to_fit_y(self, y):
        min_y = self.min_y
        max_y = self.max_y

        if y < min_y:
            self._extend_y(min_y - y, 0)
            self._array_start_shift.y = -y
        elif y > max_y:
            self._extend_y(y - max_y, self.size_y)

    def _extend_x(self, amount, index):
        for _ in range(amount):
            self._objects.insert(index, [None for _ in range(self.size_y)])

    def _extend_y(self, amount, index):
        x_list: list
        for x_list in self._objects:
            for _ in range(amount):
                x_list.insert(index, None)
