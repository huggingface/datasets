import os

import pytest
import yaml

from datasets.features.features import Features, Value
from datasets.info import DatasetInfo, DatasetInfosDict


@pytest.mark.parametrize(
    "files",
    [
        ["full:README.md", "dataset_infos.json"],
        ["empty:README.md", "dataset_infos.json"],
        ["dataset_infos.json"],
        ["full:README.md"],
    ],
)
def test_from_dir(files, tmp_path_factory):
    dataset_infos_dir = tmp_path_factory.mktemp("dset_infos_dir")
    if "full:README.md" in files:
        with open(dataset_infos_dir / "README.md", "w") as f:
            f.write("---\ndataset_info:\n  dataset_size: 42\n---")
    if "empty:README.md" in files:
        with open(dataset_infos_dir / "README.md", "w") as f:
            f.write("")
    # we want to support dataset_infos.json for backward compatibility
    if "dataset_infos.json" in files:
        with open(dataset_infos_dir / "dataset_infos.json", "w") as f:
            f.write('{"default": {"dataset_size": 42}}')
    dataset_infos = DatasetInfosDict.from_directory(dataset_infos_dir)
    assert dataset_infos
    assert dataset_infos["default"].dataset_size == 42


@pytest.mark.parametrize(
    "dataset_info",
    [
        DatasetInfo(),
        DatasetInfo(
            description="foo",
            features=Features({"a": Value("int32")}),
            builder_name="builder",
            config_name="config",
            version="1.0.0",
            splits=[{"name": "train"}],
            download_size=42,
        ),
    ],
)
def test_dataset_info_dump_and_reload(tmp_path, dataset_info: DatasetInfo):
    tmp_path = str(tmp_path)
    dataset_info.write_to_directory(tmp_path)
    reloaded = DatasetInfo.from_directory(tmp_path)
    assert dataset_info == reloaded
    assert os.path.exists(os.path.join(tmp_path, "dataset_info.json"))


def test_dataset_info_to_yaml_dict():
    dataset_info = DatasetInfo(
        description="foo",
        citation="bar",
        homepage="https://foo.bar",
        license="CC0",
        features=Features({"a": Value("int32")}),
        post_processed={},
        supervised_keys=(),
        task_templates=[],
        builder_name="builder",
        config_name="config",
        version="1.0.0",
        splits=[{"name": "train", "num_examples": 42}],
        download_checksums={},
        download_size=1337,
        post_processing_size=442,
        dataset_size=1234,
        size_in_bytes=1337 + 442 + 1234,
    )
    dataset_info_yaml_dict = dataset_info._to_yaml_dict()
    assert sorted(dataset_info_yaml_dict) == sorted(DatasetInfo._INCLUDED_INFO_IN_YAML)
    for key in DatasetInfo._INCLUDED_INFO_IN_YAML:
        assert key in dataset_info_yaml_dict
        assert isinstance(dataset_info_yaml_dict[key], (list, dict, int, str))
    dataset_info_yaml = yaml.safe_dump(dataset_info_yaml_dict)
    reloaded = yaml.safe_load(dataset_info_yaml)
    assert dataset_info_yaml_dict == reloaded


def test_dataset_info_to_yaml_dict_empty():
    dataset_info = DatasetInfo()
    dataset_info_yaml_dict = dataset_info._to_yaml_dict()
    assert dataset_info_yaml_dict == {}


@pytest.mark.parametrize(
    "dataset_infos_dict",
    [
        DatasetInfosDict(),
        DatasetInfosDict({"default": DatasetInfo()}),
        DatasetInfosDict({"my_config_name": DatasetInfo()}),
        DatasetInfosDict(
            {
                "default": DatasetInfo(
                    description="foo",
                    features=Features({"a": Value("int32")}),
                    builder_name="builder",
                    config_name="config",
                    version="1.0.0",
                    splits=[{"name": "train"}],
                    download_size=42,
                )
            }
        ),
        DatasetInfosDict(
            {
                "v1": DatasetInfo(dataset_size=42),
                "v2": DatasetInfo(dataset_size=1337),
            }
        ),
    ],
)
def test_dataset_infos_dict_dump_and_reload(tmp_path, dataset_infos_dict: DatasetInfosDict):
    tmp_path = str(tmp_path)
    dataset_infos_dict.write_to_directory(tmp_path)
    reloaded = DatasetInfosDict.from_directory(tmp_path)

    # the config_name of the dataset_infos_dict take over the attribute
    for config_name, dataset_info in dataset_infos_dict.items():
        dataset_info.config_name = config_name
        # the yaml representation doesn't include fields like description or citation
        # so we just test that we can recover what we can from the yaml
        dataset_infos_dict[config_name] = DatasetInfo._from_yaml_dict(dataset_info._to_yaml_dict())
    assert dataset_infos_dict == reloaded

    if dataset_infos_dict:
        assert os.path.exists(os.path.join(tmp_path, "README.md"))
