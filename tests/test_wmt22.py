import os
import pytest
from local_datasets.wmt22.wmt22_dataset import WMT22Dataset

def test_wmt22_loads():
    dataset_path = os.path.join("local_datasets", "wmt22", "dummy_data")
    wmt22 = WMT22Dataset(dataset_path)
    ds = wmt22.load()
    assert "train" in ds
    assert "validation" in ds
    assert "test" in ds
    assert len(ds["train"]) > 0
    assert len(ds["validation"]) > 0
    assert len(ds["test"]) > 0

def test_empty_lines_ignored():
    dataset_path = os.path.join("local_datasets", "wmt22", "dummy_data")
    wmt22 = WMT22Dataset(dataset_path)
    ds = wmt22.load()
    for split in ["train", "validation", "test"]:
        assert all("source" in ex and "target" in ex for ex in ds[split])

def test_num_examples_matches_lines():
    dataset_path = os.path.join("local_datasets", "wmt22", "dummy_data")
    wmt22 = WMT22Dataset(dataset_path)
    ds = wmt22.load()

    for split in ["train", "validation", "test"]:
        file_path = os.path.join(dataset_path, f"{split}.tsv")
        with open(file_path, encoding="utf-8") as f:
            n_lines = sum(
                1 for line in f if line.strip() and len(line.split("\t")) == 2
            )
        assert len(ds[split]) == n_lines
