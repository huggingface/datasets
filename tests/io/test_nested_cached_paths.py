"""Nested JSON features retain decoded values when export paths are cached."""

import io
import json

import pytest

from datasets import Dataset, Features, Json, List
from datasets.io.json import JsonDatasetWriter


@pytest.mark.parametrize("num_proc", [None, 2])
def test_cached_paths_decode_nested_lists_across_batches(num_proc):
    records = [
        {"payload": {"items": [{"value": 1}, None]}},
        {"payload": {"items": []}},
        {"payload": None},
        {"payload": {"items": [{"value": [2, 3]}]}},
        {"payload": {"items": [None, {"text": "中文"}]}},
    ]
    dataset = Dataset.from_list(records, features=Features({"payload": {"items": List(Json())}}))
    with io.BytesIO() as output:
        assert JsonDatasetWriter(dataset, output, batch_size=1, num_proc=num_proc).write() > 0
        assert [json.loads(line) for line in output.getvalue().splitlines()] == records
