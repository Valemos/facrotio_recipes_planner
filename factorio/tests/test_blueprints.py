import unittest

from factorio.blueprint_analysis.blueprint_resolver import BlueprintResolver
from factorio.game_environment.blueprint.blueprint import Blueprint
from factorio.game_environment.game_environment import GameEnvironment


game_env = GameEnvironment.load_default()


class TestBlueprints(unittest.TestCase):

    @staticmethod
    def resolve(string):
        return BlueprintResolver(game_env, Blueprint.from_factorio_string(string))

    def test_junction_blueprint(self):
        string = "0eNqdleFugyAUhd/l" \
            "/tZGKIr6KsuyoL1pSRQN0G1N47sP69Z1C7SWnxD4zrk398AZmu6Io5bKQn0G2Q7KQP1yBiP3SnTznj2NCDVIiz0koEQ" \
            "/r4Qx2DedVPu0F+1BKkwpTAlItcNPqMmUPERYLZQZB23TBjt7c5lOrwmgstJKXMxcFqc3dewb1I5" \
            "+30YC42Dc5UHN2rObnG7yBE5Ql9Umd0IaW7k40oNK9yh0+nFA7GC2/U+MPi1WBcTaYRxRp61oOvQpba9KUhnU1u156OybXmUX+k46" \
            "/nKAepgs1G4POf8hE0f2sPIYVuZnFatq5cFaCw+TP" \
            "+GveFBrGcMK1FpdWWbspA3UWiwM6meQLMbQNgAjMbA8AKMxMBaArcvAdbr4mrkgvyEw1qU8bQ9o7N1s8YC9" \
            "/Lmx5WsiSoqYBoYcRoWgCMDKtY0r/9hyz/flqa9vPpcE3lGbpQklYbyinLFtxgo2TV8zTRxv "
        resolver = self.resolve(string)
        pass
