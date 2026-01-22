def test_interleave_all_exhausted_without_replacement_keeps_last_elements():
    from datasets import Dataset, interleave_datasets

    d1 = Dataset.from_dict({"a": [0, 1, 2]})
    d2 = Dataset.from_dict({"a": [10, 11, 12, 13]})
    d3 = Dataset.from_dict({"a": [20, 21, 22]})

    dataset = interleave_datasets(
        [d1, d2, d3],
        stopping_strategy="all_exhausted_without_replacement",
    )

    assert dataset["a"] == [0, 10, 20, 1, 11, 21, 2, 12, 22, 13]
