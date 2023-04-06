import fnmatch
import os
import tempfile
import time
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from huggingface_hub import HfApi

from datasets import (
    Audio,
    ClassLabel,
    Dataset,
    DatasetDict,
    Features,
    Image,
    Value,
    load_dataset,
    load_dataset_builder,
)
from datasets.config import METADATA_CONFIGS_FIELD
from datasets.utils.file_utils import cached_path
from datasets.utils.hub import hf_hub_url
from datasets.utils.metadata import DatasetMetadata
from tests.fixtures.hub import CI_HUB_ENDPOINT, CI_HUB_USER, CI_HUB_USER_TOKEN
from tests.utils import for_all_test_methods, require_pil, require_sndfile, xfail_if_500_502_http_error


pytestmark = pytest.mark.integration


@for_all_test_methods(xfail_if_500_502_http_error)
@pytest.mark.usefixtures("set_ci_hub_access_token", "ci_hfh_hf_hub_url")
class TestPushToHub:
    _api = HfApi(endpoint=CI_HUB_ENDPOINT)
    _token = CI_HUB_USER_TOKEN

    def test_push_dataset_dict_to_hub_no_token(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files, [".gitattributes", "README.md", "data/train-00000-of-00001-*.parquet"]
                )
            )

    def test_push_to_hub_custom_configs(self, temporary_repo):
        ds_default = Dataset.from_dict({"x": range(10), "y": range(10)})
        local_ds_default = DatasetDict({"train": ds_default})

        ds_first = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        local_ds_first = DatasetDict({"train": ds_first})

        ds_second = Dataset.from_dict({"a": ["aa", "ab"], "b": ["bb", "bc"]})
        local_ds_second = DatasetDict({"train": ds_second})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds_default.push_to_hub(ds_name)
            hub_ds_default = load_dataset(ds_name, download_mode="force_redownload")

            # test that it doesn't break existing repos...
            local_ds_first.push_to_hub(ds_name, "first")
            hub_ds_first = load_dataset(ds_name, "first", download_mode="force_redownload")
            local_ds_second.push_to_hub(ds_name, "second")
            hub_ds_second = load_dataset(ds_name, "second", download_mode="force_redownload")

            assert local_ds_default["train"].column_names == hub_ds_default["train"].column_names == ["x", "y"]
            assert local_ds_first["train"].column_names == hub_ds_first["train"].column_names == ["x", "y"]
            assert local_ds_second["train"].column_names == hub_ds_second["train"].column_names == ["a", "b"]
            # assert hub_ds_first.column_names != hub_ds_second.column_names

            assert local_ds_default["train"].features == hub_ds_default["train"].features
            assert local_ds_first["train"].features == hub_ds_first["train"].features
            assert local_ds_second["train"].features == hub_ds_second["train"].features
            assert hub_ds_first["train"].features != hub_ds_second["train"].features

            assert local_ds_default["train"].num_rows == hub_ds_default["train"].num_rows == 10
            assert local_ds_first["train"].num_rows == hub_ds_first["train"].num_rows == 3
            assert local_ds_second["train"].num_rows == hub_ds_second["train"].num_rows == 2

            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            expected_files = sorted(
                [
                    ".gitattributes",
                    "README.md",
                    "data/train-00000-of-00001-*.parquet",
                    "first/data/train-00000-of-00001-*.parquet",
                    "second/data/train-00000-of-00001-*.parquet",
                ]
            )
            assert all(fnmatch.fnmatch(file, expected_file) for file, expected_file in zip(files, expected_files))

            # check that configs args was successfully pushed to README.md
            ds_readme_path = cached_path(hf_hub_url(ds_name, "README.md"))
            dataset_metadata = DatasetMetadata.from_readme(Path(ds_readme_path))
            assert METADATA_CONFIGS_FIELD in dataset_metadata
            assert isinstance(dataset_metadata[METADATA_CONFIGS_FIELD], list)
            assert sorted(dataset_metadata[METADATA_CONFIGS_FIELD], key=lambda x: x["config_name"]) == [
                {"config_name": "default", "data_dir": "./"},
                {"config_name": "first", "data_dir": "first"},
                {"config_name": "second", "data_dir": "second"},
            ]

    def test_push_to_hub_custom_configs_custom_splits(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(100)), "y": list(range(100))})
        ds2 = Dataset.from_dict({"x": list(range(50)), "y": list(range(50))})
        ds3 = Dataset.from_dict({"x": list(range(10)), "y": list(range(10))})

        local_ds_default = DatasetDict({"train": ds, "random": ds2})
        local_ds_custom = DatasetDict({"train": ds, "random": ds3})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds_default.push_to_hub(ds_name)
            hub_ds_default = load_dataset(ds_name, download_mode="force_redownload")
            local_ds_custom.push_to_hub(ds_name, "custom")
            hub_ds_custom = load_dataset(ds_name, "custom", download_mode="force_redownload")

            assert sorted(local_ds_default) == sorted(hub_ds_default) == sorted(["train", "random"])
            assert sorted(local_ds_custom) == sorted(hub_ds_custom) == sorted(["train", "random"])

            assert local_ds_default["random"].column_names == hub_ds_default["random"].column_names
            assert list(local_ds_default["random"].features) == list(hub_ds_default["random"].features)
            assert local_ds_default["random"].features == local_ds_default["random"].features

            assert local_ds_custom["random"].column_names == hub_ds_custom["random"].column_names
            assert list(local_ds_custom["random"].features) == list(hub_ds_custom["random"].features)
            assert local_ds_custom["random"].features == hub_ds_custom["random"].features

            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            expected_files = sorted(
                [
                    ".gitattributes",
                    "README.md",
                    "data/train-00000-of-00001-*.parquet",
                    "data/random-00000-of-00001-*.parquet",
                    "custom/data/train-00000-of-00001-*.parquet",
                    "custom/data/random-00000-of-00001-*.parquet",
                ]
            )
            assert all(fnmatch.fnmatch(file, expected_file) for file, expected_file in zip(files, expected_files))

            ds_readme_path = cached_path(hf_hub_url(ds_name, "README.md"))
            dataset_metadata = DatasetMetadata.from_readme(Path(ds_readme_path))
            assert METADATA_CONFIGS_FIELD in dataset_metadata
            assert isinstance(dataset_metadata[METADATA_CONFIGS_FIELD], list)
            assert sorted(dataset_metadata[METADATA_CONFIGS_FIELD], key=lambda x: x["config_name"]) == [
                {"config_name": "custom", "data_dir": "custom"},
                {"config_name": "default", "data_dir": "./"},
            ]

    def test_push_dataset_dict_to_hub_name_without_namespace(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name.split("/")[-1], token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files, [".gitattributes", "README.md", "data/train-00000-of-00001-*.parquet"]
                )
            )

    def test_push_dataset_dict_to_hub_datasets_with_different_features(self, cleanup_repo):
        ds_train = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_test = Dataset.from_dict({"x": [True, False, True], "y": ["a", "b", "c"]})

        local_ds = DatasetDict({"train": ds_train, "test": ds_test})

        ds_name = f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}"
        try:
            with pytest.raises(ValueError):
                local_ds.push_to_hub(ds_name.split("/")[-1], token=self._token)
        except AssertionError:
            cleanup_repo(ds_name)
            raise

    def test_push_dataset_dict_to_hub_private(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, private=True)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload", use_auth_token=self._token)

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files, [".gitattributes", "README.md", "data/train-00000-of-00001-*.parquet"]
                )
            )

    def test_push_dataset_dict_to_hub(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files, [".gitattributes", "README.md", "data/train-00000-of-00001-*.parquet"]
                )
            )

    def test_push_dataset_dict_to_hub_multiple_files(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            with patch("datasets.config.MAX_SHARD_SIZE", "16KB"):
                local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files,
                    [
                        ".gitattributes",
                        "README.md",
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                    ],
                )
            )

    def test_push_dataset_dict_to_hub_multiple_files_with_max_shard_size(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, max_shard_size="16KB")
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files,
                    [
                        ".gitattributes",
                        "README.md",
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                    ],
                )
            )

    def test_push_dataset_dict_to_hub_multiple_files_with_num_shards(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, num_shards={"train": 2})
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files,
                    [
                        ".gitattributes",
                        "README.md",
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                    ],
                )
            )

    def test_push_dataset_dict_to_hub_overwrite_files(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})
        ds2 = Dataset.from_dict({"x": list(range(100)), "y": list(range(100))})

        local_ds = DatasetDict({"train": ds, "random": ds2})

        ds_name = f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}"

        # Push to hub two times, but the second time with a larger amount of files.
        # Verify that the new files contain the correct dataset.
        with temporary_repo(ds_name) as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)

            with tempfile.TemporaryDirectory() as tmp:
                # Add a file starting with "data" to ensure it doesn't get deleted.
                path = Path(tmp) / "datafile.txt"
                with open(path, "w") as f:
                    f.write("Bogus file")

                self._api.upload_file(
                    path_or_fileobj=str(path),
                    path_in_repo="datafile.txt",
                    repo_id=ds_name,
                    repo_type="dataset",
                    token=self._token,
                )

            local_ds.push_to_hub(ds_name, token=self._token, max_shard_size=500 << 5)

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))

            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files,
                    [
                        ".gitattributes",
                        "README.md",
                        "data/random-00000-of-00001-*.parquet",
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                        "datafile.txt",
                    ],
                )
            )

            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

        # Push to hub two times, but the second time with fewer files.
        # Verify that the new files contain the correct dataset and that non-necessary files have been deleted.
        with temporary_repo(ds_name) as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, max_shard_size=500 << 5)

            with tempfile.TemporaryDirectory() as tmp:
                # Add a file starting with "data" to ensure it doesn't get deleted.
                path = Path(tmp) / "datafile.txt"
                with open(path, "w") as f:
                    f.write("Bogus file")

                self._api.upload_file(
                    path_or_fileobj=str(path),
                    path_in_repo="datafile.txt",
                    repo_id=ds_name,
                    repo_type="dataset",
                    token=self._token,
                )

            local_ds.push_to_hub(ds_name, token=self._token)

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))

            assert all(
                fnmatch.fnmatch(file, expected_file)
                for file, expected_file in zip(
                    files,
                    [
                        ".gitattributes",
                        "README.md",
                        "data/random-00000-of-00001-*.parquet",
                        "data/train-00000-of-00001-*.parquet",
                        "datafile.txt",
                    ],
                )
            )

            # Keeping the "datafile.txt" breaks the load_dataset to think it's a text-based dataset
            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

    def test_push_dataset_to_hub(self, temporary_repo):
        local_ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, split="train", token=self._token)
            local_ds_dict = {"train": local_ds}
            hub_ds_dict = load_dataset(ds_name, download_mode="force_redownload")

            assert list(local_ds_dict.keys()) == list(hub_ds_dict.keys())

            for ds_split_name in local_ds_dict.keys():
                local_ds = local_ds_dict[ds_split_name]
                hub_ds = hub_ds_dict[ds_split_name]
                assert local_ds.column_names == hub_ds.column_names
                assert list(local_ds.features.keys()) == list(hub_ds.features.keys())
                assert local_ds.features == hub_ds.features

    def test_push_dataset_to_hub_custom_features(self, temporary_repo):
        features = Features({"x": Value("int64"), "y": ClassLabel(names=["neg", "pos"])})
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [0, 0, 1]}, features=features)

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

            assert ds.column_names == hub_ds.column_names
            assert list(ds.features.keys()) == list(hub_ds.features.keys())
            assert ds.features == hub_ds.features
            assert ds[:] == hub_ds[:]

    @require_sndfile
    def test_push_dataset_to_hub_custom_features_audio(self, temporary_repo):
        audio_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_audio_44100.wav")
        data = {"x": [audio_path, None], "y": [0, -1]}
        features = Features({"x": Audio(), "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
                ds.push_to_hub(ds_name, embed_external_files=embed_external_files, token=self._token)
                hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

                assert ds.column_names == hub_ds.column_names
                assert list(ds.features.keys()) == list(hub_ds.features.keys())
                assert ds.features == hub_ds.features
                np.testing.assert_equal(ds[0]["x"]["array"], hub_ds[0]["x"]["array"])
                assert ds[1] == hub_ds[1]  # don't test hub_ds[0] since audio decoding might be slightly different
                hub_ds = hub_ds.cast_column("x", Audio(decode=False))
                elem = hub_ds[0]["x"]
                path, bytes_ = elem["path"], elem["bytes"]
                assert isinstance(path, str)
                assert os.path.basename(path) == "test_audio_44100.wav"
                assert bool(bytes_) == embed_external_files

    @require_pil
    def test_push_dataset_to_hub_custom_features_image(self, temporary_repo):
        image_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_image_rgb.jpg")
        data = {"x": [image_path, None], "y": [0, -1]}
        features = Features({"x": Image(), "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
                ds.push_to_hub(ds_name, embed_external_files=embed_external_files, token=self._token)
                hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

                assert ds.column_names == hub_ds.column_names
                assert list(ds.features.keys()) == list(hub_ds.features.keys())
                assert ds.features == hub_ds.features
                assert ds[:] == hub_ds[:]
                hub_ds = hub_ds.cast_column("x", Image(decode=False))
                elem = hub_ds[0]["x"]
                path, bytes_ = elem["path"], elem["bytes"]
                assert isinstance(path, str)
                assert bool(bytes_) == embed_external_files

    @require_pil
    def test_push_dataset_to_hub_custom_features_image_list(self, temporary_repo):
        image_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_image_rgb.jpg")
        data = {"x": [[image_path], [image_path, image_path]], "y": [0, -1]}
        features = Features({"x": [Image()], "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
                ds.push_to_hub(ds_name, embed_external_files=embed_external_files, token=self._token)
                hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

                assert ds.column_names == hub_ds.column_names
                assert list(ds.features.keys()) == list(hub_ds.features.keys())
                assert ds.features == hub_ds.features
                assert ds[:] == hub_ds[:]
                hub_ds = hub_ds.cast_column("x", [Image(decode=False)])
                elem = hub_ds[0]["x"][0]
                path, bytes_ = elem["path"], elem["bytes"]
                assert isinstance(path, str)
                assert bool(bytes_) == embed_external_files

    def test_push_dataset_dict_to_hub_custom_features(self, temporary_repo):
        features = Features({"x": Value("int64"), "y": ClassLabel(names=["neg", "pos"])})
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [0, 0, 1]}, features=features)

        local_ds = DatasetDict({"test": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["test"].features.keys()) == list(hub_ds["test"].features.keys())
            assert local_ds["test"].features == hub_ds["test"].features

    def test_push_dataset_to_hub_custom_splits(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            ds.push_to_hub(ds_name, split="random", token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert ds.column_names == hub_ds["random"].column_names
            assert list(ds.features.keys()) == list(hub_ds["random"].features.keys())
            assert ds.features == hub_ds["random"].features

    def test_push_dataset_to_hub_skip_identical_files(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})
        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            with patch("datasets.arrow_dataset.HfApi.upload_file", side_effect=self._api.upload_file) as mock_hf_api:
                # Initial push
                ds.push_to_hub(ds_name, token=self._token, max_shard_size="1KB")
                call_count_old = mock_hf_api.call_count
                mock_hf_api.reset_mock()

                # Remove a data file
                files = self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token)
                data_files = [f for f in files if f.startswith("data/")]
                assert len(data_files) > 1
                self._api.delete_file(data_files[0], repo_id=ds_name, repo_type="dataset", token=self._token)

                # "Resume" push - push missing files
                ds.push_to_hub(ds_name, token=self._token, max_shard_size="1KB")
                call_count_new = mock_hf_api.call_count
                assert call_count_old > call_count_new

            hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")
            assert ds.column_names == hub_ds.column_names
            assert list(ds.features.keys()) == list(hub_ds.features.keys())
            assert ds.features == hub_ds.features

    def test_push_dataset_to_hub_multiple_splits_one_by_one(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            ds.push_to_hub(ds_name, split="train", token=self._token)
            ds.push_to_hub(ds_name, split="test", token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")
            assert sorted(hub_ds) == ["test", "train"]
            assert ds.column_names == hub_ds["train"].column_names
            assert list(ds.features.keys()) == list(hub_ds["train"].features.keys())
            assert ds.features == hub_ds["train"].features

    def test_push_dataset_dict_to_hub_custom_splits(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"random": ds})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["random"].features.keys()) == list(hub_ds["random"].features.keys())
            assert local_ds["random"].features == hub_ds["random"].features

    @unittest.skip("This test cannot pass until iterable datasets have push to hub")
    def test_push_streaming_dataset_dict_to_hub(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        local_ds = DatasetDict({"train": ds})
        with tempfile.TemporaryDirectory() as tmp:
            local_ds.save_to_disk(tmp)
            local_ds = load_dataset(tmp, streaming=True)

            with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
                local_ds.push_to_hub(ds_name, token=self._token)
                hub_ds = load_dataset(ds_name, download_mode="force_redownload")

                assert local_ds.column_names == hub_ds.column_names
                assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
                assert local_ds["train"].features == hub_ds["train"].features

    def test_push_multiple_dataset_configs_to_hub(self, temporary_repo):
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)
            ds_builder = load_dataset_builder(ds_name, "config1", download_mode="force_redownload")
            assert len(ds_builder.BUILDER_CONFIGS) == 2
            assert len(ds_builder.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_builder.config.data_files["train"][0],
                "*/config1/train-*",
            )
            ds_builder = load_dataset_builder(ds_name, "config2", download_mode="force_redownload")
            assert len(ds_builder.BUILDER_CONFIGS) == 2
            assert len(ds_builder.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_builder.config.data_files["train"][0],
                "*/config2/train-*",
            )
            with pytest.raises(ValueError):  # no config
                load_dataset_builder(ds_name, download_mode="force_redownload")

    def test_push_multiple_dataset_dict_configs_to_hub(self, temporary_repo):
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        ds_config1 = DatasetDict({"random": ds_config1})
        ds_config2 = DatasetDict({"random": ds_config2})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)
            ds_builder = load_dataset_builder(ds_name, "config1", download_mode="force_redownload")
            assert len(ds_builder.BUILDER_CONFIGS) == 2
            assert len(ds_builder.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_builder.config.data_files["random"][0],
                "*/config1/random-*",
            )
            ds_builder = load_dataset_builder(ds_name, "config2", download_mode="force_redownload")
            assert len(ds_builder.BUILDER_CONFIGS) == 2
            assert len(ds_builder.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_builder.config.data_files["random"][0],
                "*/config2/random-*",
            )
            with pytest.raises(ValueError):  # no config
                load_dataset_builder(ds_name, download_mode="force_redownload")

    def test_push_dataset_to_hub_with_config_no_metadata_configs(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_another_config = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        parquet_buf = BytesIO()
        ds.to_parquet(parquet_buf)
        parquet_content = parquet_buf.getvalue()

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            self._api.create_repo(ds_name, token=self._token, repo_type="dataset")
            # old push_to_hub was uploading the pqrauet fiels only - without metadata configs
            self._api.upload_file(
                path_or_fileobj=parquet_content,
                path_in_repo="data/train-00000-of-00001.parquet",
                repo_id=ds_name,
                repo_type="dataset",
            )
            ds_another_config.push_to_hub(ds_name, "another_config", token=self._token)
            ds_builder = load_dataset_builder(ds_name, download_mode="force_redownload")
            assert len(ds_builder.config.data_files["train"]) == 1
            assert len(ds_builder.config.data_files) == 1
            assert fnmatch.fnmatch(ds_builder.config.data_files["train"][0], "*/data/train-00000-of-00001.parquet")
            ds_another_config_builder = load_dataset_builder(
                ds_name, "another_config", download_mode="force_redownload"
            )
            assert len(ds_another_config_builder.config.data_files) == 1
            assert len(ds_another_config_builder.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_another_config_builder.config.data_files["train"][0],
                "*/another_config/train-00000-of-00001-*.parquet",
            )

    def test_push_dataset_dict_to_hub_with_config_no_metadata_configs(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_another_config = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        parquet_buf = BytesIO()
        ds.to_parquet(parquet_buf)
        parquet_content = parquet_buf.getvalue()

        local_ds_another_config = DatasetDict({"random": ds_another_config})

        with temporary_repo(f"{CI_HUB_USER}/test-{int(time.time() * 10e3)}") as ds_name:
            self._api.create_repo(ds_name, token=self._token, repo_type="dataset")
            # old push_to_hub was uploading the pqrauet fiels only - without metadata configs
            self._api.upload_file(
                path_or_fileobj=parquet_content,
                path_in_repo="data/random-00000-of-00001.parquet",
                repo_id=ds_name,
                repo_type="dataset",
            )
            local_ds_another_config.push_to_hub(ds_name, "another_config", token=self._token)
            ds_builder = load_dataset_builder(ds_name, download_mode="force_redownload")
            assert len(ds_builder.config.data_files) == 1
            assert len(ds_builder.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(ds_builder.config.data_files["random"][0], "*/data/random-00000-of-00001.parquet")
            ds_another_config_builder = load_dataset_builder(
                ds_name, "another_config", download_mode="force_redownload"
            )
            assert len(ds_another_config_builder.config.data_files) == 1
            assert len(ds_another_config_builder.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_another_config_builder.config.data_files["random"][0],
                "*/another_config/random-00000-of-00001-*.parquet",
            )
