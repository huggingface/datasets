import pytest

from datasets.splits import SplitDict, SplitInfo
from datasets.utils.py_utils import asdict


@pytest.mark.parametrize(
    "split_dict",
    [
        SplitDict(),
        SplitDict({"train": SplitInfo(name="train", num_bytes=1337, num_examples=42, dataset_name="my_dataset")}),
        SplitDict({"train": SplitInfo(name="train", num_bytes=1337, num_examples=42)}),
        SplitDict({"train": SplitInfo()}),
    ],
)
def test_split_dict_to_yaml_list(split_dict: SplitDict):
    split_dict_yaml_list = split_dict._to_yaml_list()
    assert len(split_dict_yaml_list) == len(split_dict)
    reloaded = SplitDict._from_yaml_list(split_dict_yaml_list)
    for split_name, split_info in split_dict.items():
        # dataset_name field is deprecated, and is therefore not part of the YAML dump
        split_info.dataset_name = None
        # the split name of split_dict takes over the name of the split info object
        split_info.name = split_name
    assert split_dict == reloaded


@pytest.mark.parametrize(
    "split_info", [SplitInfo(), SplitInfo(dataset_name=None), SplitInfo(dataset_name="my_dataset")]
)
def test_split_dict_asdict_has_dataset_name(split_info):
    # For backward compatibility, we need asdict(split_dict) to return split info dictrionaries with the "dataset_name"
    # field even if it's deprecated. This way old versionso of `datasets` can still reload dataset_infos.json files
    split_dict_asdict = asdict(SplitDict({"train": split_info}))
    assert "dataset_name" in split_dict_asdict["train"]
    assert split_dict_asdict["train"]["dataset_name"] == split_info.dataset_name
