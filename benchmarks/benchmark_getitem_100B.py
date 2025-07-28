import json
import os
from dataclasses import dataclass

import numpy as np
import pyarrow as pa

import datasets
from utils import get_duration


SPEED_TEST_N_EXAMPLES = 100_000_000_000
SPEED_TEST_CHUNK_SIZE = 10_000

RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


def generate_100B_dataset(num_examples: int, chunk_size: int) -> datasets.Dataset:
    table = pa.Table.from_pydict({"col": [0] * chunk_size})
    table = pa.concat_tables([table] * (num_examples // chunk_size))
    return datasets.Dataset(table, fingerprint="table_100B")


@dataclass
class RandIter:
    low: int
    high: int
    size: int
    seed: int

    def __post_init__(self):
        rng = np.random.default_rng(self.seed)
        self._sampled_values = rng.integers(low=self.low, high=self.high, size=self.size).tolist()

    def __iter__(self):
        return iter(self._sampled_values)

    def __len__(self):
        return self.size


@get_duration
def get_first_row(dataset: datasets.Dataset):
    _ = dataset[0]


@get_duration
def get_last_row(dataset: datasets.Dataset):
    _ = dataset[-1]


@get_duration
def get_batch_of_1024_rows(dataset: datasets.Dataset):
    _ = dataset[range(len(dataset) // 2, len(dataset) // 2 + 1024)]


@get_duration
def get_batch_of_1024_random_rows(dataset: datasets.Dataset):
    _ = dataset[RandIter(0, len(dataset), 1024, seed=42)]


def benchmark_table_100B():
    times = {"num examples": SPEED_TEST_N_EXAMPLES}
    functions = (get_first_row, get_last_row, get_batch_of_1024_rows, get_batch_of_1024_random_rows)
    print("generating dataset")
    dataset = generate_100B_dataset(num_examples=SPEED_TEST_N_EXAMPLES, chunk_size=SPEED_TEST_CHUNK_SIZE)
    print("Functions")
    for func in functions:
        print(func.__name__)
        times[func.__name__] = func(dataset)

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":  # useful to run the profiler
    benchmark_table_100B()
