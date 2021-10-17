from pathlib import Path

from factorio.blueprint_analysis.a_grid_object import AGridObject
from factorio.blueprint_analysis.object_coordinate_grid import ObjectCoordinateGrid
from factorio.crafting_tree_builder.placeable_types.a_material_transport import AMaterialTransport
from factorio.crafting_tree_builder.placeable_types.assembling_machine import AssemblingMachine
from factorio.game_environment.blueprint.blueprint import Blueprint
from factorio.game_environment.blueprint.blueprint_object import BlueprintObject
from factorio.game_environment.blueprint.types.position import Position
from factorio.game_environment.game_environment import GameEnvironment


class BlueprintResolver:

    def __init__(self, game_env: GameEnvironment, blueprint: Blueprint):
        self._game_env = game_env
        self._blueprint = blueprint
        self._grid = ObjectCoordinateGrid()
        self._unresolved_objects: list[AGridObject] = []
        self._assemblers: list[AssemblingMachine] = []
        self._material_transports: list[AMaterialTransport] = []

        for obj in blueprint.entities:
            self.add_blueprint_object(obj)

    @property
    def grid(self):
        return self._grid

    def add_blueprint_object(self, obj_info: BlueprintObject):
        game_object = obj_info.to_game_object(self._game_env)
        self.add_grid_object(game_object, obj_info.position)

    def add_grid_object(self, game_object, position: Position):
        if isinstance(game_object, AssemblingMachine):
            self._assemblers.append(game_object)
        elif isinstance(game_object, AMaterialTransport):
            self._add_material_transport(game_object, position)
        else:
            self._unresolved_objects.append(game_object)

        # todo add size of objects if possible
        self._grid.place_object(game_object, position)

    def _add_material_transport(self, obj: AMaterialTransport, position: Position):
        self._material_transports.append(obj)
        for possible_connection in obj.iterate_connection_spots(position):
            other_obj = self._grid.get(possible_connection)
            if isinstance(other_obj, AMaterialTransport):
                obj.try_connect(other_obj)


if __name__ == '__main__':
    _game_environment = GameEnvironment.load_default()

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

    _string2 = "0eNqN0WELgjAQBuD/8n5e0uay2l+JCK0jDnSKm5HI/nsuCQwL" \
               "/Hjb3bPj3YCi7Khp2XqYAXytrYM5DXB8t3kZz3zfEAzYUwUBm1exck3J3lOLIMD2Rk8YGc4CZD17psl4F" \
               "/3FdlUxdhq5nBZoajcO1Da+FJFMJjuBHmaj0tG+cUvX6V4FsSDVKlJ/wGT3TeofZLqKzP5tmf0g9SryONsyRvkO3Mz+R" \
               "+BBrZuyOEi9P6q91ulWZzqEF/Qrk9s= "

    _resolver = BlueprintResolver(_game_environment, Blueprint.from_factorio_string(_string2))
    # _resolver.grid.show_debug_grid()
    pass
