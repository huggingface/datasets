import json
import os
import tempfile

from utils import generate_examples, get_duration

import datasets
from datasets.arrow_writer import ArrowWriter
from datasets.features import Array2D


SHAPE_TEST_1 = (30, 487)
SHAPE_TEST_2 = (36, 1024)
SPEED_TEST_SHAPE = (100, 100)
SPEED_TEST_N_EXAMPLES = 100

DEFAULT_FEATURES = datasets.Features(
    {"text": Array2D(SHAPE_TEST_1, dtype="float32"), "image": Array2D(SHAPE_TEST_2, dtype="float32")}
)

RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


@get_duration
def write(my_features, dummy_data, tmp_dir):
    writer = ArrowWriter(features=my_features, path=os.path.join(tmp_dir, "beta.arrow"))
    for key, record in dummy_data:
        example = my_features.encode_example(record)
        writer.write(example)
    num_examples, num_bytes = writer.finalize()


@get_duration
def read_unformated(feats, tmp_dir):
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    for _ in dataset:
        pass


@get_duration
def read_formatted_as_numpy(feats, tmp_dir):
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    dataset.set_format("numpy")
    for _ in dataset:
        pass


@get_duration
def read_batch_unformated(feats, tmp_dir):
    batch_size = 10
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    for i in range(0, len(dataset), batch_size):
        _ = dataset[i : i + batch_size]


@get_duration
def read_batch_formatted_as_numpy(feats, tmp_dir):
    batch_size = 10
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    dataset.set_format("numpy")
    for i in range(0, len(dataset), batch_size):
        _ = dataset[i : i + batch_size]


@get_duration
def read_col_unformated(feats, tmp_dir):
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    for col in feats:
        _ = dataset[col]


@get_duration
def read_col_formatted_as_numpy(feats, tmp_dir):
    dataset = datasets.Dataset.from_file(
        filename=os.path.join(tmp_dir, "beta.arrow"), info=datasets.DatasetInfo(features=feats)
    )
    dataset.set_format("numpy")
    for col in feats:
        _ = dataset[col]


def benchmark_array_xd():
    times = {}
    read_functions = (
        read_unformated,
        read_formatted_as_numpy,
        read_batch_unformated,
        read_batch_formatted_as_numpy,
        read_col_unformated,
        read_col_formatted_as_numpy,
    )
    with tempfile.TemporaryDirectory() as tmp_dir:
        feats = datasets.Features({"image": Array2D(SPEED_TEST_SHAPE, dtype="float32")})
        data = generate_examples(features=feats, num_examples=SPEED_TEST_N_EXAMPLES)
        times["write_array2d"] = write(feats, data, tmp_dir)
        for read_func in read_functions:
            times[read_func.__name__ + " after write_array2d"] = read_func(feats, tmp_dir)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # don't use fixed length for fair comparison
        # feats = datasets.Features(
        #     {"image": datasets.Sequence(datasets.Sequence(datasets.Value("float32"), SPEED_TEST_SHAPE[1]), SPEED_TEST_SHAPE[0])}
        # )
        feats = datasets.Features({"image": datasets.Sequence(datasets.Sequence(datasets.Value("float32")))})
        data = generate_examples(
            features=feats, num_examples=SPEED_TEST_N_EXAMPLES, seq_shapes={"image": SPEED_TEST_SHAPE}
        )
        times["write_nested_sequence"] = write(feats, data, tmp_dir)
        for read_func in read_functions:
            times[read_func.__name__ + " after write_nested_sequence"] = read_func(feats, tmp_dir)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # don't use fixed length for fair comparison
        # feats = datasets.Features(
        #     {"image": datasets.Sequence(datasets.Value("float32"), SPEED_TEST_SHAPE[0] * SPEED_TEST_SHAPE[1])}
        # )
        feats = datasets.Features({"image": datasets.Sequence(datasets.Value("float32"))})
        data = generate_examples(
            features=feats,
            num_examples=SPEED_TEST_N_EXAMPLES,
            seq_shapes={"image": [SPEED_TEST_SHAPE[0] * SPEED_TEST_SHAPE[1]]},
        )
        times["write_flattened_sequence"] = write(feats, data, tmp_dir)
        for read_func in read_functions:
            times[read_func.__name__ + " after write_flattened_sequence"] = read_func(feats, tmp_dir)

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":  # useful to run the profiler
    benchmark_array_xd()
