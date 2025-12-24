import lance
import pyarrow as pa
import pytest

from datasets import load_dataset


@pytest.fixture
def lance_dataset(tmp_path) -> str:
    data = pa.table(
        {
            "id": pa.array([1, 2, 3, 4]),
            "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            "text": pa.array(["a", "b", "c", "d"]),
            "vector": pa.FixedSizeListArray.from_arrays(pa.array([0.1] * 16, pa.float32()), list_size=4),
        }
    )
    dataset_path = tmp_path / "test_dataset.lance"
    lance.write_dataset(data, dataset_path)
    return str(dataset_path)


@pytest.fixture
def lance_hf_dataset(tmp_path) -> str:
    data = pa.table(
        {
            "id": pa.array([1, 2, 3, 4]),
            "value": pa.array([10.0, 20.0, 30.0, 40.0]),
            "text": pa.array(["a", "b", "c", "d"]),
            "vector": pa.FixedSizeListArray.from_arrays(pa.array([0.1] * 16, pa.float32()), list_size=4),
        }
    )
    dataset_dir = tmp_path / "data" / "train.lance"
    dataset_dir.parent.mkdir(parents=True, exist_ok=True)
    lance.write_dataset(data, dataset_dir)
    with open(tmp_path / "README.md", "w") as f:
        f.write("""---
size_categories:
- 1M<n<10M
source_datasets:
- lance_test
configs:
- config_name: default
  dataset_dirs:
  - split: train
    path:
    - "data/train.lance"
---
    # Test Lance Dataset\n\n
    # My Markdown is fancier\n
""")

    return str(tmp_path)


def test_directly_load(lance_dataset):
    dataset_dict = load_dataset(lance_dataset)
    assert "train" in dataset_dict.keys()

    dataset = dataset_dict["train"]
    assert "id" in dataset.column_names
    assert "value" in dataset.column_names
    assert "text" in dataset.column_names
    assert "vector" in dataset.column_names
    ids = dataset["id"]
    assert ids == [1, 2, 3, 4]


def test_load_hf_dataset(lance_hf_dataset):
    dataset_dict = load_dataset(lance_hf_dataset)
    assert "train" in dataset_dict.keys()

    dataset = dataset_dict["train"]
    assert "id" in dataset.column_names
    assert "value" in dataset.column_names
    assert "text" in dataset.column_names
    assert "vector" in dataset.column_names
    ids = dataset["id"]
    assert ids == [1, 2, 3, 4]


def test_load_with_columns(lance_dataset):
    dataset_dict = load_dataset(lance_dataset, columns=["id", "text"])
    assert "train" in dataset_dict.keys()

    dataset = dataset_dict["train"]
    assert "id" in dataset.column_names
    assert "text" in dataset.column_names
    assert "value" not in dataset.column_names
    assert "vector" not in dataset.column_names
    ids = dataset["id"]
    assert ids == [1, 2, 3, 4]
    text = dataset["text"]
    assert text == ["a", "b", "c", "d"]
    assert "value" not in dataset.column_names
