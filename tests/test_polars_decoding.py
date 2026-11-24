"""Polars formatting must decode features like the default and pandas formats."""

from dataclasses import dataclass

import pyarrow as pa
import pytest

from datasets import Dataset, Features, IterableDataset


@dataclass
class UpperFeature:
    """Minimal decodable feature that uppercases its stored string."""

    decode: bool = True

    def __call__(self):
        return pa.string()

    def decode_example(self, value, token_per_repo_id=None):
        return value.upper() if value is not None else None


@pytest.mark.parametrize("dataset_cls", [Dataset, IterableDataset])
def test_with_format_polars__decodable_feature__decodes(dataset_cls):
    ds = dataset_cls.from_dict({"text": ["alpha", "beta"]}, features=Features({"text": UpperFeature()}))

    rows = list(ds.with_format("polars"))

    assert [row["text"][0] for row in rows] == ["ALPHA", "BETA"]
