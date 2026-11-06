import pytest

from datasets import ClassLabel, Dataset, Features, List, Value, load_from_disk


@pytest.mark.parametrize("value", [2**63, 2**64 - 1])
def test_add_item_preserves_declared_uint64(value):
    feature = Value("uint64")
    first = 1
    features = Features({"hashes": feature})
    dataset = Dataset.from_dict({"hashes": [first]}, features=features)
    source_metadata = dataset.data.schema.metadata
    source_fingerprint = dataset._fingerprint

    result = dataset.add_item({"hashes": value})

    assert result.to_dict() == {"hashes": [first, value]}
    assert result.features == features
    assert Features.from_arrow_schema(result.data.schema) == features
    assert result._fingerprint != source_fingerprint
    assert dataset.to_dict() == {"hashes": [first]}
    assert dataset.features == features
    assert dataset.data.schema.metadata == source_metadata


def test_add_item_uint64_keeps_new_columns_and_other_feature_alignment():
    features = Features({"hash": Value("uint64"), "label": ClassLabel(names=["no", "yes"]), "extra": Value("null")})
    dataset = Dataset.from_dict({"hash": [1], "label": [0], "extra": [None]}, features=features)

    result = dataset.add_item({"hash": 2**64 - 1, "label": 1, "extra": None, "new": {"text": "added"}})

    assert result.to_dict() == {
        "hash": [1, 2**64 - 1],
        "label": [0, 1],
        "extra": [None, None],
        "new": [None, {"text": "added"}],
    }
    assert result.features == Features(
        {"hash": Value("uint64"), "label": features["label"], "extra": Value("null"), "new": {"text": Value("string")}}
    )
    assert dataset.to_dict() == {"hash": [1], "label": [0], "extra": [None]}


def test_add_item_uint64_with_subset_of_columns_and_indices():
    dataset = Dataset.from_dict(
        {"hash": [1, 2], "text": ["one", "two"]}, features=Features({"hash": Value("uint64"), "text": Value("string")})
    ).select([1, 0])

    result = dataset.add_item({"hash": 2**64 - 1})

    assert result.to_dict() == {"hash": [2, 1, 2**64 - 1], "text": ["two", "one", None]}
    assert result.features == dataset.features
    assert dataset.to_dict() == {"hash": [2, 1], "text": ["two", "one"]}


@pytest.mark.parametrize("value", [None, 0, 2**63 - 1])
def test_add_item_existing_uint64_values(value):
    dataset = Dataset.from_dict({"hash": [1]}, features=Features({"hash": Value("uint64")}))
    result = dataset.add_item({"hash": value})
    assert result.to_dict() == {"hash": [1, value]}
    assert result.features == dataset.features


@pytest.mark.parametrize("feature,value", [(Value("uint64"), 2**64), (Value("int64"), 2**63)])
def test_add_item_still_rejects_out_of_range_integers(feature, value):
    dataset = Dataset.from_dict({"hash": [1]}, features=Features({"hash": feature}))
    with pytest.raises(OverflowError):
        dataset.add_item({"hash": value})
    assert dataset.to_dict() == {"hash": [1]}


def test_add_item_does_not_infer_uint64_for_a_new_column():
    dataset = Dataset.from_dict({"hash": [1]}, features=Features({"hash": Value("uint64")}))
    with pytest.raises(OverflowError):
        dataset.add_item({"hash": 2**64 - 1, "new": 2**64 - 1})
    assert dataset.to_dict() == {"hash": [1]}


@pytest.mark.parametrize("kind", ["struct", "list"])
@pytest.mark.parametrize("extra", [False, True])
def test_add_item_nested_uint64_overflow_still_requires_inference(kind, extra):
    feature = {"hash": Value("uint64")}
    first = {"hash": 1}
    value = {"hash": 2**64 - 1}
    if extra:
        value["new"] = "must not be discarded"
    if kind == "list":
        feature, first, value = List(feature), [first], [value]
    dataset = Dataset.from_dict({"record": [first]}, features=Features({"record": feature}))
    with pytest.raises(OverflowError):
        dataset.add_item({"record": value})
    assert dataset.to_dict() == {"record": [first]}


def test_add_item_nested_null_promotion_keeps_normal_inference():
    dataset = Dataset.from_dict(
        {"record": [{"hash": 1, "extra": None}]},
        features=Features({"record": {"hash": Value("uint64"), "extra": Value("null")}}),
    )
    result = dataset.add_item({"record": {"hash": 2, "extra": "present"}})
    assert result.to_dict() == {"record": [{"hash": 1, "extra": None}, {"hash": 2, "extra": "present"}]}
    assert result.features == Features({"record": {"hash": Value("uint64"), "extra": Value("string")}})


@pytest.mark.parametrize("keep_in_memory", [False, True])
def test_add_item_uint64_reordered_disk_roundtrip(tmp_path, keep_in_memory):
    features = Features({"hash": Value("uint64"), "text": Value("string")})
    original_rows = {"hash": [1, 2], "text": ["one", "two"]}
    source_path = tmp_path / "source"
    Dataset.from_dict(original_rows, features=features).save_to_disk(source_path)
    dataset = load_from_disk(source_path, keep_in_memory=keep_in_memory).select([1, 0])

    result = dataset.add_item({"hash": 2**63, "text": "high"}).add_item({"hash": 2**64 - 1, "text": "max"})
    output_path = tmp_path / "output"
    result.save_to_disk(output_path)
    restored = load_from_disk(output_path)

    assert restored.to_dict() == {
        "hash": [2, 1, 2**63, 2**64 - 1],
        "text": ["two", "one", "high", "max"],
    }
    assert restored.features == features
    assert Features.from_arrow_schema(restored.data.schema) == features
    assert dataset.to_dict() == {"hash": [2, 1], "text": ["two", "one"]}
    original = load_from_disk(source_path)
    assert original.to_dict() == original_rows
    assert original.features == features
