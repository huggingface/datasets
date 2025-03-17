import fnmatch
import gc
import os
import shutil
import tempfile
import textwrap
import time
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from huggingface_hub import DatasetCard, HfApi

from datasets import (
    Audio,
    ClassLabel,
    Dataset,
    DatasetDict,
    DownloadManager,
    Features,
    Image,
    Value,
    load_dataset,
    load_dataset_builder,
)
from datasets.config import METADATA_CONFIGS_FIELD
from datasets.data_files import get_data_patterns
from datasets.exceptions import DatasetNotFoundError
from datasets.packaged_modules.folder_based_builder.folder_based_builder import (
    FolderBasedBuilder,
    FolderBasedBuilderConfig,
)
from datasets.utils.file_utils import cached_path
from datasets.utils.hub import hf_dataset_url

from .fixtures.hub import CI_HUB_ENDPOINT, CI_HUB_USER, CI_HUB_USER_TOKEN
from .utils import for_all_test_methods, require_librosa, require_pil, require_sndfile, xfail_if_500_502_http_error


pytestmark = pytest.mark.integration


@for_all_test_methods(xfail_if_500_502_http_error)
@pytest.mark.usefixtures("ci_hub_config", "ci_hfh_hf_hub_url")
class TestPushToHub:
    _api = HfApi(endpoint=CI_HUB_ENDPOINT)
    _token = CI_HUB_USER_TOKEN

    def test_push_dataset_dict_to_hub_no_token(self, temporary_repo, set_ci_hub_access_token):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub_name_without_namespace(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name.split("/")[-1], token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub_datasets_with_different_features(self, cleanup_repo):
        ds_train = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_test = Dataset.from_dict({"x": [True, False, True], "y": ["a", "b", "c"]})

        local_ds = DatasetDict({"train": ds_train, "test": ds_test})

        ds_name = f"{CI_HUB_USER}/test-{int(time.time() * 10e6)}"
        try:
            with pytest.raises(ValueError):
                local_ds.push_to_hub(ds_name.split("/")[-1], token=self._token)
        except AssertionError:
            cleanup_repo(ds_name)
            raise

    def test_push_dataset_dict_to_hub_private(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, private=True)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload", token=self._token)

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub_with_pull_request(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, create_pr=True)
            hub_ds = load_dataset(ds_name, revision="refs/pr/1", download_mode="force_redownload")

            assert local_ds["train"].features == hub_ds["train"].features
            assert list(local_ds.keys()) == list(hub_ds.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(
                self._api.list_repo_files(ds_name, revision="refs/pr/1", repo_type="dataset", token=self._token)
            )
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub_with_revision(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, revision="dev")
            hub_ds = load_dataset(ds_name, revision="dev", download_mode="force_redownload")

            assert local_ds["train"].features == hub_ds["train"].features
            assert list(local_ds.keys()) == list(hub_ds.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, revision="dev", repo_type="dataset", token=self._token))
            assert files == [".gitattributes", "README.md", "data/train-00000-of-00001.parquet"]

    def test_push_dataset_dict_to_hub_multiple_files(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            with patch("datasets.config.MAX_SHARD_SIZE", "16KB"):
                local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [
                ".gitattributes",
                "README.md",
                "data/train-00000-of-00002.parquet",
                "data/train-00001-of-00002.parquet",
            ]

    def test_push_dataset_dict_to_hub_multiple_files_with_max_shard_size(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, max_shard_size="16KB")
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [
                ".gitattributes",
                "README.md",
                "data/train-00000-of-00002.parquet",
                "data/train-00001-of-00002.parquet",
            ]

    def test_push_dataset_dict_to_hub_multiple_files_with_num_shards(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token, num_shards={"train": 2})
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [
                ".gitattributes",
                "README.md",
                "data/train-00000-of-00002.parquet",
                "data/train-00001-of-00002.parquet",
            ]

    def test_push_dataset_dict_to_hub_with_multiple_commits(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        with temporary_repo() as ds_name:
            self._api.create_repo(ds_name, token=self._token, repo_type="dataset")
            num_commits_before_push = len(self._api.list_repo_commits(ds_name, repo_type="dataset", token=self._token))
            with (
                patch("datasets.config.MAX_SHARD_SIZE", "16KB"),
                patch("datasets.config.UPLOADS_MAX_NUMBER_PER_COMMIT", 1),
            ):
                local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            assert files == [
                ".gitattributes",
                "README.md",
                "data/train-00000-of-00002.parquet",
                "data/train-00001-of-00002.parquet",
            ]

            num_commits_after_push = len(self._api.list_repo_commits(ds_name, repo_type="dataset", token=self._token))
            assert num_commits_after_push - num_commits_before_push > 1

    def test_push_dataset_dict_to_hub_overwrite_files(self, temporary_repo):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})
        ds2 = Dataset.from_dict({"x": list(range(100)), "y": list(range(100))})

        local_ds = DatasetDict({"train": ds, "random": ds2})

        # Push to hub two times, but the second time with a larger amount of files.
        # Verify that the new files contain the correct dataset.
        with temporary_repo() as ds_name:
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
            assert files == [
                ".gitattributes",
                "README.md",
                "data/random-00000-of-00001.parquet",
                "data/train-00000-of-00002.parquet",
                "data/train-00001-of-00002.parquet",
                "datafile.txt",
            ]

            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

        del hub_ds

        # To ensure the reference to the memory-mapped Arrow file is dropped to avoid the PermissionError on Windows
        gc.collect()

        # Push to hub two times, but the second time with fewer files.
        # Verify that the new files contain the correct dataset and that non-necessary files have been deleted.
        with temporary_repo(ds_name):
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
            assert files == [
                ".gitattributes",
                "README.md",
                "data/random-00000-of-00001.parquet",
                "data/train-00000-of-00001.parquet",
                "datafile.txt",
            ]

            # Keeping the "datafile.txt" breaks the load_dataset to think it's a text-based dataset
            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
            assert local_ds["train"].features == hub_ds["train"].features

    def test_push_dataset_to_hub(self, temporary_repo):
        local_ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        with temporary_repo() as ds_name:
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

        with temporary_repo() as ds_name:
            ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

            assert ds.column_names == hub_ds.column_names
            assert list(ds.features.keys()) == list(hub_ds.features.keys())
            assert ds.features == hub_ds.features
            assert ds[:] == hub_ds[:]

    @require_librosa
    @require_sndfile
    def test_push_dataset_to_hub_custom_features_audio(self, temporary_repo):
        audio_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_audio_44100.wav")
        data = {"x": [audio_path, None], "y": [0, -1]}
        features = Features({"x": Audio(), "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            with temporary_repo() as ds_name:
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
            with temporary_repo() as ds_name:
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
            with temporary_repo() as ds_name:
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

        with temporary_repo() as ds_name:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert local_ds.column_names == hub_ds.column_names
            assert list(local_ds["test"].features.keys()) == list(hub_ds["test"].features.keys())
            assert local_ds["test"].features == hub_ds["test"].features

    def test_push_dataset_to_hub_custom_splits(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        with temporary_repo() as ds_name:
            ds.push_to_hub(ds_name, split="random", token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            assert ds.column_names == hub_ds["random"].column_names
            assert list(ds.features.keys()) == list(hub_ds["random"].features.keys())
            assert ds.features == hub_ds["random"].features

    def test_push_dataset_to_hub_multiple_splits_one_by_one(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        with temporary_repo() as ds_name:
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

        with temporary_repo() as ds_name:
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

            with temporary_repo() as ds_name:
                local_ds.push_to_hub(ds_name, token=self._token)
                hub_ds = load_dataset(ds_name, download_mode="force_redownload")

                assert local_ds.column_names == hub_ds.column_names
                assert list(local_ds["train"].features.keys()) == list(hub_ds["train"].features.keys())
                assert local_ds["train"].features == hub_ds["train"].features

    def test_push_multiple_dataset_configs_to_hub_load_dataset_builder(self, temporary_repo):
        ds_default = Dataset.from_dict({"a": [0], "b": [1]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})

        with temporary_repo() as ds_name:
            ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)
            ds_builder_default = load_dataset_builder(ds_name, download_mode="force_redownload")  # default config
            assert len(ds_builder_default.BUILDER_CONFIGS) == 3
            assert len(ds_builder_default.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_default.config.data_files["train"][0],
                "*/data/train-*",
            )
            ds_builder_config1 = load_dataset_builder(ds_name, "config1", download_mode="force_redownload")
            assert len(ds_builder_config1.BUILDER_CONFIGS) == 3
            assert len(ds_builder_config1.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_config1.config.data_files["train"][0],
                "*/config1/train-*",
            )
            ds_builder_config2 = load_dataset_builder(ds_name, "config2", download_mode="force_redownload")
            assert len(ds_builder_config2.BUILDER_CONFIGS) == 3
            assert len(ds_builder_config2.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_config2.config.data_files["train"][0],
                "*/config2/train-*",
            )

            with pytest.raises(ValueError):  # no config 'config3'
                load_dataset_builder(ds_name, "config3", download_mode="force_redownload")

    def test_push_multiple_dataset_configs_to_hub_load_dataset(self, temporary_repo):
        ds_default = Dataset.from_dict({"a": [0], "b": [1]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})

        with temporary_repo() as ds_name:
            ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)

            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert files == [
                ".gitattributes",
                "README.md",
                "config1/train-00000-of-00001.parquet",
                "config2/train-00000-of-00001.parquet",
                "data/train-00000-of-00001.parquet",
            ]

            hub_ds_default = load_dataset(ds_name, download_mode="force_redownload")
            hub_ds_config1 = load_dataset(ds_name, "config1", download_mode="force_redownload")
            hub_ds_config2 = load_dataset(ds_name, "config2", download_mode="force_redownload")

            # only "train" split
            assert len(hub_ds_default) == len(hub_ds_config1) == len(hub_ds_config2) == 1

            assert ds_default.column_names == hub_ds_default["train"].column_names == ["a", "b"]
            assert ds_config1.column_names == hub_ds_config1["train"].column_names == ["x", "y"]
            assert ds_config2.column_names == hub_ds_config2["train"].column_names == ["foo", "bar"]

            assert ds_default.features == hub_ds_default["train"].features
            assert ds_config1.features == hub_ds_config1["train"].features
            assert ds_config2.features == hub_ds_config2["train"].features

            assert ds_default.num_rows == hub_ds_default["train"].num_rows == 1
            assert ds_config1.num_rows == hub_ds_config1["train"].num_rows == 3
            assert ds_config2.num_rows == hub_ds_config2["train"].num_rows == 2

            with pytest.raises(ValueError):  # no config 'config3'
                load_dataset(ds_name, "config3", download_mode="force_redownload")

    @pytest.mark.parametrize("specific_default_config_name", [False, True])
    def test_push_multiple_dataset_configs_to_hub_readme_metadata_content(
        self, specific_default_config_name, temporary_repo
    ):
        ds_default = Dataset.from_dict({"a": [0], "b": [2]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})

        with temporary_repo() as ds_name:
            if specific_default_config_name:
                ds_default.push_to_hub(ds_name, config_name="config0", set_default=True, token=self._token)
            else:
                ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)

            # check that configs args was correctly pushed to README.md
            ds_readme_path = cached_path(hf_dataset_url(ds_name, "README.md"))
            dataset_card_data = DatasetCard.load(ds_readme_path).data
            assert METADATA_CONFIGS_FIELD in dataset_card_data
            assert isinstance(dataset_card_data[METADATA_CONFIGS_FIELD], list)
            assert sorted(dataset_card_data[METADATA_CONFIGS_FIELD], key=lambda x: x["config_name"]) == (
                [
                    {
                        "config_name": "config0",
                        "data_files": [
                            {"split": "train", "path": "config0/train-*"},
                        ],
                        "default": True,
                    },
                ]
                if specific_default_config_name
                else []
            ) + [
                {
                    "config_name": "config1",
                    "data_files": [
                        {"split": "train", "path": "config1/train-*"},
                    ],
                },
                {
                    "config_name": "config2",
                    "data_files": [
                        {"split": "train", "path": "config2/train-*"},
                    ],
                },
            ] + (
                []
                if specific_default_config_name
                else [
                    {
                        "config_name": "default",
                        "data_files": [
                            {"split": "train", "path": "data/train-*"},
                        ],
                    },
                ]
            )

    def test_push_multiple_dataset_dict_configs_to_hub_load_dataset_builder(self, temporary_repo):
        ds_default = Dataset.from_dict({"a": [0], "b": [1]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        ds_default = DatasetDict({"random": ds_default})
        ds_config1 = DatasetDict({"random": ds_config1})
        ds_config2 = DatasetDict({"random": ds_config2})

        with temporary_repo() as ds_name:
            ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)

            ds_builder_default = load_dataset_builder(ds_name, download_mode="force_redownload")  # default config
            assert len(ds_builder_default.BUILDER_CONFIGS) == 3
            assert len(ds_builder_default.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_default.config.data_files["random"][0],
                "*/data/random-*",
            )
            ds_builder_config1 = load_dataset_builder(ds_name, "config1", download_mode="force_redownload")
            assert len(ds_builder_config1.BUILDER_CONFIGS) == 3
            assert len(ds_builder_config1.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_config1.config.data_files["random"][0],
                "*/config1/random-*",
            )
            ds_builder_config2 = load_dataset_builder(ds_name, "config2", download_mode="force_redownload")
            assert len(ds_builder_config2.BUILDER_CONFIGS) == 3
            assert len(ds_builder_config2.config.data_files["random"]) == 1
            assert fnmatch.fnmatch(
                ds_builder_config2.config.data_files["random"][0],
                "*/config2/random-*",
            )
            with pytest.raises(ValueError):  # no config named 'config3'
                load_dataset_builder(ds_name, "config3", download_mode="force_redownload")

    def test_push_multiple_dataset_dict_configs_to_hub_load_dataset(self, temporary_repo):
        ds_default = Dataset.from_dict({"a": [0], "b": [1]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        ds_default = DatasetDict({"train": ds_default, "random": ds_default})
        ds_config1 = DatasetDict({"train": ds_config1, "random": ds_config1})
        ds_config2 = DatasetDict({"train": ds_config2, "random": ds_config2})

        with temporary_repo() as ds_name:
            ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)

            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            assert files == [
                ".gitattributes",
                "README.md",
                "config1/random-00000-of-00001.parquet",
                "config1/train-00000-of-00001.parquet",
                "config2/random-00000-of-00001.parquet",
                "config2/train-00000-of-00001.parquet",
                "data/random-00000-of-00001.parquet",
                "data/train-00000-of-00001.parquet",
            ]

            hub_ds_default = load_dataset(ds_name, download_mode="force_redownload")
            hub_ds_config1 = load_dataset(ds_name, "config1", download_mode="force_redownload")
            hub_ds_config2 = load_dataset(ds_name, "config2", download_mode="force_redownload")

            # two splits
            expected_splits = ["random", "train"]
            assert len(hub_ds_default) == len(hub_ds_config1) == len(hub_ds_config2) == 2
            assert sorted(hub_ds_default) == sorted(hub_ds_config1) == sorted(hub_ds_config2) == expected_splits

            for split in expected_splits:
                assert ds_default[split].column_names == hub_ds_default[split].column_names == ["a", "b"]
                assert ds_config1[split].column_names == hub_ds_config1[split].column_names == ["x", "y"]
                assert ds_config2[split].column_names == hub_ds_config2[split].column_names == ["foo", "bar"]

                assert ds_default[split].features == hub_ds_default[split].features
                assert ds_config1[split].features == hub_ds_config1[split].features
                assert ds_config2[split].features == hub_ds_config2["train"].features

                assert ds_default[split].num_rows == hub_ds_default[split].num_rows == 1
                assert ds_config1[split].num_rows == hub_ds_config1[split].num_rows == 3
                assert ds_config2[split].num_rows == hub_ds_config2[split].num_rows == 2

            with pytest.raises(ValueError):  # no config 'config3'
                load_dataset(ds_name, "config3", download_mode="force_redownload")

    @pytest.mark.parametrize("specific_default_config_name", [False, True])
    def test_push_multiple_dataset_dict_configs_to_hub_readme_metadata_content(
        self, specific_default_config_name, temporary_repo
    ):
        ds_default = Dataset.from_dict({"a": [0], "b": [1]})
        ds_config1 = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_config2 = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        ds_default = DatasetDict({"train": ds_default, "random": ds_default})
        ds_config1 = DatasetDict({"train": ds_config1, "random": ds_config1})
        ds_config2 = DatasetDict({"train": ds_config2, "random": ds_config2})

        with temporary_repo() as ds_name:
            if specific_default_config_name:
                ds_default.push_to_hub(ds_name, config_name="config0", set_default=True, token=self._token)
            else:
                ds_default.push_to_hub(ds_name, token=self._token)
            ds_config1.push_to_hub(ds_name, "config1", token=self._token)
            ds_config2.push_to_hub(ds_name, "config2", token=self._token)

            # check that configs args was correctly pushed to README.md
            ds_readme_path = cached_path(hf_dataset_url(ds_name, "README.md"))
            dataset_card_data = DatasetCard.load(ds_readme_path).data
            assert METADATA_CONFIGS_FIELD in dataset_card_data
            assert isinstance(dataset_card_data[METADATA_CONFIGS_FIELD], list)
            assert sorted(dataset_card_data[METADATA_CONFIGS_FIELD], key=lambda x: x["config_name"]) == (
                [
                    {
                        "config_name": "config0",
                        "data_files": [
                            {"split": "train", "path": "config0/train-*"},
                            {"split": "random", "path": "config0/random-*"},
                        ],
                        "default": True,
                    },
                ]
                if specific_default_config_name
                else []
            ) + [
                {
                    "config_name": "config1",
                    "data_files": [
                        {"split": "train", "path": "config1/train-*"},
                        {"split": "random", "path": "config1/random-*"},
                    ],
                },
                {
                    "config_name": "config2",
                    "data_files": [
                        {"split": "train", "path": "config2/train-*"},
                        {"split": "random", "path": "config2/random-*"},
                    ],
                },
            ] + (
                []
                if specific_default_config_name
                else [
                    {
                        "config_name": "default",
                        "data_files": [
                            {"split": "train", "path": "data/train-*"},
                            {"split": "random", "path": "data/random-*"},
                        ],
                    },
                ]
            )

    def test_push_dataset_to_hub_with_config_no_metadata_configs(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_another_config = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        parquet_buf = BytesIO()
        ds.to_parquet(parquet_buf)
        parquet_content = parquet_buf.getvalue()

        with temporary_repo() as ds_name:
            self._api.create_repo(ds_name, token=self._token, repo_type="dataset")
            # old push_to_hub was uploading the parquet files only - without metadata configs
            self._api.upload_file(
                path_or_fileobj=parquet_content,
                path_in_repo="data/train-00000-of-00001.parquet",
                repo_id=ds_name,
                repo_type="dataset",
                token=self._token,
            )
            ds_another_config.push_to_hub(ds_name, "another_config", token=self._token)
            ds_builder = load_dataset_builder(ds_name, download_mode="force_redownload")
            assert len(ds_builder.config.data_files) == 1
            assert len(ds_builder.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(ds_builder.config.data_files["train"][0], "*/data/train-00000-of-00001.parquet")
            ds_another_config_builder = load_dataset_builder(
                ds_name, "another_config", download_mode="force_redownload"
            )
            assert len(ds_another_config_builder.config.data_files) == 1
            assert len(ds_another_config_builder.config.data_files["train"]) == 1
            assert fnmatch.fnmatch(
                ds_another_config_builder.config.data_files["train"][0],
                "*/another_config/train-00000-of-00001.parquet",
            )

    def test_push_dataset_dict_to_hub_with_config_no_metadata_configs(self, temporary_repo):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        ds_another_config = Dataset.from_dict({"foo": [1, 2], "bar": [4, 5]})
        parquet_buf = BytesIO()
        ds.to_parquet(parquet_buf)
        parquet_content = parquet_buf.getvalue()

        local_ds_another_config = DatasetDict({"random": ds_another_config})

        with temporary_repo() as ds_name:
            self._api.create_repo(ds_name, token=self._token, repo_type="dataset")
            # old push_to_hub was uploading the parquet files only - without metadata configs
            self._api.upload_file(
                path_or_fileobj=parquet_content,
                path_in_repo="data/random-00000-of-00001.parquet",
                repo_id=ds_name,
                repo_type="dataset",
                token=self._token,
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
                "*/another_config/random-00000-of-00001.parquet",
            )


class DummyFolderBasedBuilder(FolderBasedBuilder):
    BASE_FEATURE = dict
    BASE_COLUMN_NAME = "base"
    BUILDER_CONFIG_CLASS = FolderBasedBuilderConfig
    EXTENSIONS = [".txt"]
    # CLASSIFICATION_TASK = TextClassification(text_column="base", label_column="label")


@pytest.fixture(params=[".jsonl", ".csv"])
def text_file_with_metadata(request, tmp_path, text_file):
    metadata_filename_extension = request.param
    data_dir = tmp_path / "data_dir"
    data_dir.mkdir()
    text_file_path = data_dir / "file.txt"
    shutil.copyfile(text_file, text_file_path)
    metadata_file_path = data_dir / f"metadata{metadata_filename_extension}"
    metadata = textwrap.dedent(
        """\
        {"file_name": "file.txt", "additional_feature": "Dummy file"}
        """
        if metadata_filename_extension == ".jsonl"
        else """\
        file_name,additional_feature
        file.txt,Dummy file
        """
    )
    with open(metadata_file_path, "w", encoding="utf-8") as f:
        f.write(metadata)
    return text_file_path, metadata_file_path


@for_all_test_methods(xfail_if_500_502_http_error)
@pytest.mark.usefixtures("ci_hub_config", "ci_hfh_hf_hub_url")
class TestLoadFromHub:
    _api = HfApi(endpoint=CI_HUB_ENDPOINT)
    _token = CI_HUB_USER_TOKEN

    def test_load_dataset_with_metadata_file(self, temporary_repo, text_file_with_metadata, tmp_path):
        text_file_path, metadata_file_path = text_file_with_metadata
        data_dir_path = text_file_path.parent
        cache_dir_path = tmp_path / ".cache"
        cache_dir_path.mkdir()
        with temporary_repo() as repo_id:
            self._api.create_repo(repo_id, token=self._token, repo_type="dataset")
            self._api.upload_folder(
                folder_path=str(data_dir_path),
                repo_id=repo_id,
                repo_type="dataset",
                token=self._token,
            )
            data_files = [
                f"hf://datasets/{repo_id}/{text_file_path.name}",
                f"hf://datasets/{repo_id}/{metadata_file_path.name}",
            ]
            builder = DummyFolderBasedBuilder(
                dataset_name=repo_id.split("/")[-1], data_files=data_files, cache_dir=str(cache_dir_path)
            )
            download_manager = DownloadManager()
            gen_kwargs = builder._split_generators(download_manager)[0].gen_kwargs
            generator = builder._generate_examples(**gen_kwargs)
            result = [example for _, example in generator]
            assert len(result) == 1

    def test_get_data_patterns(self, temporary_repo, tmp_path):
        repo_dir = tmp_path / "test_get_data_patterns"
        data_dir = repo_dir / "data"
        data_dir.mkdir(parents=True)
        data_file = data_dir / "train-00001-of-00009.parquet"
        data_file.touch()
        with temporary_repo() as repo_id:
            self._api.create_repo(repo_id, token=self._token, repo_type="dataset")
            self._api.upload_folder(
                folder_path=str(repo_dir),
                repo_id=repo_id,
                repo_type="dataset",
                token=self._token,
            )
            data_file_patterns = get_data_patterns(f"hf://datasets/{repo_id}")
            assert data_file_patterns == {
                "train": ["data/train-[0-9][0-9][0-9][0-9][0-9]-of-[0-9][0-9][0-9][0-9][0-9]*.*"]
            }

    @pytest.mark.parametrize("dataset", ["gated", "private"])
    def test_load_dataset_raises_for_unauthenticated_user(
        self, dataset, hf_gated_dataset_repo_txt_data, hf_private_dataset_repo_txt_data
    ):
        dataset_ids = {
            "gated": hf_gated_dataset_repo_txt_data,
            "private": hf_private_dataset_repo_txt_data,
        }
        dataset_id = dataset_ids[dataset]
        with pytest.raises(DatasetNotFoundError):
            _ = load_dataset(dataset_id, token=False)
