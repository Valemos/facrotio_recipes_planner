import base64
import json
import zlib


def get_factorio_json(data):
    result = data[1:]
    result = base64.decodebytes(result.encode('utf-8'))
    result = zlib.decompress(result)
    return json.loads(result)
