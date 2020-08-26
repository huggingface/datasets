import timeit

import numpy as np

import nlp
from nlp.features import _ArrayXD


def get_duration(func):
    def wrapper(*args, **kwargs):
        starttime = timeit.default_timer()
        _ = func(*args, **kwargs)
        delta = timeit.default_timer() - starttime
        return delta

    wrapper.__name__ = func.__name__

    return wrapper


def generate_examples(features: dict, num_examples=100, seq_shapes=None):
    dummy_data = []
    seq_shapes = seq_shapes or {}
    for i in range(num_examples):
        example = {}
        for col_id, (k, v) in enumerate(features.items()):
            if isinstance(v, _ArrayXD):
                data = np.random.rand(*v.shape).astype(v.dtype)
            elif isinstance(v, nlp.Value):
                data = "foo"
            elif isinstance(v, nlp.Sequence):
                while isinstance(v, nlp.Sequence):
                    v = v.feature
                shape = seq_shapes[k]
                data = np.random.rand(*shape).astype(v.dtype)
            example[k] = data
            dummy_data.append((i, example))

    return dummy_data
