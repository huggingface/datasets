from itertools import islice

import numpy as np
import pytest

from datasets.iterable_dataset import (
    BufferShuffledExamplesIterable,
    CyclingMultiSourcesExamplesIterable,
    ExamplesIterable,
    IterableDataset,
    MappedExamplesIterable,
    RandomlyCyclingMultiSourcesExamplesIterable,
    iterable_dataset,
)


@pytest.fixture
def generate_examples_fn():
    def generate_examples_fn(**kwargs):
        n = kwargs.pop("n", 3)
        filepaths = kwargs.pop("filepaths", ["0.txt"])
        for filepath in filepaths:
            for i in range(n):
                yield f"{filepath}_{i}", {"id": i, "filepath": filepath, **kwargs}

    return generate_examples_fn


def test_examples_iterable(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {})
    expected = list(generate_examples_fn())
    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected


def test_examples_iterable_with_kwargs(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"], "split": "train"})
    expected = list(generate_examples_fn(filepaths=["0.txt", "1.txt"], split="train"))
    assert list(ex_iterable) == expected
    assert all("split" in ex for _, ex in ex_iterable)
    assert sorted(set(ex["filepath"] for _, ex in ex_iterable)) == ["0.txt", "1.txt"]


def test_examples_iterable_shuffle(generate_examples_fn):
    ex_iterable = ExamplesIterable(generate_examples_fn, {"filepaths": ["0.txt", "1.txt"]})
    ex_iterable = ex_iterable.shuffle(42)
    expected = list(generate_examples_fn(filepaths=["1.txt", "0.txt"]))  # shuffle the filepaths
    assert list(ex_iterable) == expected


def test_buffer_shuffled_examples_iterable(generate_examples_fn):
    n, buffer_size, seed = 100, 30, 42
    rng = np.random.default_rng(seed)
    expected_indices_used_for_shuffling = list(
        islice(BufferShuffledExamplesIterable._iter_random_indices(rng, buffer_size=buffer_size), n - buffer_size)
    )
    # indices to pick in the shuffle buffer should all be in the right range
    assert all(0 <= index_to_pick < buffer_size for index_to_pick in expected_indices_used_for_shuffling)
    # it should be random indices
    assert expected_indices_used_for_shuffling != list(range(buffer_size))

    base_ex_iterable = ExamplesIterable(generate_examples_fn, {"n": n})
    ex_iterable = BufferShuffledExamplesIterable(base_ex_iterable, buffer_size=buffer_size, seed=seed)

    # The final order of examples is the result of a shuffle buffer.
    all_examples = list(generate_examples_fn(n=n))
    # We create a buffer and we pick random examples from it.
    buffer, rest = all_examples[:buffer_size], all_examples[buffer_size:]
    expected = []
    for i, index_to_pick in enumerate(expected_indices_used_for_shuffling):
        expected.append(buffer[index_to_pick])
        # The picked examples are directly replaced by the next examples from the iterable.
        buffer[index_to_pick] = rest.pop(0)
    # Once we have reached the end of the iterable, we shuffle the buffer and return the remaining examples.
    rng.shuffle(buffer)
    expected += buffer

    assert next(iter(ex_iterable)) == expected[0]
    assert list(ex_iterable) == expected
    assert sorted(list(ex_iterable)) == sorted(all_examples)
