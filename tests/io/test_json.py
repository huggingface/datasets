import json

import pytest

from datasets import NamedSplit
from datasets.io.json import JsonlDatasetReader


DATA = [
    {"col_1": "a", "col_2": 0, "col_3": 0.0},
    {"col_1": "b", "col_2": 1, "col_3": 1.0},
    {"col_1": "c", "col_2": 2, "col_3": 2.0},
    {"col_1": "d", "col_2": 3, "col_3": 3.0},
]


@pytest.fixture(scope="session")
def jsonl_path(tmp_path_factory):
    path = str(tmp_path_factory.mktemp("data") / "dataset.jsonl")
    with open(path, "w") as f:
        for item in DATA:
            f.write(json.dumps(item))
    return path


@pytest.mark.parametrize("split, expected_split", [(None, None), (NamedSplit("train"), "train")])
def test_dataset_jsonl_reader(split, expected_split, jsonl_path):
    path = jsonl_path
    ds = JsonlDatasetReader(path, split=split).read()
    assert ds.num_rows == 4
    assert ds.num_columns == 3
    assert ds.column_names == ["col_1", "col_2", "col_3"]
    assert ds.features["col_1"].dtype == "string"
    assert ds.features["col_2"].dtype == "int64"
    assert ds.features["col_3"].dtype == "float64"
    assert ds.split == expected_split
