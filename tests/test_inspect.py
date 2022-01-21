import pytest

from datasets import get_dataset_config_names


@pytest.mark.parametrize(
    "path, expected",
    [
        ("squad", "plain_text"),
        ("acronym_identification", "default"),
        ("lhoestq/squad", "plain_text"),
        ("lhoestq/test", "default"),
        ("lhoestq/demo1", "lhoestq--demo1"),
    ],
)
def test_get_dataset_config_names(path, expected):
    config_names = get_dataset_config_names(path)
    assert expected in config_names
