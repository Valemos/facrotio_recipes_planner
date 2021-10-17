from factorio.blueprint_analysis.a_sized_grid_object import ASizedGridObject
from factorio.game_environment.blueprint.types.position import Position


def _show_labels_grid(colors, labels, x_numbers, y_numbers, **kw):
    import numpy as np
    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    pc = plt.pcolor(colors, edgecolors=None, linewidths=4, cmap='Blues', vmin=0.0, vmax=1.0)
    pc.update_scalarmappable()

    plt.xticks([i+.5 for i in range(len(x_numbers))], labels=x_numbers)
    plt.yticks([i+.5 for i in range(len(y_numbers))], labels=y_numbers)

    for p, color in zip(pc.get_paths(), pc.get_facecolors()):
        x, y = p.vertices[:-2, :].mean(0)
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        pc.axes.text(x, y, labels[int(x)][int(y)], ha="center", va="center", color=color, **kw)

    plt.show()


class ObjectCoordinateGrid:

    def __init__(self):
        self._grid: list[list[object]] = []
        self._all_objects: list[object] = []
        self._array_start_shift = Position(0, 0)

    @property
    def size_x(self):
        return len(self._grid)

    @property
    def size_y(self):
        if len(self._grid) == 0:
            return 0
        return len(self._grid[0])

    @property
    def min_x(self):
        return int(- self._array_start_shift.x)

    @property
    def max_x(self):
        return int(self.size_x - 1 - self._array_start_shift.x)

    @property
    def min_y(self):
        return int(- self._array_start_shift.y)

    @property
    def max_y(self):
        return int(self.size_y - 1 - self._array_start_shift.y)

    def place_object_at_position(self, obj, position: Position):
        if self.size_x == 0 and self.size_y == 0:
            self._grid = [[None]]
            self._array_start_shift = Position(-position.x, -position.y)
        self._extend_grid_for_position(position)
        self._set_at_position(obj, position)

    def place_grid_object(self, obj: ASizedGridObject):
        self.place_object_at_position(obj, obj.position.round())

    def remove_object_from_position(self, position: Position):
        self._set_at_position(None, position)

    def get(self, position: Position):
        try:
            return self._grid[self._get_grid_x(position.x)][self._get_grid_y(position.y)]
        except IndexError:
            return None

    def show_debug_grid(self, highlight: Position = None):
        if self.size_y == 0:
            return

        from copy import deepcopy
        import numpy

        colors = numpy.full((self.size_y, self.size_x), 0, dtype=numpy.float)
        if highlight is not None:
            colors[self._get_grid_x(highlight.y), self._get_grid_x(highlight.x)] = 1

        labels = deepcopy(self._grid)
        for x in range(self.size_x):
            for y, obj in enumerate(labels[x]):
                if obj is not None:
                    labels[x][y] = obj.__class__.__name__
                    colors[y, x] = 0.5

        x_numbers = numpy.round(numpy.linspace(self.min_x, self.max_x + 1, self.size_x + 1), 2)
        y_numbers = numpy.round(numpy.linspace(self.min_y, self.max_y + 1, self.size_y), 2)
        _show_labels_grid(colors, labels, x_numbers, y_numbers)

    def _get_grid_x(self, x):
        return int(x + self._array_start_shift.x)

    def _get_grid_y(self, y):
        return int(y + self._array_start_shift.y)

    def _extend_grid_for_position(self, position: Position):
        # order is important. at first extend rows, than columns in that rows
        self._extend_to_fit_x(position.x)
        self._extend_to_fit_y(position.y)

    def _set_at_position(self, obj, position):
        self._grid[self._get_grid_x(position.x)][self._get_grid_y(position.y)] = obj
        if obj is not None:
            if obj not in self._all_objects:
                self._all_objects.append(obj)

    def _extend_to_fit_x(self, x):
        min_x = self.min_x
        max_x = self.max_x

        x = round(x)

        if x < min_x:
            self._extend_x(min_x - x, 0)
            self._array_start_shift.x = -x
        elif x > max_x:
            self._extend_x(x - max_x, self.size_y)

    def _extend_to_fit_y(self, y):
        min_y = self.min_y
        max_y = self.max_y

        y = round(y)

        if y < min_y:
            self._extend_y(min_y - y, 0)
            self._array_start_shift.y = -y
        elif y > max_y:
            self._extend_y(y - max_y, self.size_y)

    def _extend_x(self, amount, index):
        for _ in range(amount):
            self._grid.insert(index, [None for _ in range(self.size_y)])

    def _extend_y(self, amount, index):
        x_list: list
        for x_list in self._grid:
            for _ in range(amount):
                x_list.insert(index, None)

    def iterate_objects(self):
        yield from iter(self._all_objects)
