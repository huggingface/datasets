import fnmatch
import os
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest
from huggingface_hub import HfApi

from datasets import Audio, ClassLabel, Dataset, DatasetDict, Features, Image, Value, load_dataset
from tests.fixtures.hub import CI_HUB_ENDPOINT, CI_HUB_USER, CI_HUB_USER_TOKEN
from tests.utils import require_pil, require_sndfile


pytestmark = pytest.mark.integration


@pytest.mark.usefixtures("set_ci_hub_access_token")
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
                    files, [".gitattributes", "data/train-00000-of-00001-*.parquet", "dataset_infos.json"]
                )
            )

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
                    files, [".gitattributes", "data/train-00000-of-00001-*.parquet", "dataset_infos.json"]
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
                    files, [".gitattributes", "data/train-00000-of-00001-*.parquet", "dataset_infos.json"]
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
                    files, [".gitattributes", "data/train-00000-of-00001-*.parquet", "dataset_infos.json"]
                )
            )

    def test_push_dataset_dict_to_hub_multiple_files(self, temporary_repo):
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
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                        "dataset_infos.json",
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
                        "data/random-00000-of-00001-*.parquet",
                        "data/train-00000-of-00002-*.parquet",
                        "data/train-00001-of-00002-*.parquet",
                        "datafile.txt",
                        "dataset_infos.json",
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
                        "data/random-00000-of-00001-*.parquet",
                        "data/train-00000-of-00001-*.parquet",
                        "datafile.txt",
                        "dataset_infos.json",
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
                assert bool(path) == (not embed_external_files)
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
                assert bool(path) == (not embed_external_files)
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
                assert bool(path) == (not embed_external_files)
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
