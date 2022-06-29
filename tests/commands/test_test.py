import json
import os
from collections import namedtuple
from dataclasses import dataclass

from packaging import version

from datasets import config
from datasets.commands.test import TestCommand


if config.PY_VERSION >= version.parse("3.7"):
    _TestCommandArgs = namedtuple(
        "_TestCommandArgs",
        [
            "dataset",
            "name",
            "cache_dir",
            "data_dir",
            "all_configs",
            "save_infos",
            "ignore_verifications",
            "force_redownload",
            "clear_cache",
        ],
        defaults=[None, None, None, False, False, False, False, False],
    )
else:

    @dataclass
    class _TestCommandArgs:
        dataset: str
        name: str = None
        cache_dir: str = None
        data_dir: str = None
        all_configs: bool = False
        save_infos: bool = False
        ignore_verifications: bool = False
        force_redownload: bool = False
        clear_cache: bool = False

        def __iter__(self):
            return iter(self.__dict__.values())


def test_test_command(dataset_loading_script_dir):
    args = _TestCommandArgs(dataset=dataset_loading_script_dir, all_configs=True, save_infos=True)
    test_command = TestCommand(*args)
    test_command.run()
    dataset_infos_path = os.path.join(dataset_loading_script_dir, config.DATASETDICT_INFOS_FILENAME)
    assert os.path.exists(dataset_infos_path)
    with open(dataset_infos_path, encoding="utf-8") as f:
        dataset_infos = json.load(f)
    expected_dataset_infos = {
        "default": {
            "description": "",
            "citation": "",
            "homepage": "",
            "license": "",
            "features": {
                "tokens": {
                    "feature": {"dtype": "string", "id": None, "_type": "Value"},
                    "length": -1,
                    "id": None,
                    "_type": "Sequence",
                },
                "ner_tags": {
                    "feature": {
                        "num_classes": 7,
                        "names": ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"],
                        "id": None,
                        "_type": "ClassLabel",
                    },
                    "length": -1,
                    "id": None,
                    "_type": "Sequence",
                },
                "langs": {
                    "feature": {"dtype": "string", "id": None, "_type": "Value"},
                    "length": -1,
                    "id": None,
                    "_type": "Sequence",
                },
                "spans": {
                    "feature": {"dtype": "string", "id": None, "_type": "Value"},
                    "length": -1,
                    "id": None,
                    "_type": "Sequence",
                },
            },
            "post_processed": None,
            "supervised_keys": None,
            "task_templates": None,
            "builder_name": "__dummy_dataset1__",
            "config_name": "default",
            "version": {"version_str": "0.0.0", "description": None, "major": 0, "minor": 0, "patch": 0},
            "splits": {
                "train": {
                    "name": "train",
                    "num_bytes": 2351591,
                    "num_examples": 10000,
                    "dataset_name": "__dummy_dataset1__",
                },
                "validation": {
                    "name": "validation",
                    "num_bytes": 238446,
                    "num_examples": 1000,
                    "dataset_name": "__dummy_dataset1__",
                },
            },
            "download_checksums": {
                "https://huggingface.co/datasets/albertvillanova/tests-raw-jsonl/resolve/main/wikiann-bn-train.jsonl": {
                    "num_bytes": 3578339,
                    "checksum": "6fbe6dbdcb3c9c3a98b0ab4d56b1c8b73baab9293d603064a5ab5230ab4f366b",
                },
                "https://huggingface.co/datasets/albertvillanova/tests-raw-jsonl/resolve/main/wikiann-bn-validation.jsonl": {
                    "num_bytes": 362341,
                    "checksum": "2ddd0c090a8ccb721d7aa8477ed7323750683822c247015d5cfab1af1c8c8b3f",
                },
            },
            "download_size": 3940680,
            "post_processing_size": None,
            "dataset_size": 2590037,
            "size_in_bytes": 6530717,
        }
    }
    assert dataset_infos.keys() == expected_dataset_infos.keys()
    assert dataset_infos["default"].keys() == expected_dataset_infos["default"].keys()
    for key in dataset_infos["default"].keys():
        if key in [
            "description",
            "citation",
            "homepage",
            "license",
            "features",
            "post_processed",
            "supervised_keys",
            "task_templates",
            "builder_name",
            "config_name",
            "version",
            "download_checksums",
            "download_size",
            "post_processing_size",
        ]:
            assert dataset_infos["default"][key] == expected_dataset_infos["default"][key]
        elif key in ["dataset_size", "size_in_bytes"]:
            assert round(dataset_infos["default"][key] / 10**5) == round(
                expected_dataset_infos["default"][key] / 10**5
            )
        elif key == "splits":
            assert dataset_infos["default"]["splits"].keys() == expected_dataset_infos["default"]["splits"].keys()
            for split in dataset_infos["default"]["splits"].keys():
                assert (
                    dataset_infos["default"]["splits"][split].keys()
                    == expected_dataset_infos["default"]["splits"][split].keys()
                )
                for subkey in dataset_infos["default"]["splits"][split].keys():
                    if subkey == "num_bytes":
                        assert round(dataset_infos["default"]["splits"][split][subkey] / 10**2) == round(
                            expected_dataset_infos["default"]["splits"][split][subkey] / 10**2
                        )
                    else:
                        assert (
                            dataset_infos["default"]["splits"][split][subkey]
                            == expected_dataset_infos["default"]["splits"][split][subkey]
                        )
