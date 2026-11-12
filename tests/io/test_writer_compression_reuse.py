"""JSON writers retain explicit compression when reused."""

import bz2
import gzip
import json
import lzma

import pytest

from datasets import Dataset
from datasets.io.json import JsonDatasetWriter


@pytest.mark.parametrize(
    "compression,decode",
    [("gzip", gzip.decompress), ("bz2", bz2.decompress), ("xz", lzma.decompress)],
)
def test_repeated_json_export_preserves_explicit_compression(tmp_path, compression, decode):
    path = tmp_path / "export.data"
    dataset = Dataset.from_dict({"id": [1, 2], "label": ["a", "b"]})
    writer = JsonDatasetWriter(dataset, path, compression=compression, batch_size=1)
    for _ in range(2):
        assert writer.write() > 0
        records = [json.loads(line) for line in decode(path.read_bytes()).splitlines()]
        assert records == [{"id": 1, "label": "a"}, {"id": 2, "label": "b"}]
