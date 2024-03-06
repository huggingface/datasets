import os
from collections import namedtuple

import pytest

from datasets import ClassLabel, Features, Sequence, Value
from datasets.commands.test import TestCommand
from datasets.info import DatasetInfo, DatasetInfosDict


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
        "num_proc",
    ],
    defaults=[None, None, None, False, False, False, False, False, None],
)


def is_1percent_close(source, target):
    return (abs(source - target) / target) < 0.01


@pytest.mark.integration
def test_test_command(dataset_loading_script_dir):
    args = _TestCommandArgs(dataset=dataset_loading_script_dir, all_configs=True, save_infos=True)
    test_command = TestCommand(*args)
    test_command.run()
    dataset_readme_path = os.path.join(dataset_loading_script_dir, "README.md")
    assert os.path.exists(dataset_readme_path)
    dataset_infos = DatasetInfosDict.from_directory(dataset_loading_script_dir)
    expected_dataset_infos = DatasetInfosDict(
        {
            "default": DatasetInfo(
                features=Features(
                    {
                        "tokens": Sequence(Value("string")),
                        "ner_tags": Sequence(
                            ClassLabel(names=["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC"])
                        ),
                        "langs": Sequence(Value("string")),
                        "spans": Sequence(Value("string")),
                    }
                ),
                splits=[
                    {
                        "name": "train",
                        "num_bytes": 2351563,
                        "num_examples": 10000,
                    },
                    {
                        "name": "validation",
                        "num_bytes": 238418,
                        "num_examples": 1000,
                    },
                ],
                download_size=3940680,
                dataset_size=2589981,
            )
        }
    )
    assert dataset_infos.keys() == expected_dataset_infos.keys()
    for key in DatasetInfo._INCLUDED_INFO_IN_YAML:
        result, expected = getattr(dataset_infos["default"], key), getattr(expected_dataset_infos["default"], key)
        if key == "num_bytes":
            assert is_1percent_close(result, expected)
        elif key == "splits":
            assert list(result) == list(expected)
            for split in result:
                assert result[split].name == expected[split].name
                assert result[split].num_examples == expected[split].num_examples
                assert is_1percent_close(result[split].num_bytes, expected[split].num_bytes)
        else:
            result == expected
