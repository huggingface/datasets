import pytest

from datasets import Dataset, Features, LargeList, List, Sequence, Value, load_from_disk


@pytest.mark.parametrize("kind", ["list", "fixed", "large"])
def test_sequence_list_disk_roundtrip(tmp_path, kind):
    subfeature = (
        LargeList(Value("int64")) if kind == "large" else List(Value("int64"), length=2 if kind == "fixed" else -1)
    )
    features = Features({"col": Sequence({"tokens": subfeature, "labels": Value("string")})})
    data = {"col": [{"tokens": [1, 2], "labels": ["a"]}, {"tokens": [3, 4], "labels": ["b", "c"]}]}
    dataset = Dataset.from_dict(data, features=features)
    dataset.save_to_disk(tmp_path / "arrow")
    restored = load_from_disk(tmp_path / "arrow")
    assert restored.to_dict() == data
    assert restored.features["col"]["tokens"] == subfeature
    path = tmp_path / "data.parquet"
    dataset.to_parquet(path)
    parquet = Dataset.from_parquet(str(path))
    assert parquet.to_dict() == data
    assert parquet.features == features
    assert features["col"]["tokens"] == subfeature
