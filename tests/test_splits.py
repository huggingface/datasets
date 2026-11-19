import inspect

import pytest

from datasets.splits import (
    NamedSplit,
    NamedSplitAll,
    PercentSlice,
    SlicedSplitInfo,
    Split,
    SplitDict,
    SplitInfo,
    SplitReadInstruction,
)
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


def test_named_split_inequality():
    # Used while building the docs, when set as a default parameter value in a function signature
    assert Split.TRAIN != inspect.Parameter.empty


def test_custom_split_creation():
    assert Split("custom") == NamedSplit("custom")
    assert isinstance(Split("all"), NamedSplitAll)
    assert Split.TRAIN == "train"
    assert Split.TRAIN != "test"
    assert Split.TRAIN != 123


def test_percent_slice_validation():
    assert PercentSlice[10:20] == slice(10, 20)
    with pytest.raises(ValueError, match="datasets.percent should only be called with slice"):
        _ = PercentSlice[42]


def test_subsplit_validation():
    # Multiple arguments error
    with pytest.raises(ValueError, match="Only one argument of subsplit should be set"):
        Split.TRAIN.subsplit(k=2, percent=slice(0, 50))

    # Invalid k values (> 100 or negative)
    with pytest.raises(ValueError, match="Subsplit k should be between 0 and 100"):
        Split.TRAIN.subsplit(k=101)

    with pytest.raises(ValueError, match="Subsplit k should be between 0 and 100"):
        Split.TRAIN.subsplit(k=-5)

    # Invalid argument type
    with pytest.raises(ValueError, match="Invalid split argument"):
        Split.TRAIN.subsplit("invalid_arg")


def test_split_info_repr():
    info = SplitInfo(name="train", num_bytes=100, num_examples=10)
    rep = repr(info)
    assert "SplitInfo" in rep
    assert "name='train'" in rep
    assert "num_bytes=100" in rep
    assert "num_examples=10" in rep


def test_split_read_instruction_double_slice():
    instruction = SplitReadInstruction()
    sliced = SlicedSplitInfo(split_info=SplitInfo(name="train"), slice_value=slice(0, 50))
    instruction.add(sliced)
    with pytest.raises(ValueError, match="which has already been sliced"):
        _ = instruction[slice(10, 20)]
