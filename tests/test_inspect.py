import pytest

from datasets import get_dataset_config_names, get_dataset_infos


@pytest.mark.parametrize(
    "path, expected",
    [
        ("squad", "plain_text"),
        ("acronym_identification", "default"),
        ("lhoestq/squad", "plain_text"),
        ("lhoestq/test", "default"),
        ("lhoestq/demo1", "lhoestq--demo1"),
        ("dalle-mini/wit", "dalle-mini--wit"),
    ],
)
def test_get_dataset_config_names(path, expected):
    config_names = get_dataset_config_names(path)
    assert expected in config_names


@pytest.mark.parametrize(
    "path, expected_config, expected_splits",
    [("squad", "plain_text", ["train", "validation"]), ("dalle-mini/wit", "dalle-mini--wit", ["train"])],
)
def test_get_dataset_info(path, expected_config, expected_splits):
    infos = get_dataset_infos(path)
    assert expected_config in infos
    info = infos[expected_config]
    assert info.config_name == expected_config
    assert list(info.splits.keys()) == expected_splits
