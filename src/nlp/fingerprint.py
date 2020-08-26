import json
from dataclasses import asdict

import pyarrow as pa
import xxhash

from .info import DatasetInfo
from .utils.py_utils import dumps


def hashregister(t):
    def proxy(func):
        Hasher.dispatch[t] = func
        return func

    return proxy


class Hasher:
    """Hasher that accepts python objets as inputs."""

    dispatch = {}

    def __init__(self):
        self.m = xxhash.xxh64()

    @classmethod
    def hash_bytes(cls, value):
        value = [value] if isinstance(value, bytes) else value
        m = xxhash.xxh64()
        for x in value:
            m.update(x)
        return m.hexdigest()

    @classmethod
    def hash_default(cls, value):
        return cls.hash_bytes(dumps(value))

    @classmethod
    def hash(cls, value):
        if type(value) in cls.dispatch:
            return cls.dispatch[type(value)](cls, value)
        else:
            return cls.hash_default(value)

    def update(self, value):
        self.m.update(f"=={type(value)}==".encode("utf8"))
        self.m.update(self.hash(value).encode("utf-8"))

    def hexdigest(self):
        return self.m.hexdigest()


# Register a new hasher can be useful for two possible reasons:
# 1 - optimize the hashing of large amount of data (e.g. pa.Table)
# 2 - take advantage of a custom serialization method (e.g. DatasetInfo)


@hashregister(pa.Table)
def _hash_pa_table(hasher, value):
    def _hash_pa_array(value):
        if isinstance(value, pa.ChunkedArray):
            return hasher.hash_bytes(c.to_string() for c in value.chunks)
        else:
            return hasher.hash_bytes(value)

    value = "-".join(col + "-" + _hash_pa_array(value[col]) for col in sorted(value.column_names))
    return hasher.hash_bytes(value.encode("utf-8"))


@hashregister(DatasetInfo)
def _hash_dataset_info(hasher, value):
    return hasher.hash_bytes(json.dumps(asdict(value)).encode("utf-8"))


def generate_fingerprint(dataset):
    state = dataset.__getstate__()
    hasher = Hasher()
    for key in sorted(state):
        if key == "_fingerprint":
            continue
        hasher.update(key)
        hasher.update(state[key])
    return hasher.hexdigest()


def update_fingerprint(fingerprint, transform, transform_args):
    hasher = Hasher()
    hasher.update(fingerprint)
    hasher.update(transform)
    for key in sorted(transform_args):
        hasher.update(key)
        hasher.update(transform_args[key])
    return hasher.hexdigest()
