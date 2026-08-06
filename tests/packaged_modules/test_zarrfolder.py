import logging
import os

import numpy as np
import pytest

from datasets.data_files import DataFilesDict, get_data_patterns
from datasets.download.streaming_download_manager import StreamingDownloadManager
from datasets.features import Features
from datasets.features.zarr import Zarr
from datasets.packaged_modules.zarrfolder.zarrfolder import (
    ZarrFolder,
    ZarrFolderConfig,
    _dirname_urlsafe,
    _discover_zarr_dirs_remote,
    _find_zarr_roots,
    _join_urlsafe,
    _parent_dir,
)

from ..utils import require_zarr


def _create_zarr_array_on_disk(path, shape=(10, 20), dtype="float32", chunks=(5, 10)):
    import zarr

    z = zarr.open_array(str(path), mode="w", shape=shape, dtype=dtype, chunks=chunks)
    z[:] = np.zeros(shape, dtype=dtype)


class TestDiscoverZarrDirsRemote:
    def test_store_root_is_single_store(self, tmp_path):
        _create_zarr_array_on_disk(tmp_path)
        url = "file:///" + str(tmp_path).replace("\\", "/")
        roots = _discover_zarr_dirs_remote(url)
        assert roots == [url.rstrip("/")]

    def test_nested_zarr_dirs(self, tmp_path):
        import zarr

        zarr.open_array(str(tmp_path / "a.zarr"), mode="w", shape=(2, 2))
        sub = tmp_path / "sub"
        sub.mkdir()
        zarr.open_array(str(sub / "b.zarr"), mode="w", shape=(2, 2))

        url = "file:///" + str(tmp_path).replace("\\", "/")
        roots = _discover_zarr_dirs_remote(url)
        assert roots == [
            url + "/a.zarr",
            url + "/sub/b.zarr",
        ]

    def test_empty_dir(self, tmp_path):
        url = "file:///" + str(tmp_path).replace("\\", "/")
        assert _discover_zarr_dirs_remote(url) == []


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


class TestUrlSafePathHelpers:
    def test_dirname_local(self):
        assert _dirname_urlsafe("C:\\data\\img.zarr\\0") == "C:\\data\\img.zarr"
        assert _dirname_urlsafe("/data/img.zarr/0") == "/data/img.zarr"

    def test_dirname_hf_url(self):
        assert _dirname_urlsafe("hf://buckets/user/bucket/img.zarr") == "hf://buckets/user/bucket"

    def test_dirname_hf_url_with_subpath(self):
        assert _dirname_urlsafe("hf://buckets/user/bucket/raw/img.zarr") == "hf://buckets/user/bucket/raw"

    def test_join_local(self):
        assert _join_urlsafe("C:\\data", "img.zarr") == os.path.join("C:\\data", "img.zarr")
        assert _join_urlsafe("/data", "img.zarr") == os.path.join("/data", "img.zarr")

    def test_join_hf_url(self):
        assert _join_urlsafe("hf://buckets/user/bucket", "img.zarr") == "hf://buckets/user/bucket/img.zarr"

    def test_join_hf_url_trailing_slash(self):
        assert _join_urlsafe("hf://buckets/user/bucket/", "img.zarr") == "hf://buckets/user/bucket/img.zarr"


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

    def test_generate_examples_with_metadata_columns(self, tmp_path):
        import csv

        data_dir = tmp_path / "zarr_meta_cols"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")
        _create_zarr_array_on_disk(data_dir / "scan2.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption", "score"])
            writer.writerow(["scan1.zarr", "first", "1.5"])
            writer.writerow(["scan2.zarr", "second", "2.5"])

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=False)
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 2
        # metadata columns are kept in the features, not silently dropped
        assert list(builder.info.features.keys()) == ["zarr", "caption", "score"]
        assert examples[0][1]["caption"] == "first"
        assert examples[0][1]["score"] == 1.5

    def test_metadata_columns_union_across_splits(self, tmp_path):
        import csv

        data_dir = tmp_path / "zarr_union"
        train_dir = data_dir / "train"
        test_dir = data_dir / "test"
        train_dir.mkdir(parents=True)
        test_dir.mkdir()
        _create_zarr_array_on_disk(train_dir / "scan1.zarr")
        _create_zarr_array_on_disk(test_dir / "scan2.zarr")

        with open(train_dir / "metadata.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption"])
            writer.writerow(["scan1.zarr", "train cap"])
        with open(test_dir / "metadata.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "score"])
            writer.writerow(["scan2.zarr", "3.0"])

        data_files = DataFilesDict(
            {
                "train": [str(train_dir / "metadata.csv"), str(train_dir / "scan1.zarr")],
                "test": [str(test_dir / "metadata.csv"), str(test_dir / "scan2.zarr")],
            }
        )
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=False)
        gen_kwargs_list = [sg.gen_kwargs for sg in builder._split_generators(StreamingDownloadManager())]
        examples = []
        for gen_kwargs in gen_kwargs_list:
            examples.extend(list(builder._generate_examples(**gen_kwargs)))
        assert len(examples) == 2
        assert set(builder.info.features.keys()) == {"zarr", "caption", "score"}
        caps = [sample["caption"] for _, sample in examples if "caption" in sample]
        scores = [sample["score"] for _, sample in examples if "score" in sample]
        assert caps == ["train cap"]
        assert scores == [3.0]

    def test_metadata_dangling_path_is_skipped_with_warning(self, tmp_path, caplog):
        import csv

        data_dir = tmp_path / "zarr_dangle"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption"])
            writer.writerow(["scan1.zarr", "ok"])
            writer.writerow(["missing.zarr", "dangling"])

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=False)
        with caplog.at_level(logging.WARNING):
            gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
            examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 1
        assert any("not found among the discovered .zarr stores" in r.message for r in caplog.records)

    def test_metadata_row_without_file_name_is_skipped_with_warning(self, tmp_path, caplog):
        import csv

        data_dir = tmp_path / "zarr_no_filename"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["caption"])
            writer.writerow(["no file_name here"])

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(data_files=data_files, drop_labels=True, drop_metadata=False)
        with caplog.at_level(logging.WARNING):
            gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
            examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 0
        assert any("without 'file_name'/'zarr_file_name'" in r.message for r in caplog.records)

    def test_metadata_unknown_column_dropped_with_warning(self, tmp_path, caplog):
        import csv

        data_dir = tmp_path / "zarr_unknown_col"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption"])
            writer.writerow(["scan1.zarr", "some caption"])

        data_files = DataFilesDict.from_patterns(get_data_patterns(str(data_dir)), str(data_dir))
        builder = ZarrFolder(
            data_files=data_files,
            features=Features({"zarr": Zarr()}),
            drop_labels=True,
            drop_metadata=False,
        )
        with caplog.at_level(logging.WARNING):
            gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
            examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 1
        assert "caption" not in examples[0][1]
        assert any("Dropping metadata column 'caption'" in r.message for r in caplog.records)

    def test_generate_examples_with_remote_metadata_url(self, tmp_path):
        import csv

        data_dir = tmp_path / "zarr_remote_meta"
        data_dir.mkdir()
        _create_zarr_array_on_disk(data_dir / "scan1.zarr")

        metadata_path = data_dir / "metadata.csv"
        with open(metadata_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["file_name", "caption"])
            writer.writerow(["scan1.zarr", "first scan"])

        # Pass the metadata file as a remote (file://) URL to exercise the
        # streaming-safe read path through xopen, and check the joined
        # store path stays a valid URL.
        from datasets.data_files import DataFilesDict, DataFilesList

        remote_meta = "file:///" + str(metadata_path).replace("\\", "/")
        remote_root = "file:///" + str(data_dir).replace("\\", "/")
        paths = [remote_root + "/scan1.zarr", remote_meta]
        data_files = DataFilesDict(
            {"train": DataFilesList(paths, [()] * len(paths))}
        )
        builder = ZarrFolder(
            data_files=data_files,
            drop_labels=True,
        )
        gen_kwargs = builder._split_generators(StreamingDownloadManager())[0].gen_kwargs
        examples = list(builder._generate_examples(**gen_kwargs))
        assert len(examples) == 1
        _, sample = examples[0]
        assert sample["caption"] == "first scan"
        assert sample["zarr"].startswith("file:///")
        assert "scan1.zarr" in sample["zarr"]


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