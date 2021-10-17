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


def read_stats_file(json_path, stats_class):
    result = {}
    json_objects = read(json_path)
    for name, stats in zip(json_objects.keys(), read_stats_iter(json_objects.values(), stats_class)):
        result[name] = stats
    return result
