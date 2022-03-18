import timeit

import numpy as np

import datasets
from datasets.arrow_writer import ArrowWriter
from datasets.features.features import _ArrayXD


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
            elif isinstance(v, datasets.Value):
                if v.dtype == "string":
                    data = "The small grey turtle was surprisingly fast when challenged."
                else:
                    data = np.random.randint(10, size=1).astype(v.dtype).item()
            elif isinstance(v, datasets.Sequence):
                while isinstance(v, datasets.Sequence):
                    v = v.feature
                shape = seq_shapes[k]
                data = np.random.rand(*shape).astype(v.dtype)
            example[k] = data

        dummy_data.append((i, example))

    return dummy_data


def generate_example_dataset(dataset_path, features, num_examples=100, seq_shapes=None):
    dummy_data = generate_examples(features, num_examples=num_examples, seq_shapes=seq_shapes)

    with ArrowWriter(features=features, path=dataset_path) as writer:
        for key, record in dummy_data:
            example = features.encode_example(record)
            writer.write(example)

        num_final_examples, num_bytes = writer.finalize()

    if not num_final_examples == num_examples:
        raise ValueError(
            f"Error writing the dataset, wrote {num_final_examples} examples but should have written {num_examples}."
        )

    dataset = datasets.Dataset.from_file(filename=dataset_path, info=datasets.DatasetInfo(features=features))

    return dataset
