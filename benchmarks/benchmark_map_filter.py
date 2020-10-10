import json
import os
import tempfile

import transformers
from utils import generate_example_dataset, get_duration

import datasets


SPEED_TEST_N_EXAMPLES = 500_000

RESULTS_BASEPATH, RESULTS_FILENAME = os.path.split(__file__)
RESULTS_FILE_PATH = os.path.join(RESULTS_BASEPATH, "results", RESULTS_FILENAME.replace(".py", ".json"))


@get_duration
def map(dataset: datasets.Dataset, **kwargs):
    _ = dataset.map(**kwargs)


@get_duration
def filter(dataset: datasets.Dataset, **kwargs):
    _ = dataset.filter(**kwargs)


def benchmark_map_filter():
    times = {"num examples": SPEED_TEST_N_EXAMPLES}
    with tempfile.TemporaryDirectory() as tmp_dir:
        features = datasets.Features({"text": datasets.Value("string"), "numbers": datasets.Value("float32")})
        dataset = generate_example_dataset(
            os.path.join(tmp_dir, "dataset.arrow"), features, num_examples=SPEED_TEST_N_EXAMPLES
        )

        tokenizer = transformers.AutoTokenizer.from_pretrained("bert-base-cased", use_fast=True)

        def tokenize(examples):
            return tokenizer(examples["text"])

        times["map identity"] = map(dataset)

        times["map identity batched"] = map(dataset, batched=True)

        times["map no-op batched"] = map(dataset, function=lambda x: None, batched=True)

        with dataset.formatted_as(type="numpy"):
            times["map no-op batched numpy"] = map(dataset, function=lambda x: None, batched=True)

        with dataset.formatted_as(type="pandas"):
            times["map no-op batched pandas"] = map(dataset, function=lambda x: None, batched=True)

        with dataset.formatted_as(type="torch", columns="numbers"):
            times["map no-op batched pytorch"] = map(dataset, function=lambda x: None, batched=True)

        with dataset.formatted_as(type="tensorflow", columns="numbers"):
            times["map no-op batched tensorflow"] = map(dataset, function=lambda x: None, batched=True)

        times["map fast-tokenizer batched"] = map(dataset, function=tokenize, batched=True)

        times["filter"] = filter(dataset)

        # Activate later when tokenizer support batched inputs
        # with dataset.formatted_as(type='numpy'):
        #     times[func.__name__ + " fast-tokenizer batched numpy"] = func(dataset, function=tokenize, batched=True)

    with open(RESULTS_FILE_PATH, "wb") as f:
        f.write(json.dumps(times).encode("utf-8"))


if __name__ == "__main__":  # useful to run the profiler
    benchmark_map_filter()
