from factorio.crafting_tree_builder.coordinate_grid import CoordinateGrid
from factorio.game_environment.parsing.blueprint import Blueprint
from factorio.game_environment.parsing.blueprint_object import BlueprintObject


class CraftingTreeBuilder:

    def __init__(self) -> None:
        self._grid = CoordinateGrid()

    @classmethod
    def from_blueprint(cls, blueprint: Blueprint):
        builder = cls()
        for obj in blueprint.objects:
            builder.add_blueprint_object(obj)

    def add_blueprint_object(self, obj: BlueprintObject):
        self._grid.place_object(obj, obj.position)
