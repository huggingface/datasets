import io
import subprocess
import sys
import textwrap

import pyarrow as pa
import pyarrow.dataset as pa_ds
import pyarrow.parquet as pq
import pytest

from datasets import load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.parquet import parquet as parquet_module
from datasets.packaged_modules.parquet.parquet import Parquet, ParquetConfig


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


@pytest.mark.parametrize("termination", ["exhaust", "close", "error"])
@pytest.mark.parametrize("pre_buffer", [False, True])
def test_parquet_scan_cleanup(multi_row_groups_parquet_path, monkeypatch, termination, pre_buffer):
    builder = Parquet(batch_size=1, fragment_scan_options=pa_ds.ParquetFragmentScanOptions(pre_buffer=pre_buffer))
    read_ranges = []

    class TrackedFile(io.BytesIO):
        def read(self, size=-1):
            start = self.tell()
            data = super().read(size)
            read_ranges.append((start, start + len(data)))
            return data

    with open(multi_row_groups_parquet_path, "rb") as source:
        first_group = pq.read_metadata(source).row_group(0)
        source.seek(0)
        data = source.read()
    group_end = max(
        (column.dictionary_page_offset or column.data_page_offset) + column.total_compressed_size
        for column in (first_group.column(i) for i in range(first_group.num_columns))
    )
    source = TrackedFile(data)
    monkeypatch.setattr(parquet_module, "open", lambda *args: source, raising=False)
    tables = builder._generate_tables([multi_row_groups_parquet_path], [None])
    try:
        assert next(tables)[1].num_rows == 1
        # The first read loads the footer; data reads must stay within the current row group.
        assert all(end <= group_end for _, end in read_ranges[1:])
        if termination == "close":
            tables.close()
        elif termination == "error":
            error = RuntimeError("scan interrupted")
            with pytest.raises(RuntimeError) as exc_info:
                tables.throw(error)
            assert exc_info.value is error
        else:
            list(tables)
        assert source.closed
    finally:
        tables.close()


def test_parquet_streaming_shutdown(tmp_path):
    path = tmp_path / "data.parquet"
    pq.write_table(
        pa.table({"data": [b"x" * (1 << 20)] * 16}), path, row_group_size=1, compression=None, use_dictionary=False
    )
    script = textwrap.dedent(
        """
        import io
        import sys
        import threading
        import time

        import pyarrow as pa
        import pyarrow.dataset as ds
        from datasets import load_dataset
        from datasets.packaged_modules.parquet import parquet

        pending = threading.Event()

        class SlowFile(io.BufferedReader):
            def read(self, size=-1):
                later_group = size > 65536 and self.tell() > 1 << 20
                if later_group:
                    pending.set()
                    time.sleep(0.3)
                try:
                    return super().read(size)
                finally:
                    if later_group:
                        pending.clear()

        options = ds.ParquetFragmentScanOptions(
            cache_options=pa.CacheOptions(prefetch_limit=8, range_size_limit=1 << 20)
        )
        builder = parquet.Parquet(batch_size=1, fragment_scan_options=options)
        parquet.open = lambda path, mode: SlowFile(io.FileIO(path, mode))
        tables = builder._generate_tables([sys.argv[1]], [None])
        assert next(tables)[1].num_rows == 1
        pending.wait(0.1)
        tables.close()
        assert not pending.is_set(), "Parquet reads still running after close"

        dataset = load_dataset(
            "parquet", data_files=sys.argv[1], streaming=True, split="train", batch_size=1,
            fragment_scan_options=options,
        ).shuffle(seed=0, buffer_size=2)
        iterator = dataset.iter(batch_size=1)
        next(iterator)
        iterator.close()
        """
    )
    result = subprocess.run([sys.executable, "-c", script, str(path)], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert "Exception ignored" not in result.stderr


@pytest.mark.parametrize("threshold, expected_batches", [(4, [[5], [6, 7, 8]]), (10, [[]])])
def test_parquet_filtered_batches(tmp_path, threshold, expected_batches):
    path = str(tmp_path / "data.parquet")
    pq.write_table(pa.table({"value": range(9)}), path, row_group_size=3)
    builder = Parquet(batch_size=4, filters=[("value", ">", threshold)])
    batches = [
        (key.item_or_batch_id, table["value"].to_pylist()) for key, table in builder._generate_tables([path], [None])
    ]
    assert batches == list(enumerate(expected_batches))


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
