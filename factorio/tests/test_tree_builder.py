import unittest

from factorio.game_environment.game_environment import GameEnvironment


class TestTreeBuilder(unittest.TestCase):

    def setUp(self) -> None:
        self.game_env = GameEnvironment()
