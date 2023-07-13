import os

import pytest

from datasets import (
    get_dataset_config_info,
    get_dataset_config_names,
    get_dataset_infos,
    get_dataset_split_names,
    inspect_dataset,
    inspect_metric,
)


pytestmark = pytest.mark.integration


@pytest.mark.parametrize("path", ["paws", "csv"])
def test_inspect_dataset(path, tmp_path):
    inspect_dataset(path, tmp_path)
    script_name = path + ".py"
    assert script_name in os.listdir(tmp_path)
    assert "__pycache__" not in os.listdir(tmp_path)


@pytest.mark.filterwarnings("ignore:inspect_metric is deprecated:FutureWarning")
@pytest.mark.filterwarnings("ignore:metric_module_factory is deprecated:FutureWarning")
@pytest.mark.parametrize("path", ["accuracy"])
def test_inspect_metric(path, tmp_path):
    inspect_metric(path, tmp_path)
    script_name = path + ".py"
    assert script_name in os.listdir(tmp_path)
    assert "__pycache__" not in os.listdir(tmp_path)


@pytest.mark.parametrize(
    "path, config_name, expected_splits",
    [
        ("squad", "plain_text", ["train", "validation"]),
        ("dalle-mini/wit", "default", ["train"]),
        ("paws", "labeled_final", ["train", "test", "validation"]),
    ],
)
def test_get_dataset_config_info(path, config_name, expected_splits):
    info = get_dataset_config_info(path, config_name=config_name)
    assert info.config_name == config_name
    assert list(info.splits.keys()) == expected_splits


@pytest.mark.parametrize(
    "path, config_name, expected_exception",
    [
        ("paws", None, ValueError),
    ],
)
def test_get_dataset_config_info_error(path, config_name, expected_exception):
    with pytest.raises(expected_exception):
        get_dataset_config_info(path, config_name=config_name)


@pytest.mark.parametrize(
    "path, expected",
    [
        ("squad", ["plain_text"]),
        ("acronym_identification", ["default"]),
        ("lhoestq/squad", ["plain_text"]),
        ("lhoestq/test", ["default"]),
        ("lhoestq/demo1", ["default"]),
        ("dalle-mini/wit", ["default"]),
        ("datasets-maintainers/audiofolder_no_configs_in_metadata", ["default"]),
        ("datasets-maintainers/audiofolder_single_config_in_metadata", ["custom"]),
        ("datasets-maintainers/audiofolder_two_configs_in_metadata", ["v1", "v2"]),
    ],
)
def test_get_dataset_config_names(path, expected):
    config_names = get_dataset_config_names(path)
    assert config_names == expected


@pytest.mark.parametrize(
    "path, expected_configs, expected_splits_in_first_config",
    [
        ("squad", ["plain_text"], ["train", "validation"]),
        ("dalle-mini/wit", ["default"], ["train"]),
        ("paws", ["labeled_final", "labeled_swap", "unlabeled_final"], ["train", "test", "validation"]),
    ],
)
def test_get_dataset_info(path, expected_configs, expected_splits_in_first_config):
    infos = get_dataset_infos(path)
    assert list(infos.keys()) == expected_configs
    expected_config = expected_configs[0]
    assert expected_config in infos
    info = infos[expected_config]
    assert info.config_name == expected_config
    assert list(info.splits.keys()) == expected_splits_in_first_config


@pytest.mark.parametrize(
    "path, expected_config, expected_splits",
    [
        ("squad", "plain_text", ["train", "validation"]),
        ("dalle-mini/wit", "default", ["train"]),
        ("paws", "labeled_final", ["train", "test", "validation"]),
    ],
)
def test_get_dataset_split_names(path, expected_config, expected_splits):
    infos = get_dataset_infos(path)
    assert expected_config in infos
    info = infos[expected_config]
    assert info.config_name == expected_config
    assert list(info.splits.keys()) == expected_splits


@pytest.mark.parametrize(
    "path, config_name, expected_exception",
    [
        ("paws", None, ValueError),
    ],
)
def test_get_dataset_split_names_error(path, config_name, expected_exception):
    with pytest.raises(expected_exception):
        get_dataset_split_names(path, config_name=config_name)
