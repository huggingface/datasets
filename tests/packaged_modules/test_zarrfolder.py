import os

import numpy as np
import pytest

from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.packaged_modules.zarrfolder.zarrfolder import ZarrFolder, ZarrFolderConfig, _find_zarr_roots, _parent_dir

from ..utils import require_zarr


def _create_zarr_array_on_disk(path, shape=(10, 20), dtype="float32", chunks=(5, 10)):
    import zarr

    z = zarr.open_array(str(path), mode="w", shape=shape, dtype=dtype, chunks=chunks)
    z[:] = np.zeros(shape, dtype=dtype)


class TestFindZarrRoots:
    def test_single_root(self):
        paths = [
            "/data/healthy/scan.zarr/0",
            "/data/healthy/scan.zarr/.zarray",
            "/data/healthy/scan.zarr/.zattrs",
        ]
        roots = _find_zarr_roots(paths)
        assert roots == ["/data/healthy/scan.zarr"]

    def test_multiple_roots(self):
        paths = [
            "/data/healthy/a.zarr/0",
            "/data/healthy/a.zarr/.zarray",
            "/data/diseased/b.zarr/0",
            "/data/diseased/b.zarr/.zarray",
        ]
        roots = _find_zarr_roots(paths)
        assert roots == ["/data/diseased/b.zarr", "/data/healthy/a.zarr"]

    def test_no_zarr_paths(self):
        paths = ["/data/file.txt", "/data/other.json"]
        roots = _find_zarr_roots(paths)
        assert roots == []

    def test_windows_backslash(self):
        paths = ["C:\\data\\scan.zarr\\0", "C:\\data\\scan.zarr\\.zarray"]
        roots = _find_zarr_roots(paths)
        assert roots == ["C:/data/scan.zarr"]

    def test_nested_zarr(self):
        paths = [
            "/data/group.zarr/array.zarr/0",
            "/data/group.zarr/array.zarr/.zarray",
        ]
        roots = _find_zarr_roots(paths)
        assert roots == ["/data/group.zarr"]


class TestParentDir:
    def test_simple(self):
        assert _parent_dir("/data/healthy/scan.zarr") == "healthy"

    def test_nested(self):
        assert _parent_dir("/data/genus/species/scan.zarr") == "species"

    def test_trailing_slash(self):
        assert _parent_dir("/data/healthy/scan.zarr/") == "healthy"

    def test_short_path(self):
        assert _parent_dir("scan.zarr") == ""

    def test_hf_path(self):
        assert _parent_dir("hf://datasets/user/repo/healthy/scan.zarr") == "healthy"


@require_zarr
class TestZarrFolderNoLabels:
    def test_generate_examples_no_labels(self, tmp_path):
        data_dir = tmp_path / "zarr_data"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")
        _create_zarr_array_on_disk(data_dir / "scan2.zarr")

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=True)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 2
        for idx, sample in examples:
            assert "zarr" in sample
            assert sample["zarr"].endswith(".zarr")
            assert "label" not in sample


@require_zarr
class TestZarrFolderWithLabels:
    def test_generate_examples_with_labels(self, tmp_path):
        data_dir = tmp_path / "zarr_labeled"
        data_dir.mkdir()
        healthy_dir = data_dir / "healthy"
        healthy_dir.mkdir()
        diseased_dir = data_dir / "diseased"
        diseased_dir.mkdir()
        _create_zarr_array_on_disk(healthy_dir / "scan1.zarr")
        _create_zarr_array_on_disk(diseased_dir / "scan2.zarr")

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=False, drop_metadata=True)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 2
        labels = {sample["label"] for _, sample in examples}
        assert labels == {"diseased", "healthy"}


@require_zarr
class TestZarrFolderWithMetadata:
    def test_generate_examples_with_metadata_jsonl(self, tmp_path):
        import json

        data_dir = tmp_path / "zarr_metadata"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")
        _create_zarr_array_on_disk(data_dir / "scan2.zarr")

        metadata_path = data_dir / "metadata.jsonl"
        with open(metadata_path, "w") as f:
            f.write(json.dumps({"file_name": "scan1.zarr", "caption": "first scan"}) + "\n")
            f.write(json.dumps({"file_name": "scan2.zarr", "caption": "second scan"}) + "\n")

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=True)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 2
        paths = [sample["zarr"] for _, sample in examples]
        assert any("scan1.zarr" in p for p in paths)

    def test_generate_examples_with_metadata_csv(self, tmp_path):
        import csv

        data_dir = tmp_path / "zarr_csv"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption"])
            writer.writerow(["scan1.zarr", "first scan"])

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=True)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 1


@require_zarr
class TestZarrFolderNoZarrFiles:
    def test_no_zarr_found(self, tmp_path):
        data_dir = tmp_path / "empty_data"
        data_dir.mkdir()
        (data_dir / "readme.txt").write_text("not a zarr file")

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=True)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 0


@require_zarr
class TestZarrFolderConfig:
    def test_config_defaults(self):
        config = ZarrFolderConfig(name="test")
        assert config.drop_labels is None
        assert config.drop_metadata is None

    def test_config_drop_labels(self):
        config = ZarrFolderConfig(name="test", drop_labels=True)
        assert config.drop_labels is True