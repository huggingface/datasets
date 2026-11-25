import subprocess
import sys

import pytest

from datasets import load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.parquet.parquet import ParquetConfig


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


def test_parquet_streaming_without_threads_exits_cleanly(multi_row_groups_parquet_path, tmp_path):
    # code holds the script passed to python -c so we can check for crashes at interpreter shutdown.
    # Background reads can outlive the stream and access Python while the interpreter is finalizing.
    code = """\
import io
import sys
import time

import pyarrow.dataset as ds
import datasets
from datasets.packaged_modules.parquet import parquet

class SlowFile(io.BufferedReader):
    finished = False

    def read(self, size=-1):
        SlowFile.finished = False
        time.sleep(0.5)
        result = super().read(size)
        SlowFile.finished = True
        return result

dataset = datasets.load_dataset(
    "parquet", data_files=sys.argv[1], split="train", streaming=True,
    cache_dir=sys.argv[2], use_threads=False,
    fragment_scan_options=ds.ParquetFragmentScanOptions(pre_buffer=False),
)
parquet.open = lambda path, mode="rb": SlowFile(io.FileIO(path, mode))
datasets.config.SLEEP_TIME_ON_THREADS_SHUTDOWN = 0
assert len(list(dataset.shuffle(seed=42, buffer_size=1).take(1))) == 1
assert SlowFile.finished, "Read still running after iterator cleanup"
"""
    command = [sys.executable, "-c", code, multi_row_groups_parquet_path, str(tmp_path)]
    subprocess.run(command, check=True, timeout=30)
