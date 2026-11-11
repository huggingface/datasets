"""Regression coverage for the data transferred by multiprocessing map."""

import os

import pyarrow as pa
import pytest
from multiprocess.reduction import ForkingPickler

import datasets.arrow_dataset as arrow_dataset
from datasets import Dataset, concatenate_datasets, load_from_disk
from datasets.table import ConcatenationTable, InMemoryTable, MemoryMappedTable


@pytest.mark.parametrize("batched", [False, True])
@pytest.mark.parametrize(
    "storage",
    [
        "memory",
        "indexed",
        "filtered",
        "shuffled",
        "split",
        "concatenated",
        "concatenated_uneven",
        "concatenated_indexed",
    ],
)
def test_map_multiprocessing_transfers_only_shard_rows(monkeypatch, batched, storage):
    # Each marker occurs in exactly one input row. A shard must not serialize
    # the other shard's rows just because its Arrow buffers are shared.
    texts = [f"unique-row-{i:04d}:" + "x" * 128 for i in range(100)]
    dataset = Dataset.from_dict({"text": texts, "nested": [[i, None] for i in range(len(texts))]})
    if storage == "indexed":
        dataset = dataset.select([3, 1, 0] + list(range(4, 100)))
    elif storage == "filtered":
        dataset = dataset.filter(lambda row: row["nested"][0] % 3 != 0)
    elif storage == "shuffled":
        dataset = dataset.shuffle(seed=42)
    elif storage == "split":
        dataset = dataset.train_test_split(test_size=0.2, seed=42)["train"]
    elif storage.startswith("concatenated"):
        boundary = 50 if storage == "concatenated" else 70
        dataset = concatenate_datasets([Dataset.from_dict(dataset[:boundary]), Dataset.from_dict(dataset[boundary:])])
        assert isinstance(dataset.data, ConcatenationTable)
        if storage == "concatenated_indexed":
            dataset = dataset.select([99, 3, 1, 0, 70, 69, 99])
    expected = dataset.to_dict()
    expected["size"] = [len(text) for text in expected["text"]]
    original_buffers = dataset.data.column("text").chunk(0).buffers()
    payloads = []
    original_iflat = arrow_dataset.iflatmap_unordered

    def capture_shards(pool, func, *, kwargs_iterable):
        kwargs_iterable = list(kwargs_iterable)
        payloads.extend(bytes(ForkingPickler.dumps(job["shard"])) for job in kwargs_iterable)
        yield from original_iflat(pool, func, kwargs_iterable=kwargs_iterable)

    monkeypatch.setattr(arrow_dataset, "iflatmap_unordered", capture_shards)
    function = (
        (lambda batch: {"size": [len(text) for text in batch["text"]]})
        if batched
        else (lambda row: {"size": len(row["text"])})
    )
    result = dataset.map(function, batched=batched, num_proc=2, keep_in_memory=True)
    assert result.to_dict() == expected
    assert result.features["nested"] == dataset.features["nested"]
    assert len(payloads) == 2
    boundary = (len(dataset) + 1) // 2
    for payload, shard_texts in zip(payloads, [expected["text"][:boundary], expected["text"][boundary:]]):
        assert {text for text in texts if text.encode() in payload} == set(shard_texts)
    assert dataset.data.column("text").chunk(0).buffers() == original_buffers


@pytest.mark.parametrize("view_type", [pa.string_view(), pa.binary_view()], ids=str)
@pytest.mark.parametrize("storage", ["memory", "indexed", "concatenated"])
@pytest.mark.parametrize("container", ["scalar", "list", "struct", "list_struct"])
def test_map_multiprocessing_compacts_view_values(monkeypatch, view_type, storage, container):
    texts = [f"unique-row-{i:04d}:" + "x" * 128 for i in range(100)]
    values = texts + [None, "", "short"]
    if pa.types.is_binary_view(view_type):
        values = [value.encode() if value is not None else None for value in values]
    markers = [value.encode() if isinstance(value, str) else value for value in values]
    column_type = view_type
    if container in ("struct", "list_struct"):
        column_type = pa.struct({"value": column_type})
        values = [{"value": value} for value in values]
    if container in ("list", "list_struct"):
        column_type = pa.list_(column_type)
        values = [[value] for value in values]
    dataset = Dataset(pa.table({"text": pa.array(values, type=column_type)}))
    if storage == "indexed":
        indices = [99, 2, 100, 0, 101, 99, 102]
        dataset = dataset.select(indices)
        markers = [markers[index] for index in indices]
    elif storage == "concatenated":
        dataset = concatenate_datasets(
            [Dataset(dataset.data.table.slice(0, 70)), Dataset(dataset.data.table.slice(70))]
        )
    expected = dataset.to_dict()
    original_table, original_indices = dataset.data, dataset._indices
    dataset.set_format("arrow")
    baseline_sizes = [
        len(ForkingPickler.dumps(dataset.shard(num_shards=2, index=rank, contiguous=True))) for rank in range(2)
    ]
    payloads = []
    original_iflat = arrow_dataset.iflatmap_unordered

    def capture_shards(pool, func, *, kwargs_iterable):
        def jobs():
            for job in kwargs_iterable:
                payloads.append(bytes(ForkingPickler.dumps(job["shard"])))
                yield job

        yield from original_iflat(pool, func, kwargs_iterable=jobs())

    def add_size(batch):
        # Check the actual worker input type, including after pickling.
        assert batch.schema.field("text").type == column_type
        sizes = [len(value) if value is not None else -1 for value in batch["text"].to_pylist()]
        return batch.append_column("size", pa.array(sizes))

    monkeypatch.setattr(arrow_dataset, "iflatmap_unordered", capture_shards)
    result = dataset.map(add_size, batched=True, num_proc=2, keep_in_memory=True)
    assert result.to_dict() == {
        **expected,
        "size": [len(value) if value is not None else -1 for value in expected["text"]],
    }
    assert len(payloads) == 2
    boundary = (len(dataset) + 1) // 2
    for payload, baseline_size, shard_values, shard_markers in zip(
        payloads,
        baseline_sizes,
        [expected["text"][:boundary], expected["text"][boundary:]],
        [markers[:boundary], markers[boundary:]],
    ):
        restored = ForkingPickler.loads(payload)
        assert restored.to_dict() == {"text": shard_values}
        assert restored.data.column("text").type == column_type
        assert {text.encode() for text in texts if text.encode() in payload} == {
            text.encode() for text in texts if text.encode() in shard_markers
        }
        assert len(payload) < baseline_size
    assert dataset.data is original_table
    assert dataset._indices is original_indices


@pytest.mark.parametrize("indexed", [False, True])
def test_map_multiprocessing_keeps_mixed_concatenation_mapped(monkeypatch, tmp_path, indexed):
    texts = [f"unique-row-{i:04d}:" + "x" * 128 for i in range(100)]
    memory = Dataset.from_dict({"text": texts[:70]})
    Dataset.from_dict({"text": texts[70:]}).save_to_disk(tmp_path / "input")
    dataset = concatenate_datasets([memory, load_from_disk(tmp_path / "input")])
    if indexed:
        dataset = dataset.select([99, 3, 1, 0, 70, 69, 99])
    original_table, original_indices = dataset.data, dataset._indices
    expected = dataset.to_dict()
    original_iflat = arrow_dataset.iflatmap_unordered
    mapped_shards = []

    def capture_shards(pool, func, *, kwargs_iterable):
        def jobs():
            for job in kwargs_iterable:
                shard = job["shard"]
                payload = bytes(ForkingPickler.dumps(shard))
                restored = ForkingPickler.loads(payload)
                if shard.cache_files:
                    assert isinstance(restored.data, ConcatenationTable)
                    blocks = [block for row in restored.data.blocks for block in row]
                    assert any(isinstance(block, MemoryMappedTable) for block in blocks)
                    assert any(isinstance(block, InMemoryTable) for block in blocks)
                    assert restored.cache_files == dataset.cache_files
                    assert not any(text.encode() in payload for text in texts[70:])
                    mapped_shards.append(restored)
                yield job

        yield from original_iflat(pool, func, kwargs_iterable=jobs())

    def add_size(row):
        return {"size": len(row["text"])}

    reference = dataset.map(add_size, keep_in_memory=True)
    monkeypatch.setattr(arrow_dataset, "iflatmap_unordered", capture_shards)
    result = dataset.map(add_size, num_proc=2, keep_in_memory=True)
    assert len(mapped_shards) == (2 if indexed else 1)
    assert result.to_dict() == {**expected, "size": [144] * len(dataset)}
    assert result.features == reference.features
    assert result._fingerprint == reference._fingerprint
    assert dataset.data is original_table
    assert dataset._indices is original_indices


@pytest.mark.parametrize("storage", ["memory", "indexed", "disk"])
@pytest.mark.parametrize("format_type", [None, "numpy"])
def test_map_multiprocessing_preserves_inputs_and_fingerprint(tmp_path, storage, format_type):
    dataset = Dataset.from_dict({"text": ["one", "two", "three", "four"], "nested": [[1], None, [], [2, 3]]})
    if storage == "disk":
        dataset.save_to_disk(tmp_path / "input")
        dataset = load_from_disk(tmp_path / "input")
        assert isinstance(dataset.data, MemoryMappedTable)
    elif storage == "indexed":
        dataset = dataset.select([3, 1, 0])
    dataset.set_format(format_type, columns=["text"], output_all_columns=True)
    original_table = dataset.data
    original_indices = dataset._indices
    original_format = dataset.format
    original_data = dataset.to_dict()
    original_fingerprint = dataset._fingerprint
    # Returning nothing must preserve the dataset, including its fingerprint.
    unchanged = dataset.map(lambda row: None, num_proc=2)
    assert unchanged.to_dict() == original_data
    assert unchanged._fingerprint == original_fingerprint
    assert unchanged.format == original_format
    assert dataset.data is original_table
    assert dataset._indices is original_indices
    assert dataset.format == original_format
    assert dataset.to_dict() == original_data

    def add_size(row):
        return {"size": len(row["text"])}

    mapped = dataset.map(add_size, num_proc=2)
    expected = dataset.map(add_size)
    assert mapped.to_dict() == expected.to_dict()
    assert mapped.features == expected.features
    assert mapped.format == expected.format
    assert mapped._fingerprint == expected._fingerprint
    if storage == "disk":
        assert all(isinstance(block, MemoryMappedTable) for row in mapped.data.blocks for block in row)


@pytest.mark.parametrize("indexed", [False, True])
@pytest.mark.parametrize("error_type", [pa.ArrowNotImplementedError, TypeError])
def test_map_multiprocessing_falls_back_if_compaction_fails(monkeypatch, indexed, error_type):
    dataset = Dataset.from_dict({"text": ["one", "two", "three", "four"], "nested": [[1], None, [], [2, 3]]})
    if indexed:
        dataset = dataset.select([3, 1, 0])
    expected = dataset.to_dict()
    expected["size"] = [len(text) for text in expected["text"]]
    original_table, original_indices = dataset.data, dataset._indices
    original_concat = pa.concat_arrays
    parent_pid = os.getpid()
    failures = []

    def fail_compaction(arrays, *args, **kwargs):
        # Fail after the text column has been copied, to check atomic fallback.
        if os.getpid() == parent_pid and pa.types.is_list(arrays[0].type):
            failures.append(True)
            raise error_type("unsupported column compaction")
        return original_concat(arrays, *args, **kwargs)

    monkeypatch.setattr(pa, "concat_arrays", fail_compaction)
    result = dataset.map(lambda row: {"size": len(row["text"])}, num_proc=2)
    assert result.to_dict() == expected
    assert result.features["nested"] == dataset.features["nested"]
    assert dataset.data is original_table
    assert dataset._indices is original_indices
    assert len(failures) == 2


def test_map_multiprocessing_compacts_shards_as_jobs_are_submitted(monkeypatch):
    dataset = Dataset.from_dict({"text": ["one", "two", "three", "four"]})
    original_concat = pa.concat_arrays
    original_iflat = arrow_dataset.iflatmap_unordered
    copied_rows = []

    def capture_copy(arrays, *args, **kwargs):
        copied_rows.append(sum(len(array) for array in arrays))
        return original_concat(arrays, *args, **kwargs)

    def capture_jobs(pool, func, *, kwargs_iterable):
        assert copied_rows == []

        def jobs():
            for rank, job in enumerate(kwargs_iterable):
                assert copied_rows == [2] * (rank + 1)
                yield job

        yield from original_iflat(pool, func, kwargs_iterable=jobs())

    monkeypatch.setattr(pa, "concat_arrays", capture_copy)
    monkeypatch.setattr(arrow_dataset, "iflatmap_unordered", capture_jobs)
    result = dataset.map(lambda row: {"size": len(row["text"])}, num_proc=2)
    assert result.to_dict() == {"text": ["one", "two", "three", "four"], "size": [3, 3, 5, 4]}


def test_map_multiprocessing_keeps_chunked_nested_features():
    table = pa.table(
        {
            "text": pa.chunked_array([["one", "two"], ["three", "four"]]),
            "nested": pa.chunked_array([[[1], None], [[], [2, 3]]], type=pa.list_(pa.int64())),
        }
    )
    dataset = Dataset(table)
    result = dataset.map(lambda row: {"size": len(row["text"])}, num_proc=2)
    assert result.to_dict() == {
        "text": ["one", "two", "three", "four"],
        "nested": [[1], None, [], [2, 3]],
        "size": [3, 3, 5, 4],
    }
    assert result.features["nested"] == dataset.features["nested"]


def test_map_multiprocessing_preserves_chunks_above_offset_limit():
    # Null children need no value buffer: this exercises the 32-bit list offset
    # limit with four rows and only a few bytes of actual Arrow allocation.
    chunk = pa.ListArray.from_arrays([0, 1 << 30], pa.nulls(1 << 30))
    dataset = Dataset(pa.table({"nested": pa.chunked_array([chunk] * 4)}), fingerprint="large-list")
    result = dataset.map(lambda row: None, num_proc=2)
    assert len(result) == 4
    assert result.data.column(0).num_chunks == 4
    assert result._fingerprint == dataset._fingerprint
