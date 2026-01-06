import lance
import numpy as np
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
    lance.write_dataset(data[:2], tmp_path / "data" / "test.lance")

    with open(tmp_path / "README.md", "w") as f:
        f.write("""---
size_categories:
- 1M<n<10M
source_datasets:
- lance_test
---
    # Test Lance Dataset\n\n
    # My Markdown is fancier\n
""")

    return str(tmp_path)


def test_load_lance_dataset(lance_dataset):
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
    dataset_dict = load_dataset(lance_hf_dataset, columns=["id", "text"])
    assert "train" in dataset_dict.keys()
    assert "test" in dataset_dict.keys()
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


def test_load_vectors(lance_hf_dataset):
    dataset_dict = load_dataset(lance_hf_dataset, columns=["vector"])
    assert "train" in dataset_dict.keys()
    dataset = dataset_dict["train"]

    assert "vector" in dataset.column_names
    vectors = dataset.data["vector"].combine_chunks().values.to_numpy(zero_copy_only=False)
    assert np.allclose(vectors, np.full(16, 0.1))


def test_load_stream_datasets():
    dataset = load_dataset("lance-format/openvid-lance", split="train", streaming=True)
    assert "id" in dataset.column_names
    ids = [example["id"] for example in dataset]
    assert ids == [1, 2, 3, 4]


@pytest.mark.parametrize("streaming", [False, True])
def test_load_lance_streaming_modes(lance_hf_dataset, streaming):
    """Test loading Lance dataset in both streaming and non-streaming modes."""
    from datasets import IterableDataset

    ds = load_dataset(lance_hf_dataset, split="train", streaming=streaming)
    if streaming:
        assert isinstance(ds, IterableDataset)
        items = list(ds)
    else:
        items = list(ds)
    assert len(items) == 4
    assert all("id" in item for item in items)


def test_streaming_with_columns(lance_hf_dataset):
    """Test streaming mode with column selection."""
    ds = load_dataset(lance_hf_dataset, split="train", streaming=True, columns=["id", "text"])
    first = next(iter(ds))
    assert "id" in first
    assert "text" in first
    assert "value" not in first
    assert "vector" not in first
