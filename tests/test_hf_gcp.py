import os
from tempfile import TemporaryDirectory
from unittest import TestCase

import pytest
from absl.testing import parameterized

from datasets import config
from datasets.arrow_reader import HF_GCP_BASE_URL
from datasets.builder import DatasetBuilder
from datasets.dataset_dict import IterableDatasetDict
from datasets.iterable_dataset import IterableDataset
from datasets.load import dataset_module_factory, import_main_class
from datasets.utils.file_utils import cached_path


DATASETS_ON_HF_GCP = [
    {"dataset": "wikipedia", "config_name": "20220301.de"},
    {"dataset": "wikipedia", "config_name": "20220301.en"},
    {"dataset": "wikipedia", "config_name": "20220301.fr"},
    {"dataset": "wikipedia", "config_name": "20220301.frr"},
    {"dataset": "wikipedia", "config_name": "20220301.it"},
    {"dataset": "wikipedia", "config_name": "20220301.simple"},
    {"dataset": "snli", "config_name": "plain_text"},
    {"dataset": "eli5", "config_name": "LFQA_reddit"},
    {"dataset": "wiki40b", "config_name": "en"},
    {"dataset": "wiki_dpr", "config_name": "psgs_w100.nq.compressed"},
    {"dataset": "wiki_dpr", "config_name": "psgs_w100.nq.no_index"},
    {"dataset": "wiki_dpr", "config_name": "psgs_w100.multiset.no_index"},
    {"dataset": "natural_questions", "config_name": "default"},
]


def list_datasets_on_hf_gcp_parameters(with_config=True):
    if with_config:
        return [
            {
                "testcase_name": d["dataset"] + "/" + d["config_name"],
                "dataset": d["dataset"],
                "config_name": d["config_name"],
            }
            for d in DATASETS_ON_HF_GCP
        ]
    else:
        return [
            {"testcase_name": dataset, "dataset": dataset} for dataset in {d["dataset"] for d in DATASETS_ON_HF_GCP}
        ]


@parameterized.named_parameters(list_datasets_on_hf_gcp_parameters(with_config=True))
class TestDatasetOnHfGcp(TestCase):
    dataset = None
    config_name = None

    def test_dataset_info_available(self, dataset, config_name):
        with TemporaryDirectory() as tmp_dir:
            dataset_module = dataset_module_factory(dataset, cache_dir=tmp_dir)

            builder_cls = import_main_class(dataset_module.module_path, dataset=True)

            builder_instance: DatasetBuilder = builder_cls(
                cache_dir=tmp_dir,
                config_name=config_name,
                hash=dataset_module.hash,
            )

            dataset_info_url = "/".join(
                [
                    HF_GCP_BASE_URL,
                    builder_instance._relative_data_dir(with_hash=False).replace(os.sep, "/"),
                    config.DATASET_INFO_FILENAME,
                ]
            )
            datset_info_path = cached_path(dataset_info_url, cache_dir=tmp_dir)
            self.assertTrue(os.path.exists(datset_info_path))


@pytest.mark.integration
def test_as_dataset_from_hf_gcs(tmp_path_factory):
    tmp_dir = tmp_path_factory.mktemp("test_hf_gcp") / "test_wikipedia_simple"
    dataset_module = dataset_module_factory("wikipedia", cache_dir=tmp_dir)
    builder_cls = import_main_class(dataset_module.module_path)
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=tmp_dir,
        config_name="20220301.frr",
        hash=dataset_module.hash,
    )
    # use the HF cloud storage, not the original download_and_prepare that uses apache-beam
    builder_instance._download_and_prepare = None
    builder_instance.download_and_prepare()
    ds = builder_instance.as_dataset()
    assert ds


@pytest.mark.integration
def test_as_streaming_dataset_from_hf_gcs(tmp_path):
    dataset_module = dataset_module_factory("wikipedia", cache_dir=tmp_path)
    builder_cls = import_main_class(dataset_module.module_path, dataset=True)
    builder_instance: DatasetBuilder = builder_cls(
        cache_dir=tmp_path,
        config_name="20220301.frr",
        hash=dataset_module.hash,
    )
    ds = builder_instance.as_streaming_dataset()
    assert ds
    assert isinstance(ds, IterableDatasetDict)
    assert "train" in ds
    assert isinstance(ds["train"], IterableDataset)
    assert next(iter(ds["train"]))
