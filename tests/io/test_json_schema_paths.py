"""Regression tests for memoizing JSON feature-path extraction during export."""

import io
import json

import pytest

from datasets import Dataset, Features, Json, Value
from datasets.io import json as json_io


@pytest.mark.parametrize("num_proc", [None, 2])
def test_json_writer_traverses_nested_features_only_once(monkeypatch, num_proc):
    records = [
        {"id": i, "payload": {"items": [i, None], "label": "中文"}}
        for i in range(9)
    ]
    dataset = Dataset.from_list(
        records,
        features=Features({"id": Value("int64"), "payload": Json()}),
    )
    original = json_io.get_json_field_paths_from_feature
    calls = []

    def track_features(features):
        calls.append(features)
        return original(features)

    monkeypatch.setattr(json_io, "get_json_field_paths_from_feature", track_features)
    with io.BytesIO() as output:
        writer = json_io.JsonDatasetWriter(dataset, output, batch_size=2, num_proc=num_proc)
        assert writer.write() > 0
        decoded = [json.loads(line) for line in output.getvalue().splitlines()]

    assert decoded == records
    assert len(calls) == 1
