import os
from tempfile import TemporaryDirectory
from unittest import TestCase

import pytest
from absl.testing import parameterized

from datasets import config, load_dataset_builder
from datasets.arrow_reader import HF_GCP_BASE_URL
from datasets.dataset_dict import IterableDatasetDict
from datasets.iterable_dataset import IterableDataset
from datasets.utils.file_utils import cached_path


DATASETS_ON_HF_GCP = [
    {"dataset": "wikipedia", "config_name": "20220301.de", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wikipedia", "config_name": "20220301.en", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wikipedia", "config_name": "20220301.fr", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wikipedia", "config_name": "20220301.frr", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wikipedia", "config_name": "20220301.it", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wikipedia", "config_name": "20220301.simple", "revision": "4d013bdd32c475c8536aae00a56efc774f061649"},
    {"dataset": "wiki40b", "config_name": "en", "revision": "7b21a2e64b90323b2d3d1b81aa349bb4bc76d9bf"},
    {
        "dataset": "wiki_dpr",
        "config_name": "psgs_w100.nq.compressed",
        "revision": "b24a417d802a583f8922946c1c75210290e93108",
    },
    {
        "dataset": "wiki_dpr",
        "config_name": "psgs_w100.nq.no_index",
        "revision": "b24a417d802a583f8922946c1c75210290e93108",
    },
    {
        "dataset": "wiki_dpr",
        "config_name": "psgs_w100.multiset.no_index",
        "revision": "b24a417d802a583f8922946c1c75210290e93108",
    },
    {"dataset": "natural_questions", "config_name": "default", "revision": "19ba7767b174ad046a84f46af056517a3910ee57"},
]


def list_datasets_on_hf_gcp_parameters(with_config=True, with_revision=True):
    columns = ["dataset"]
    if with_config:
        columns.append("config_name")
    if with_revision:
        columns.append("revision")
    dataset_list = [{col: dataset[col] for col in columns} for dataset in DATASETS_ON_HF_GCP]

    def get_testcase_name(dataset):
        testcase_name = dataset["dataset"]
        if with_config:
            testcase_name += "/" + dataset["config_name"]
        if with_revision:
            testcase_name += "@" + dataset["revision"]
        return testcase_name

    dataset_list = [{"testcase_name": get_testcase_name(dataset), **dataset} for dataset in dataset_list]
    return dataset_list


@parameterized.named_parameters(list_datasets_on_hf_gcp_parameters(with_config=True, with_revision=True))
class TestDatasetOnHfGcp(TestCase):
    dataset = None
    config_name = None
    revision = None

    def test_dataset_info_available(self, dataset, config_name, revision):
        with TemporaryDirectory() as tmp_dir:
            builder = load_dataset_builder(
                dataset,
                config_name,
                revision=revision,
                cache_dir=tmp_dir,
            )

            dataset_info_url = "/".join(
                [
                    HF_GCP_BASE_URL,
                    builder._relative_data_dir(with_hash=False).replace(os.sep, "/"),
                    config.DATASET_INFO_FILENAME,
                ]
            )
            datset_info_path = cached_path(dataset_info_url, cache_dir=tmp_dir)
            self.assertTrue(os.path.exists(datset_info_path))


@pytest.mark.integration
def test_as_dataset_from_hf_gcs(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("test_hf_gcp") / "test_wikipedia_simple"
    builder = load_dataset_builder("wikipedia", "20220301.frr", cache_dir=tmp_dir)
    # use the HF cloud storage, not the original download_and_prepare that uses apache-beam
    builder._download_and_prepare = None
    builder.download_and_prepare(try_from_hf_gcs=True)
    ds = builder.as_dataset()
    assert ds


@pytest.mark.integration
def test_as_streaming_dataset_from_hf_gcs(tmp_path):
    builder = load_dataset_builder(
        "wikipedia", "20220301.frr", revision="4d013bdd32c475c8536aae00a56efc774f061649", cache_dir=tmp_path
    )
    ds = builder.as_streaming_dataset()
    assert ds
    assert isinstance(ds, IterableDatasetDict)
    assert "train" in ds
    assert isinstance(ds["train"], IterableDataset)
    assert next(iter(ds["train"]))
