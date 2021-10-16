import json
from pathlib import Path


def read(file_path: Path) -> dict:
    with file_path.open("r") as fin:
        return json.load(fin)


def read_stats_iter(jsons_iter, stats_class):
    for stats_json in jsons_iter:
        yield stats_class.from_json(stats_json)


def read_stats(jsons_iter, stats_class):
    return list(read_stats_iter(jsons_iter, stats_class))


def read_stats_dict(json_path, stats_class):
    result = {}
    for stats in read_stats_iter(read(json_path).values(), stats_class):
        result[stats.name] = stats
    return result
