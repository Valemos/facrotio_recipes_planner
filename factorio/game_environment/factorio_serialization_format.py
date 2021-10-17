import base64
import json
import zlib


def deserialize_factorio_format(string):
    decoded = base64.b64decode(string[1:])
    decompressed = zlib.decompress(decoded)
    return json.loads(decompressed)


def serialize_factorio_format(json_obj):
    decompressed = json.dumps(json_obj, separators=(',', ':')).encode('ascii')
    compressed = zlib.compress(decompressed, level=9)
    return (b'0' + base64.b64encode(compressed)).decode("ascii")


if __name__ == '__main__':
    _sample_str = "0eNqV0+9uhCAMAPB36We4+AfU81Uuy4LaeU0UCeoyY3z34Zkzl8nM9rGk/Ci0zFA0IxpLeoB8Bio73UN" \
                  "+m6GnWqtmXRsmg5ADDdgCA63aNeqo4RY" \
                  "/SKOdYGFAusIvyMPljQHqgQbCzXkE07se2wKtS9iFYrRuM1d9j23RkK55q8q7A90hpuud0On1" \
                  "+FWV4iIZTJDL60UuCzuw0c4ePR6eiUnkF2P" \
                  "/VY9SErxKDCqyWG4JkccVu2vIIB86Xttu1JVPjp9y8FNOPLLc5fKOLZWq4aZRrq8eOXvK4V/k5B81J7" \
                  "/W7HuN9Kxv0WnfpL9v2ZkYn4rZKrr5fUx6/vIxGHyi7bdLZKFIr1EqRByIRCzLNzakDkc= "

    from factorio.crafting_tree_builder.placeable_types import Blueprint
    from factorio.crafting_tree_builder.placeable_types import BlueprintEntity

    b: Blueprint = Blueprint.from_json(deserialize_factorio_format(_sample_str))
    e: BlueprintEntity
    for e in b.entities:
        print(e.name)

    # import pyperclip
    # pyperclip.copy(serialize_factorio_format(b.to_json()))
    pass
