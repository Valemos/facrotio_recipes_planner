import hashlib


def hash_det(obj):
    hashing = hashlib.md5()
    if isinstance(obj, tuple):
        for o in obj:
            hashing.update(hash(o).to_bytes(16, byteorder='big', signed=True))
    elif isinstance(obj, str):
        hashing.update(obj.encode("utf-8"))
    else:
        return hash(obj)

    return int(hashing.hexdigest(), 16)
