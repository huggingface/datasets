from contextlib import nullcontext
from copy import deepcopy

import pytest

from datasets.parallel import parallel_backend
from datasets.utils.py_utils import map_nested


@pytest.mark.parametrize("backend,num_proc", [(None, 0), ("threading", 0), ("threading", -1), ("sequential", -1)])
@pytest.mark.parametrize("batch_size", [None, 0, -3])
def test_automatic_batch_size_with_nonpositive_worker_counts(backend, num_proc, batch_size):
    calls = []

    def transform(batch):
        calls.append(list(batch))
        return [value * 3 for value in batch]

    with parallel_backend(backend) if backend else nullcontext():
        actual = map_nested(transform, [1, 2, 3, 4], batched=True, batch_size=batch_size, num_proc=num_proc)

    assert actual == [3, 6, 9, 12]
    # An unspecified/nonpositive batch size requests the whole iterable when
    # the worker argument is a backend sentinel rather than a positive count.
    assert calls == [[1, 2, 3, 4]]


@pytest.mark.parametrize("values", [[], [7]])
@pytest.mark.parametrize("num_proc", [0, -1])
def test_automatic_batch_size_for_empty_and_singleton_inputs(values, num_proc):
    calls = []

    def transform(batch):
        calls.append(list(batch))
        return [value + 1 for value in batch]

    with parallel_backend("threading"):
        actual = map_nested(transform, values, batched=True, batch_size=None, num_proc=num_proc)

    assert actual == [value + 1 for value in values]
    assert calls == ([values] if values else [])


@pytest.mark.parametrize("num_proc", [0, -1, 2])
def test_automatic_batch_size_preserves_nested_training_inputs(num_proc):
    values = {"train": [1, 2, 3, 4, 5], "validation": [6, 7]}
    original = deepcopy(values)
    with parallel_backend("threading"):
        actual = map_nested(
            lambda batch: [value + 10 for value in batch],
            values,
            batched=True,
            batch_size=None,
            num_proc=num_proc,
        )

    assert actual == {"train": [11, 12, 13, 14, 15], "validation": [16, 17]}
    assert values == original


@pytest.mark.parametrize("num_proc", [1, 2])
@pytest.mark.parametrize("batch_size", [None, 2])
def test_positive_worker_counts_preserve_batch_boundaries(num_proc, batch_size):
    calls = []

    def transform(batch):
        calls.append(list(batch))
        return [-value for value in batch]

    with parallel_backend("threading"):
        actual = map_nested(transform, [1, 2, 3, 4, 5], batched=True, batch_size=batch_size, num_proc=num_proc)

    assert actual == [-1, -2, -3, -4, -5]
    expected_size = batch_size or (5 + num_proc - 1) // num_proc
    assert sorted(calls) == [[1, 2, 3, 4, 5][start : start + expected_size] for start in range(0, 5, expected_size)]


@pytest.mark.parametrize("num_proc", [0, -1])
def test_explicit_batch_size_with_nonpositive_worker_counts(num_proc):
    with parallel_backend("threading"):
        actual = map_nested(
            lambda batch: [value * 3 for value in batch],
            [1, 2, 3, 4],
            batched=True,
            batch_size=2,
            num_proc=num_proc,
        )
    assert actual == [3, 6, 9, 12]
