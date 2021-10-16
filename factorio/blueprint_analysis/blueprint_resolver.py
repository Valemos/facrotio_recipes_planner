from pathlib import Path

from factorio.blueprint_analysis.grid_object import GridObject
from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.crafting_tree_builder.objects.assembling_machine import AssemblingMachine
from factorio.crafting_tree_builder.objects.material_transport import AMaterialTransport
from factorio.game_environment.game_environment import GameEnvironment
from factorio.game_environment.parsing.blueprint import Blueprint
from factorio.game_environment.parsing.blueprint_object import BlueprintObject
from factorio.game_environment.parsing.types.position import Position


class BlueprintResolver:

    def __init__(self, game_env: GameEnvironment, blueprint: Blueprint):
        self._game_env = game_env
        self._blueprint = blueprint
        self._grid = ObjectCoordinateGrid()
        self._objects_by_name: dict[str, list[GridObject]] = {}
        self._assemblers = []
        self._material_transport = []

        for obj in blueprint.entities:
            self.add_blueprint_object(obj)

    def add_blueprint_object(self, obj_info: BlueprintObject):
        game_object = self._game_env.get_placeable_stats(obj_info.name).to_object()

        orientation = None
        if obj_info.direction is not None:
            orientation = obj_info.direction
        elif obj_info.orientation is not None:
            orientation = obj_info.orientation

        grid_object = GridObject(game_object, Position(), orientation)
        self.add_grid_object(obj_info.name, grid_object)

    def add_grid_object(self, name: str, grid_object: GridObject):
        if name not in self._objects_by_name:
            self._objects_by_name[name] = []
        self._objects_by_name[name].append(grid_object)
        self._grid.place_object(grid_object, grid_object.position)

    def resolve_connections(self):
        for obj in self._grid.iterate_objects():
            if isinstance(obj.item, AssemblingMachine):
                self._assemblers.append(obj)
            elif isinstance(obj.item, AMaterialTransport):
                self._material_transport.append(obj)

        # todo merge conveyors to item transport and connect them to assemblers
        pass


if __name__ == '__main__':
    _game_environment = GameEnvironment.from_folder(Path('/home/anton/.factorio/script-output/recipe-lister/'))

    _string = "0eNqdmu9u2jAUxd/Fn9PK/x3zKlM10darItEEJWFaVfHug6GFTsTj3POpAqU/ju17fK4Nn+p5dyj7setntflU3cvQT2rz7VNN3Vu" \
              "/3Z3fmz/2RW1UN5d31ah++35+NY/bftoP4/zwXHazOjaq61/LL7Uxx6dGlX7u5q5cSH9efHzvD+/PZTw9UGM0aj9Mp38b+vOnnlG" \
              "+fQyN+lCbBxMew/HY3MAsBfPrMLfAun4q43x6bwWT/8E06rUby8vlibgC9Qt0moe+PPw4jP32payQg" \
              "/k71jVxAR9pcHWJfgUdkXEHKxt3ovQGRG8L6fV1vXYFmvF1iv9bJ6MhdUmmzghcE" \
              "+66xliKVrGNcZQJbYXmhS60SDWaQGl0FY1Rbmq3CuJc4hCXmJZiW4idhVsGtEhWC41tEetYI3f26mJZK3Q2Js9RXqy4x" \
              "3qKVqlzy7nGVGiRoukKLQn3CQ2VYCt3tlmVlyn3GcR9TgvdBw3dGUqxhhRbobM1Yh3n5M5eXSznhc7G5AXKi5V6d5GiVbzo" \
              "ru6Z9rturrhnWeYWGK4gb3xYwBV9Avt4/xV2V6fXjM4MoSVnmyhTbRl0RszpHVQLS/VnQK1ntnpsIiSZlGVoKqDyegV7SWt" \
              "nZDolnZ2WoanYgtBB4LtrdmHoq+8O/WsZ38bh9Pe+7lt7NMttR78/nK81bj9LcnaS7UxB0goGGVrSF8p2piCJuSRDU5lXi" \
              "ZSQGFjF3UESdku9RWjQGdqOl9KK95FRS/xxRacbvff9EQ0kfynfBMiXZF8STXZ0TKxiaM+g03q9ReokhumMTKBi6CSquwz" \
              "U3XCYa4VHpWKCxpGZLIemKGkGDalOhpkQTLVl2gRMtWPQmGrPdCAYOjBobEIi0xVgqhPTy2DollGNTUhmVEPoVjNtEjQhr" \
              "WHQmGrLdGAY2jFobEKoq0oMTd28YBMSmcYvQOjEXExg6JbpRTB0ZpozCJ010/RgaMM0PRjaMomOoR2T6BiaykYMTX11jaE" \
              "jd/D39YN/vcHMiYk0bBwtE2kYOjM7OIQ2mopLkE19473CfmouP13ZfPmlS6N+lnG6PNCetqVsk/dO++iPx9+N+FI3 "

    _resolver = BlueprintResolver(_game_environment, Blueprint.from_factorio_string(_string))
    pass
