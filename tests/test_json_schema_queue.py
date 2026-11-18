import copy
import json

import pytest

from datasets import Dataset, Json, List, load_dataset
from datasets.utils.json import find_mixed_struct_types_field_paths


@pytest.mark.parametrize(
    "examples,allow_root,expected",
    [
        ([], False, []),
        ([None, None], False, []),
        ([{"x": 1}, {"x": 2}], False, []),
        ([{"x": 1}, {"y": 2}], False, []),
        ([{"x": 1}, {"y": 2}], True, [[]]),
        ([{"x": {}}], False, [["x"]]),
        ([{"x": {"a": 1}}, {"x": {"b": 2}}], False, [["x"]]),
        ([{"x": [{"a": 1}, {"b": 2}]}], False, [["x", 0]]),
        ([{"x": None}, {"x": []}, {"x": [None]}], False, []),
        ([{"x": {"a": 1}}, {"x": "text"}], False, [["x"]]),
        ([{"[]": [[{"a": 1}], [{"b": 2}]]}], False, [["[]", 0, 0]]),
    ],
)
def test_json_schema_traversal_preserves_paths_and_inputs(examples, allow_root, expected):
    original = copy.deepcopy(examples)
    assert find_mixed_struct_types_field_paths(examples, allow_root=allow_root) == expected
    assert examples == original


def test_wide_schema_finds_each_nested_json_field_once():
    left = {f"field_{index}": {"records": [{"left": index}]} for index in range(128)}
    right = {f"field_{index}": {"records": [{"right": index}]} for index in range(128)}

    actual = find_mixed_struct_types_field_paths([left, right])

    assert len(actual) == 128
    assert {tuple(path) for path in actual} == {(f"field_{index}", "records", 0) for index in range(128)}


@pytest.mark.parametrize("streaming", [False, True])
def test_wide_json_schema_in_native_dataset_loading(tmp_path, streaming):
    rows = [
        {f"field_{index}": [{"left": index}] for index in range(128)},
        {f"field_{index}": [{"right": index + 1}] for index in range(128)},
    ]
    path = tmp_path / "wide.jsonl"
    content = "\n".join(json.dumps(row) for row in rows)
    path.write_text(content, encoding="utf-8")

    if streaming:
        dataset = load_dataset("json", data_files=str(path), split="train", streaming=True)
    else:
        dataset = Dataset.from_json(str(path), cache_dir=str(tmp_path / "cache"))

    assert list(dataset) == rows
    assert all(feature == List(Json()) for feature in dataset.features.values())
    assert path.read_text(encoding="utf-8") == content
