from datasets import Dataset, Features, Value


def test_flatten_rejects_name_collision_between_struct_field_and_column():
    dataset = Dataset.from_dict({"a": [{"b": 1}], "a.b": [2]})

    try:
        dataset.flatten()
    except ValueError as error:
        assert "a.b" in str(error)
    else:
        raise AssertionError("flatten silently dropped the flattened values")


def test_flatten_still_flattens_without_collision():
    dataset = Dataset.from_dict({"a": [{"b": 1, "c": 2}]})

    flattened = dataset.flatten()

    assert flattened.column_names == ["a.b", "a.c"]
    assert flattened.to_dict() == {"a.b": [1], "a.c": [2]}


def test_flatten_keeps_plain_columns():
    dataset = Dataset.from_dict({"x": [1], "a": [{"b": 2}]})

    flattened = dataset.flatten()

    assert flattened.column_names == ["x", "a.b"]
