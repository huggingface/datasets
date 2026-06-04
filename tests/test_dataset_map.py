from datasets import Dataset

def test_map_does_not_drop_columns():
    ds = Dataset.from_dict({
        "a": [1, 2, 3],
        "b": [10, 20, 30]
    })

    ds2 = ds.map(lambda x: {"a": x["a"] * 2})

    assert "a" in ds2.column_names
    assert "b" in ds2.column_names
    assert ds2["b"] == [10, 20, 30]
