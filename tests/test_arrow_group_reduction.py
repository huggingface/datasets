import tracemalloc

import numpy as np
import pyarrow as pa
import pytest

from datasets import Dataset
from datasets.table import _batch_accumulate_arrow_table_by_columns


@pytest.mark.parametrize("streaming", [False, True])
@pytest.mark.parametrize(
    "keys,other,columns,expected",
    [
        (["A"] * 8, [0] * 8, "key", [list(range(8))]),
        ([None] * 8, [0] * 8, "key", [list(range(8))]),
        ([1] * 5 + [2] * 3, [0] * 8, "key", [list(range(5)), [5, 6, 7]]),
        (["A"] * 5 + [None] * 3, [0] * 8, "key", [list(range(5)), [5, 6, 7]]),
        ([None] * 5 + ["A"] * 3, [0] * 8, "key", [list(range(5)), [5, 6, 7]]),
        (
            [1] * 8,
            [None] * 5 + [2] * 3,
            ["key", "other"],
            [list(range(5)), [5, 6, 7]],
        ),
        ([True] * 3 + [False] * 3 + [True] * 2, [0] * 8, "key", [[0, 1, 2], [3, 4, 5], [6, 7]]),
        ([1.0] * 5 + [float("nan")] * 3, [0] * 8, "key", [list(range(5)), [5], [6], [7]]),
    ],
)
def test_group_reduction_keeps_native_batches(streaming, keys, other, columns, expected):
    dataset = Dataset.from_dict({"key": keys, "other": other, "id": list(range(8))})
    source = dataset.to_iterable_dataset() if streaming else dataset

    actual = list(source.batch(by_column=columns, batch_size=2))

    assert [batch["id"] for batch in actual] == expected
    assert [item for batch in actual for item in batch["id"]] == list(range(8))
    assert dataset["id"] == list(range(8))


@pytest.mark.parametrize("different", [False, True])
@pytest.mark.parametrize("nullable", [False, True])
def test_group_reduction_handles_chunked_arrow_keys(different, nullable):
    value = None if nullable else "same"
    keys = pa.chunked_array(
        [
            pa.array([value] * 3, type=pa.string()),
            pa.array([value, "other" if different else value], type=pa.string()),
        ]
    )
    incoming = pa.table({"key": keys, "id": [1, 2, 3, 4, 5]})
    previous = pa.table({"key": pa.array([value], type=pa.string()), "id": [0]})
    accumulator = [previous]

    result = _batch_accumulate_arrow_table_by_columns(incoming, range(1, 6), ["key"], accumulator, None)

    if different:
        assert result["id"].to_pylist() == [[0, 1, 2, 3, 4]]
        assert pa.concat_tables(accumulator)["id"].to_pylist() == [5]
    else:
        assert len(result) == 0
        assert accumulator == [previous, incoming]
    assert incoming["id"].to_pylist() == [1, 2, 3, 4, 5]


@pytest.mark.parametrize("nullable", [False, True])
def test_group_reduction_does_not_materialize_python_boolean_columns(nullable):
    size = 200_000
    keys = pa.nulls(size) if nullable else pa.array(np.ones(size, dtype=np.int64))
    incoming = pa.table({"key": keys, "id": np.arange(size)})
    accumulator = [incoming.slice(0, 1)]
    # Initialize the Arrow kernels before measuring Python allocations.
    _batch_accumulate_arrow_table_by_columns(incoming.slice(0, 2), range(2), ["key"], [], None)

    tracemalloc.start()
    try:
        result = _batch_accumulate_arrow_table_by_columns(incoming, range(size), ["key"], accumulator, None)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert len(result) == 0
    assert accumulator[-1] is incoming
    # A Python pointer for every comparison would exceed 1.5 MB on 64-bit Python.
    assert peak < 500_000
