import os
import tempfile
import time
import unittest
from os.path import expanduser
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import numpy as np
from huggingface_hub import HfApi
from huggingface_hub.hf_api import HfFolder

from datasets import Audio, ClassLabel, Dataset, DatasetDict, Features, Image, Value, load_dataset
from datasets.utils._hf_hub_fixes import delete_repo
from tests.utils import require_pil, require_sndfile


REPO_NAME = f"repo-{int(time.time() * 10e3)}"
ENDPOINT_STAGING = "https://moon-staging.huggingface.co"

# Should create a __DUMMY_DATASETS_USER__ :)
USER = "__DUMMY_TRANSFORMERS_USER__"
PASS = "__DUMMY_TRANSFORMERS_PASS__"
TOKEN_PATH_STAGING = expanduser("~/.huggingface/staging_token")


def with_staging_testing(func):
    config = patch.multiple(
        "datasets.config",
        HF_ENDPOINT=ENDPOINT_STAGING,
        HUB_DATASETS_URL=ENDPOINT_STAGING + "/datasets/{path}/resolve/{revision}/{name}",
    )
    return config(func)


@with_staging_testing
class TestPushToHub(TestCase):
    _api = HfApi(endpoint=ENDPOINT_STAGING)

    def cleanup_repo(self, ds_name):
        organization, name = ds_name.split("/")
        delete_repo(hf_api=self._api, name=name, organization=organization, token=self._token, repo_type="dataset")

    @classmethod
    def setUpClass(cls):
        """
        Share this valid token in all tests below.
        """
        cls._hf_folder_patch = patch(
            "huggingface_hub.hf_api.HfFolder.path_token",
            TOKEN_PATH_STAGING,
        )
        cls._hf_folder_patch.start()

        cls._token = cls._api.login(username=USER, password=PASS)
        HfFolder.save_token(cls._token)

    @classmethod
    def tearDownClass(cls) -> None:
        HfFolder.delete_token()
        cls._hf_folder_patch.stop()

    def test_push_dataset_dict_to_hub_no_token(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            self.assertListEqual(files, [".gitattributes", "data/train-00000-of-00001.parquet", "dataset_infos.json"])
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_name_without_namespace(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name.split("/")[-1], token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset"))
            self.assertListEqual(files, [".gitattributes", "data/train-00000-of-00001.parquet", "dataset_infos.json"])
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_private(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, token=self._token, private=True)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload", use_auth_token=self._token)

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            self.assertListEqual(files, [".gitattributes", "data/train-00000-of-00001.parquet", "dataset_infos.json"])
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"train": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

            # Ensure that there is a single file on the repository that has the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            self.assertListEqual(files, [".gitattributes", "data/train-00000-of-00001.parquet", "dataset_infos.json"])
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_multiple_files(self):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})

        local_ds = DatasetDict({"train": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, token=self._token, shard_size=500 << 5)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            self.assertListEqual(
                files,
                [
                    ".gitattributes",
                    "data/train-00000-of-00002.parquet",
                    "data/train-00001-of-00002.parquet",
                    "dataset_infos.json",
                ],
            )
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_overwrite_files(self):
        ds = Dataset.from_dict({"x": list(range(1000)), "y": list(range(1000))})
        ds2 = Dataset.from_dict({"x": list(range(100)), "y": list(range(100))})

        local_ds = DatasetDict({"train": ds, "random": ds2})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"

        # Push to hub two times, but the second time with a larger amount of files.
        # Verify that the new files contain the correct dataset.
        try:
            local_ds.push_to_hub(ds_name, token=self._token)

            with tempfile.TemporaryDirectory() as tmp:
                # Add a file starting with "data" to ensure it doesn't get deleted.
                path = Path(tmp) / "datafile.txt"
                with open(path, "w") as f:
                    f.write("Bogus file")

                self._api.upload_file(
                    str(path), path_in_repo="datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token
                )

            local_ds.push_to_hub(ds_name, token=self._token, shard_size=500 << 5)

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            self.assertListEqual(
                files,
                [
                    ".gitattributes",
                    "data/random-00000-of-00001.parquet",
                    "data/train-00000-of-00002.parquet",
                    "data/train-00001-of-00002.parquet",
                    "datafile.txt",
                    "dataset_infos.json",
                ],
            )

            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

        finally:
            self.cleanup_repo(ds_name)

        # Push to hub two times, but the second time with fewer files.
        # Verify that the new files contain the correct dataset and that non-necessary files have been deleted.
        try:
            local_ds.push_to_hub(ds_name, token=self._token, shard_size=500 << 5)

            with tempfile.TemporaryDirectory() as tmp:
                # Add a file starting with "data" to ensure it doesn't get deleted.
                path = Path(tmp) / "datafile.txt"
                with open(path, "w") as f:
                    f.write("Bogus file")

                self._api.upload_file(
                    str(path), path_in_repo="datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token
                )

            local_ds.push_to_hub(ds_name, token=self._token)

            # Ensure that there are two files on the repository that have the correct name
            files = sorted(self._api.list_repo_files(ds_name, repo_type="dataset", token=self._token))
            self.assertListEqual(
                files,
                [
                    ".gitattributes",
                    "data/random-00000-of-00001.parquet",
                    "data/train-00000-of-00001.parquet",
                    "datafile.txt",
                    "dataset_infos.json",
                ],
            )

            # Keeping the "datafile.txt" breaks the load_dataset to think it's a text-based dataset
            self._api.delete_file("datafile.txt", repo_id=ds_name, repo_type="dataset", token=self._token)

            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
            self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)

        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_to_hub(self):
        local_ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, split="train", token=self._token)
            local_ds_dict = {"train": local_ds}
            hub_ds_dict = load_dataset(ds_name, download_mode="force_redownload")

            self.assertListEqual(list(local_ds_dict.keys()), list(hub_ds_dict.keys()))

            for ds_split_name in local_ds_dict.keys():
                local_ds = local_ds_dict[ds_split_name]
                hub_ds = hub_ds_dict[ds_split_name]
                self.assertListEqual(local_ds.column_names, hub_ds.column_names)
                self.assertListEqual(list(local_ds.features.keys()), list(hub_ds.features.keys()))
                self.assertDictEqual(local_ds.features, hub_ds.features)
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_to_hub_custom_features(self):
        features = Features({"x": Value("int64"), "y": ClassLabel(names=["neg", "pos"])})
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [0, 0, 1]}, features=features)

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

            self.assertListEqual(ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(ds.features.keys()), list(hub_ds.features.keys()))
            self.assertDictEqual(ds.features, hub_ds.features)
            self.assertEqual(ds[:], hub_ds[:])
        finally:
            self.cleanup_repo(ds_name)

    @require_sndfile
    def test_push_dataset_to_hub_custom_features_audio(self):
        audio_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_audio_44100.wav")
        data = {"x": [audio_path, None], "y": [0, -1]}
        features = Features({"x": Audio(), "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
            try:
                ds.push_to_hub(ds_name, embed_external_files=embed_external_files, token=self._token)
                hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

                self.assertListEqual(ds.column_names, hub_ds.column_names)
                self.assertListEqual(list(ds.features.keys()), list(hub_ds.features.keys()))
                self.assertDictEqual(ds.features, hub_ds.features)
                np.testing.assert_equal(ds[0]["x"]["array"], hub_ds[0]["x"]["array"])
                self.assertEqual(
                    ds[1], hub_ds[1]
                )  # don't test hub_ds[0] since audio decoding might be slightly different
                hub_ds = hub_ds.cast_column("x", Audio(decode=False))
                elem = hub_ds[0]["x"]
                path, bytes_ = elem["path"], elem["bytes"]
                self.assertTrue(bool(path) == (not embed_external_files))
                self.assertTrue(bool(bytes_) == embed_external_files)
            finally:
                self.cleanup_repo(ds_name)

    @require_pil
    def test_push_dataset_to_hub_custom_features_image(self):
        image_path = os.path.join(os.path.dirname(__file__), "features", "data", "test_image_rgb.jpg")
        data = {"x": [image_path, None], "y": [0, -1]}
        features = Features({"x": Image(), "y": Value("int32")})
        ds = Dataset.from_dict(data, features=features)

        for embed_external_files in [True, False]:
            ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
            try:
                ds.push_to_hub(ds_name, embed_external_files=embed_external_files, token=self._token)
                hub_ds = load_dataset(ds_name, split="train", download_mode="force_redownload")

                self.assertListEqual(ds.column_names, hub_ds.column_names)
                self.assertListEqual(list(ds.features.keys()), list(hub_ds.features.keys()))
                self.assertDictEqual(ds.features, hub_ds.features)
                self.assertEqual(ds[:], hub_ds[:])
                hub_ds = hub_ds.cast_column("x", Image(decode=False))
                elem = hub_ds[0]["x"]
                path, bytes_ = elem["path"], elem["bytes"]
                self.assertTrue(bool(path) == (not embed_external_files))
                self.assertTrue(bool(bytes_) == embed_external_files)
            finally:
                self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_custom_features(self):
        features = Features({"x": Value("int64"), "y": ClassLabel(names=["neg", "pos"])})
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [0, 0, 1]}, features=features)

        local_ds = DatasetDict({"test": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["test"].features.keys()), list(hub_ds["test"].features.keys()))
            self.assertDictEqual(local_ds["test"].features, hub_ds["test"].features)
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_to_hub_custom_splits(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            ds.push_to_hub(ds_name, split="random", token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertListEqual(ds.column_names, hub_ds["random"].column_names)
            self.assertListEqual(list(ds.features.keys()), list(hub_ds["random"].features.keys()))
            self.assertDictEqual(ds.features, hub_ds["random"].features)
        finally:
            self.cleanup_repo(ds_name)

    def test_push_dataset_dict_to_hub_custom_splits(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})

        local_ds = DatasetDict({"random": ds})

        ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
        try:
            local_ds.push_to_hub(ds_name, token=self._token)
            hub_ds = load_dataset(ds_name, download_mode="force_redownload")

            self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
            self.assertListEqual(list(local_ds["random"].features.keys()), list(hub_ds["random"].features.keys()))
            self.assertDictEqual(local_ds["random"].features, hub_ds["random"].features)
        finally:
            self.cleanup_repo(ds_name)

    @unittest.skip("This test cannot pass until iterable datasets have push to hub")
    def test_push_streaming_dataset_dict_to_hub(self):
        ds = Dataset.from_dict({"x": [1, 2, 3], "y": [4, 5, 6]})
        local_ds = DatasetDict({"train": ds})
        with tempfile.TemporaryDirectory() as tmp:
            local_ds.save_to_disk(tmp)
            local_ds = load_dataset(tmp, streaming=True)

            ds_name = f"{USER}/test-{int(time.time() * 10e3)}"
            try:
                local_ds.push_to_hub(ds_name, token=self._token)
                hub_ds = load_dataset(ds_name, download_mode="force_redownload")

                self.assertDictEqual(local_ds.column_names, hub_ds.column_names)
                self.assertListEqual(list(local_ds["train"].features.keys()), list(hub_ds["train"].features.keys()))
                self.assertDictEqual(local_ds["train"].features, hub_ds["train"].features)
            finally:
                self.cleanup_repo(ds_name)
