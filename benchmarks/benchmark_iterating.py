import json
import os
import tempfile

from utils import generate_example_dataset, get_duration

import datasets


SPEED_TEST_N_EXAMPLES = 50_000
SMALL_TEST = 5_000

RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


@get_duration
def read(dataset: datasets.Dataset, length):
    for i in range(length):
        _ = dataset[i]


@get_duration
def read_batch(dataset: datasets.Dataset, length, batch_size):
    for i in range(0, len(dataset), batch_size):
        _ = dataset[i : i + batch_size]


@get_duration
def read_formatted(dataset: datasets.Dataset, length, type):
    with dataset.formatted_as(type=type):
        for i in range(length):
            _ = dataset[i]


@get_duration
def read_formatted_batch(dataset: datasets.Dataset, length, batch_size, type):
    with dataset.formatted_as(type=type):
        for i in range(0, length, batch_size):
            _ = dataset[i : i + batch_size]


def benchmark_iterating():
    times = {"num examples": SPEED_TEST_N_EXAMPLES}
    functions = [
        (read, {"length": SMALL_TEST}),
        (read, {"length": SPEED_TEST_N_EXAMPLES}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 10}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 100}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 1_000}),
        (read_formatted, {"type": "numpy", "length": SMALL_TEST}),
        (read_formatted, {"type": "pandas", "length": SMALL_TEST}),
        (read_formatted, {"type": "torch", "length": SMALL_TEST}),
        (read_formatted, {"type": "tensorflow", "length": SMALL_TEST}),
        (read_formatted_batch, {"type": "numpy", "length": SMALL_TEST, "batch_size": 10}),
        (read_formatted_batch, {"type": "numpy", "length": SMALL_TEST, "batch_size": 1_000}),
    ]

    functions_shuffled = [
        (read, {"length": SMALL_TEST}),
        (read, {"length": SPEED_TEST_N_EXAMPLES}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 10}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 100}),
        (read_batch, {"length": SPEED_TEST_N_EXAMPLES, "batch_size": 1_000}),
        (read_formatted, {"type": "numpy", "length": SMALL_TEST}),
        (read_formatted_batch, {"type": "numpy", "length": SMALL_TEST, "batch_size": 10}),
        (read_formatted_batch, {"type": "numpy", "length": SMALL_TEST, "batch_size": 1_000}),
    ]
    with tempfile.TemporaryDirectory() as tmp_dir:
        print("generating dataset")
        features = datasets.Features(
            {"list": datasets.Sequence(datasets.Value("float32")), "numbers": datasets.Value("float32")}
        )
        dataset = generate_example_dataset(
            os.path.join(tmp_dir, "dataset.arrow"),
            features,
            num_examples=SPEED_TEST_N_EXAMPLES,
            seq_shapes={"list": (100,)},
        )
        print("first set of iterations")
        for func, kwargs in functions:
            print(func.__name__, str(kwargs))
            times[func.__name__ + " " + " ".join(str(v) for v in kwargs.values())] = func(dataset, **kwargs)

        print("shuffling dataset")
        dataset = dataset.shuffle()
        print("Second set of iterations (after shuffling")
        for func, kwargs in functions_shuffled:
            print("shuffled ", func.__name__, str(kwargs))
            times["shuffled " + func.__name__ + " " + " ".join(str(v) for v in kwargs.values())] = func(
                dataset, **kwargs
            )

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":  # useful to run the profiler
    benchmark_iterating()
