from copy import deepcopy

import pyarrow as pa
import pyarrow.dataset as pds
import pyarrow.parquet as pq
import pytest

from datasets import Features, Value, concatenate_datasets, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.distributed import split_dataset_by_node
from datasets.iterable_dataset import SkipExamplesIterable
from datasets.packaged_modules.parquet.parquet import ParquetConfig

from ..utils import require_torch


@pytest.fixture
def parquet_skip_paths(tmp_path):
    files = []
    for i, values in enumerate([range(6), range(6, 11), range(11, 15)]):
        path = tmp_path / f"{i}.parquet"
        pq.write_table(pa.table({"id": values}), path, row_group_size=2)
        files.append(str(path))
    return files


@pytest.fixture(
    params=[(False, None), (False, "arrow"), (True, None), (True, "arrow")],
    ids=["files-python", "files-arrow", "row-groups-python", "row-groups-arrow"],
)
def parquet_stream(request, parquet_skip_paths):
    # Unequal file lengths and a partial final row group exercise both source granularities.
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    reshard, formatting = request.param
    if reshard:
        dataset = dataset.reshard()
    return dataset.with_format(formatting)


def _parquet_stream_ids(examples):
    return [
        row["id"]
        for example in examples
        for row in (example.to_pylist() if isinstance(example, pa.Table) else [example])
    ]


def test_parquet_stream_skip_boundaries(parquet_stream):
    # Before, at, and after row-group/file boundaries; the last two skips exhaust the stream.
    for n in [0, 1, 2, 3, 5, 6, 7, 10, 11, 12, 14, 15, 16]:
        assert _parquet_stream_ids(parquet_stream.skip(n)) == list(range(n, 15)), n


@pytest.mark.parametrize("consumed", [1, 5], ids=["first-retained-row", "across-file-boundary"])
def test_parquet_stream_skip_resume(parquet_stream, consumed):
    # Skip a whole file and part of a row group before saving progress.
    dataset = parquet_stream.skip(7)
    iterator = iter(dataset)
    prefix = [next(iterator) for _ in range(consumed)]
    state = deepcopy(dataset.state_dict())
    remaining = _parquet_stream_ids(iterator)

    restored = parquet_stream.skip(7)
    restored.load_state_dict(state)
    assert _parquet_stream_ids(prefix) == list(range(7, 7 + consumed))
    assert remaining == list(range(7 + consumed, 15))
    assert _parquet_stream_ids(restored) == remaining


@pytest.mark.parametrize("consumed_batches", [0, 1, 3])
def test_parquet_stream_skip_resume_batches(parquet_stream, consumed_batches):
    def batch_ids(batches):
        return [
            value
            for batch in batches
            for value in (batch["id"].to_pylist() if isinstance(batch, pa.Table) else batch["id"])
        ]

    dataset = parquet_stream.skip(7)
    iterator = dataset.iter(batch_size=3)
    prefix = [next(iterator) for _ in range(consumed_batches)]
    # Force exhaustion for the checkpoint after the final partial batch.
    if consumed_batches == 3:
        assert next(iterator, None) is None
    state = deepcopy(dataset.state_dict())
    tail = batch_ids(iterator)
    restored = parquet_stream.skip(7)
    restored.load_state_dict(state)
    assert batch_ids(prefix) + tail == list(range(7, 15))
    assert batch_ids(restored.iter(batch_size=3)) == tail


def test_parquet_stream_skip_repeated_epochs(parquet_stream):
    dataset = parquet_stream.skip(7)
    for epoch in [0, 1, 1, 2, 0]:
        dataset.set_epoch(epoch)
        assert _parquet_stream_ids(dataset) == list(range(7, 15)), epoch


@pytest.mark.parametrize("n, expected_decoded", [(7, 2), (15, 0), (16, 0)])
def test_parquet_stream_skip_does_not_decode_complete_sources(parquet_stream, monkeypatch, n, expected_decoded):
    source = parquet_stream._ex_iterable
    generate_tables = source.generate_tables_fn
    decoded = []

    def counted_tables(**kwargs):
        for key, table in generate_tables(**kwargs):
            decoded.append(len(table))
            yield key, table

    monkeypatch.setattr(source, "generate_tables_fn", counted_tables)
    iterator = iter(parquet_stream.skip(n))
    first = next(iterator, None)
    assert _parquet_stream_ids([] if first is None else [first]) == ([n] if n < 15 else [])
    assert sum(decoded) == expected_decoded


def test_parquet_skip_selected_row_groups(parquet_skip_paths):
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    source = dataset._ex_iterable
    source.kwargs = {"files": parquet_skip_paths, "row_groups_list": [(1, 2), (1,), ()]}
    assert list(source.generate_num_examples_fn(**source.kwargs)) == [4, 2, 0]
    expected = [2, 3, 4, 5, 8, 9]
    for n in [0, 3, 4, 5, 6, 7]:
        assert _parquet_stream_ids(dataset.skip(n)) == expected[n:]


@pytest.mark.parametrize("operation", ["map", "filter", "shuffle"])
def test_parquet_skip_transformed_input_falls_back(parquet_stream, monkeypatch, operation):
    def must_not_count(**kwargs):
        pytest.fail("Transformed inputs must use the scan path")

    monkeypatch.setattr(parquet_stream._ex_iterable, "generate_num_examples_fn", must_not_count)
    dataset = parquet_stream.with_format(None)
    if operation == "map":
        dataset = dataset.map(lambda row: {"id": row["id"] * 2})
    elif operation == "filter":
        dataset = dataset.filter(lambda row: row["id"] % 2 == 0)
    else:
        dataset = dataset.shuffle(seed=42, buffer_size=4)
    expected = _parquet_stream_ids(dataset)
    assert _parquet_stream_ids(dataset.skip(7)) == expected[7:]


@pytest.mark.parametrize(
    "config",
    [
        {"filters": [("id", ">", 3)]},
        {"columns": ["id"]},
        {"features": Features({"id": Value("float64")})},
        {"on_bad_files": "skip"},
        {"on_bad_files": "warn"},
        {"fragment_scan_options": pds.ParquetFragmentScanOptions(page_checksum_verification=True)},
    ],
)
def test_parquet_skip_config_falls_back(parquet_skip_paths, monkeypatch, config):
    from datasets.packaged_modules.parquet.parquet import Parquet

    def must_not_count(*args, **kwargs):
        pytest.fail("Unsupported configurations must use the scan path")

    monkeypatch.setattr(Parquet, "_generate_num_examples", must_not_count)
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True, **config)
    assert _parquet_stream_ids(dataset.skip(7)) == _parquet_stream_ids(dataset)[7:]


def test_parquet_skip_restored_state_falls_back(parquet_stream, monkeypatch):
    dataset = parquet_stream.skip(7)
    iterator = iter(dataset)
    next(iterator)
    state = deepcopy(dataset.state_dict())

    def must_not_count(**kwargs):
        pytest.fail("Checkpoint replay must use the scan path")

    monkeypatch.setattr(parquet_stream._ex_iterable, "generate_num_examples_fn", must_not_count)
    restored = parquet_stream.skip(7)
    restored.load_state_dict(state)
    assert _parquet_stream_ids(restored) == list(range(8, 15))


def test_parquet_skip_progressed_source_falls_back(parquet_stream, monkeypatch):
    source = parquet_stream._ex_iterable
    source._init_state_dict()
    iterator = iter(source)
    assert next(iterator)[1]["id"] == 0
    iterator.close()

    def must_not_count(**kwargs):
        pytest.fail("An already progressed source must use the scan path")

    monkeypatch.setattr(source, "generate_num_examples_fn", must_not_count)
    assert [row["id"] for _, row in SkipExamplesIterable(source, 7)] == list(range(8, 15))


def test_parquet_skip_concatenated_restore_falls_back(parquet_stream, monkeypatch):
    dataset = concatenate_datasets([parquet_stream.skip(7), parquet_stream.skip(7)])
    iterator = iter(dataset)
    next(iterator)
    state = deepcopy(dataset.state_dict())

    def must_not_count(**kwargs):
        pytest.fail("Restored children must use the scan path, including an unvisited child")

    monkeypatch.setattr(parquet_stream._ex_iterable, "generate_num_examples_fn", must_not_count)
    restored = concatenate_datasets([parquet_stream.skip(7), parquet_stream.skip(7)])
    restored.load_state_dict(state)
    assert _parquet_stream_ids(restored) == list(range(8, 15)) + list(range(7, 15))


@pytest.mark.parametrize("num_shards, contiguous", [(2, True), (2, False), (5, False)])
def test_parquet_skip_worker_sharding_matches_scan(parquet_stream, num_shards, contiguous):
    fast = SkipExamplesIterable(parquet_stream._ex_iterable, 7)
    slow_source = deepcopy(parquet_stream._ex_iterable)
    slow_source.generate_num_examples_fn = None
    slow = SkipExamplesIterable(slow_source, 7)
    for index in range(min(num_shards, fast.num_shards)):
        fast_worker = fast.shard_data_sources(num_shards, index, contiguous)
        slow_worker = slow.shard_data_sources(num_shards, index, contiguous)
        assert list(fast_worker) == list(slow_worker)


@require_torch
@pytest.mark.parametrize("num_workers, reshard", [(2, False), (5, False), (2, True)])
def test_parquet_skip_dataloader_matches_scan(parquet_skip_paths, num_workers, reshard):
    from torch.utils.data import DataLoader

    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    if reshard:
        dataset = dataset.reshard()
    slow = deepcopy(dataset)
    slow._ex_iterable.generate_num_examples_fn = None
    actual = sorted(_parquet_stream_ids(DataLoader(dataset.skip(7), batch_size=None, num_workers=num_workers)))
    expected = sorted(_parquet_stream_ids(DataLoader(slow.skip(7), batch_size=None, num_workers=num_workers)))
    assert actual == expected


@pytest.mark.parametrize("world_size, skip_first", [(2, True), (3, True), (2, False), (3, False)])
def test_parquet_skip_distributed_matches_scan(parquet_stream, world_size, skip_first):
    slow = deepcopy(parquet_stream)
    slow._ex_iterable.generate_num_examples_fn = None
    for rank in range(world_size):

        def prepare(dataset):
            if skip_first:
                dataset = dataset.skip(7)
            dataset = split_dataset_by_node(dataset, rank=rank, world_size=world_size)
            return dataset if skip_first else dataset.skip(7)

        assert _parquet_stream_ids(prepare(parquet_stream)) == _parquet_stream_ids(prepare(slow))


def test_parquet_skip_unknown_metadata(parquet_stream, monkeypatch):
    original = pq.read_metadata
    calls = []

    def unavailable(file, *args, **kwargs):
        calls.append(file.name)
        if file.name.endswith("1.parquet"):
            raise OSError("metadata unavailable")
        return original(file, *args, **kwargs)

    monkeypatch.setattr(pq, "read_metadata", unavailable)
    assert _parquet_stream_ids(parquet_stream.skip(12)) == [12, 13, 14]
    assert calls[-1].endswith("1.parquet")


def test_parquet_skip_reuses_footer_after_resharding(parquet_skip_paths, monkeypatch):
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True).reshard()
    original = pq.read_metadata
    calls = []

    def counted(file, *args, **kwargs):
        calls.append(file.name)
        return original(file, *args, **kwargs)

    monkeypatch.setattr(pq, "read_metadata", counted)
    assert _parquet_stream_ids(dataset.skip(16)) == []
    assert calls == parquet_skip_paths
    assert _parquet_stream_ids(dataset.skip(0)) == list(range(15))
    assert calls == parquet_skip_paths


@pytest.mark.parametrize("groups", [[], [0], [0, 2], [2, 0, 2]])
def test_parquet_skip_empty_sources_preserves_baseline(tmp_path, groups):
    path = tmp_path / "empty.parquet"
    with pq.ParquetWriter(path, pa.schema([("id", pa.int64())])) as writer:
        for size in groups:
            writer.write_table(pa.table({"id": pa.array(range(size), type=pa.int64())}))
    dataset = load_dataset("parquet", data_files=str(path), split="train", streaming=True)
    if groups and groups[0] == 0:
        # Existing main behavior, owned by #8742; metadata skipping must not hide it.
        with pytest.raises(pa.ArrowInvalid, match="BatchSize must be greater than 0"):
            list(dataset.skip(10))
    else:
        assert list(dataset.skip(10)) == []


def test_parquet_skip_required_fields(parquet_skip_paths, monkeypatch):
    schema = pa.schema([pa.field("id", pa.int64(), nullable=False)])
    pq.write_table(pa.Table.from_arrays([pa.array(range(6))], schema=schema), parquet_skip_paths[0], row_group_size=2)
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    source = dataset._ex_iterable
    assert sum(source.generate_num_examples_fn(**source.kwargs)) == 15
    original = source.generate_tables_fn
    scanned = []

    def tables(**kwargs):
        scanned.extend(kwargs["files"])
        yield from original(**kwargs)

    monkeypatch.setattr(source, "generate_tables_fn", tables)
    assert _parquet_stream_ids(dataset.skip(7)) == list(range(7, 15))
    assert parquet_skip_paths[0] not in scanned


def test_parquet_skip_schema_change_falls_back(parquet_skip_paths, monkeypatch):
    pq.write_table(pa.table({"id": pa.array(range(6, 11), type=pa.int32())}), parquet_skip_paths[1], row_group_size=2)
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    source = dataset._ex_iterable
    counts = source.generate_num_examples_fn(**source.kwargs)
    assert next(counts) == 6
    with pytest.raises(NotImplementedError):
        next(counts)
    original = source.generate_tables_fn
    decoded = []

    def tables(**kwargs):
        for key, table in original(**kwargs):
            decoded.append(len(table))
            yield key, table

    monkeypatch.setattr(source, "generate_tables_fn", tables)
    assert next(iter(dataset.skip(12)))["id"] == 12
    assert sum(decoded) == 7  # Scan the differently typed source, then the retained batch.


def test_parquet_skip_bad_footer_still_raises(parquet_skip_paths):
    with open(parquet_skip_paths[1], "wb") as file:
        file.write(b"not a parquet footer")
    dataset = load_dataset("parquet", data_files=parquet_skip_paths, split="train", streaming=True)
    with pytest.raises(pa.ArrowInvalid):
        list(dataset.skip(15))


@pytest.mark.parametrize("selection", [(1, 0), (1, 1)])
def test_parquet_skip_noncanonical_row_groups_falls_back(tmp_path, selection):
    path = tmp_path / "groups.parquet"
    with pq.ParquetWriter(path, pa.schema([("id", pa.int64())])) as writer:
        writer.write_table(pa.table({"id": pa.array([], type=pa.int64())}))
        writer.write_table(pa.table({"id": [1, 2]}))
    dataset = load_dataset("parquet", data_files=str(path), split="train", streaming=True)
    source = dataset._ex_iterable
    source.kwargs["row_groups_list"] = [selection]
    with pytest.raises(NotImplementedError):
        list(source.generate_num_examples_fn(**source.kwargs))
    if 0 in selection:
        with pytest.raises(pa.ArrowInvalid, match="BatchSize must be greater than 0"):
            list(dataset.skip(2))
    else:
        assert list(dataset.skip(2)) == []


def test_config_raises_when_invalid_name() -> None:
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        _ = ParquetConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files) -> None:
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        _ = ParquetConfig(name="name", data_files=data_files)


def test_parquet_reshard(multi_row_groups_parquet_path):
    ds = load_dataset("parquet", data_files=multi_row_groups_parquet_path, split="train", streaming=True)
    assert ds.num_shards == 1
    expected = list(ds)
    resharded_ds = ds.reshard()
    assert resharded_ds.num_shards == 4
    assert list(resharded_ds) == expected


def test_parquet_columns(parquet_path):
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True)
    full_features = ds.features
    assert len(ds.features) == 3
    assert len(next(iter(ds))) == 3
    ds = load_dataset("parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"])
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1
    ds = load_dataset(
        "parquet", data_files=parquet_path, split="train", streaming=True, columns=["col_1"], features=full_features
    )
    assert len(ds.features) == 1
    assert len(next(iter(ds))) == 1
