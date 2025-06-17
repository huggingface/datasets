import pytest
from datasets.load import load_dataset_builder

def test_duplicate_builder_and_config_kwargs():
    builder_kwargs = {"foo-key": 1}
    config_kwargs  = {"foo-key": 2}
    with pytest.raises(TypeError) as excinfo:
        load_dataset_builder(
            "csv",
            builder_kwargs=builder_kwargs,
            config_kwargs=config_kwargs,
        )
    msg = str(excinfo.value).lower()
    assert "duplicate keys" in msg
    assert "builder_kwargs" in msg
    assert "config_kwargs" in msg