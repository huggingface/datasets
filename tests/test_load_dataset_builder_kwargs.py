import pytest

from datasets.load import load_dataset_builder


def test_load_dataset_builder_does_not_fail_with_duplicate_builder_kwargs(tmp_path):
    # Regression test for https://github.com/huggingface/datasets/issues/4910
    # Some module factories provide `base_path` in `builder_kwargs`, and users can also pass `base_path`
    # via `config_kwargs`, which used to raise:
    #   TypeError: ... got multiple values for keyword argument 'base_path'
    train_csv = tmp_path / "train.csv"
    train_csv.write_text("col\n1\n", encoding="utf-8")

    custom_base_path = str(tmp_path / "custom_base_path")
    builder = load_dataset_builder("csv", data_files=str(train_csv), base_path=custom_base_path)
    assert builder.base_path == custom_base_path

