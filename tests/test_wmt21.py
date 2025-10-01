import os
import pytest
from local_datasets.wmt21.wmt21_dataset import WMT21Dataset

# Path to dummy data
DATASET_PATH = os.path.join("local_datasets", "wmt21", "dummy_data")


def test_wmt21_loads():
    """Test that the WMT21 dataset loads correctly for all splits."""
    wmt21 = WMT21Dataset(DATASET_PATH)
    ds = wmt21.load()

    # Ensure splits exist
    for split in ["train", "validation", "test"]:
        assert split in ds, f"{split} split missing"
        assert len(ds[split]) > 0, f"{split} split is empty"


def test_empty_lines_ignored():
    """Test that empty lines in .tsv files are ignored."""
    # Add a temporary empty line in train.tsv
    train_file = os.path.join(DATASET_PATH, "train.tsv")
    with open(train_file, "a", encoding="utf-8") as f:
        f.write("\n")

    wmt21 = WMT21Dataset(DATASET_PATH)
    ds = wmt21.load()

    # No extra empty example should be added
    assert all(
        e["source"].strip() != "" and e["target"].strip() != "" for e in ds["train"]
    )

    # Clean up: remove the empty line
    with open(train_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    with open(train_file, "w", encoding="utf-8") as f:
        f.writelines(lines[:-1])


def test_num_examples_matches_lines():
    """Check that number of examples matches the number of valid lines in each .tsv."""
    wmt21 = WMT21Dataset(DATASET_PATH)
    ds = wmt21.load()

    for split in ["train", "validation", "test"]:
        file_path = os.path.join(DATASET_PATH, f"{split}.tsv")
        with open(file_path, encoding="utf-8") as f:
            n_lines = sum(
                1 for line in f if line.strip() and len(line.split("\t")) == 2
            )
        assert len(ds[split]) == n_lines, f"{split} split length mismatch"
