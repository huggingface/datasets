import pytest

from datasets.exceptions import DatasetNotFoundError
from datasets.inspect import (
    get_dataset_config_info,
    get_dataset_config_names,
    get_dataset_default_config_name,
    get_dataset_infos,
    get_dataset_split_names,
)


pytestmark = pytest.mark.integration


@pytest.mark.parametrize(
    "path, config_name, expected_splits",
    [
        ("rajpurkar/squad", "plain_text", ["train", "validation"]),
        ("dalle-mini/wit", "default", ["train"]),
        ("paws", "labeled_final", ["train", "test", "validation"]),
    ],
)
def test_get_dataset_config_info(path, config_name, expected_splits):
    info = get_dataset_config_info(path, config_name=config_name)
    assert info.config_name == config_name
    assert list(info.splits.keys()) == expected_splits


def test_get_dataset_config_info_private(hf_token, hf_private_dataset_repo_txt_data):
    info = get_dataset_config_info(hf_private_dataset_repo_txt_data, config_name="default", token=hf_token)
    assert list(info.splits.keys()) == ["train"]


@pytest.mark.parametrize(
    "path, config_name, expected_exception",
    [
        ("paws", None, ValueError),
        # non-existing, gated, private:
        ("hf-internal-testing/non-existing-dataset", "default", DatasetNotFoundError),
        ("hf-internal-testing/gated_dataset_with_data_files", "default", DatasetNotFoundError),
        ("hf-internal-testing/private_dataset_with_data_files", "default", DatasetNotFoundError),
        ("hf-internal-testing/gated_dataset_with_script", "default", DatasetNotFoundError),
        ("hf-internal-testing/private_dataset_with_script", "default", DatasetNotFoundError),
    ],
)
def test_get_dataset_config_info_raises(path, config_name, expected_exception):
    kwargs = {"trust_remote_code": True} if path.endswith("_with_script") else {}
    with pytest.raises(expected_exception):
        get_dataset_config_info(path, config_name=config_name, **kwargs)


@pytest.mark.parametrize(
    "path, expected",
    [
        ("acronym_identification", ["default"]),
        ("rajpurkar/squad", ["plain_text"]),
        ("hf-internal-testing/dataset_with_script", ["default"]),
        ("dalle-mini/wit", ["default"]),
        ("hf-internal-testing/librispeech_asr_dummy", ["clean"]),
        ("hf-internal-testing/audiofolder_no_configs_in_metadata", ["default"]),
        ("hf-internal-testing/audiofolder_single_config_in_metadata", ["custom"]),
        ("hf-internal-testing/audiofolder_two_configs_in_metadata", ["v1", "v2"]),
    ],
)
def test_get_dataset_config_names(path, expected):
    config_names = get_dataset_config_names(path, trust_remote_code=True)
    assert config_names == expected


@pytest.mark.parametrize(
    "path, expected",
    [
        ("acronym_identification", "default"),
        ("rajpurkar/squad", "plain_text"),
        ("hf-internal-testing/dataset_with_script", "default"),
        ("dalle-mini/wit", "default"),
        ("hf-internal-testing/librispeech_asr_dummy", "clean"),
        ("hf-internal-testing/audiofolder_no_configs_in_metadata", "default"),
        ("hf-internal-testing/audiofolder_single_config_in_metadata", "custom"),
        ("hf-internal-testing/audiofolder_two_configs_in_metadata", None),
    ],
)
def test_get_dataset_default_config_name(path, expected):
    default_config_name = get_dataset_default_config_name(path, trust_remote_code=True)
    if expected:
        assert default_config_name == expected
    else:
        assert default_config_name is None


@pytest.mark.parametrize(
    "path, expected_configs, expected_splits_in_first_config",
    [
        ("rajpurkar/squad", ["plain_text"], ["train", "validation"]),
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
        ("rajpurkar/squad", "plain_text", ["train", "validation"]),
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
