import csv
import io
import json
import sqlite3
from collections.abc import Iterator

import pytest

from datasets import Dataset
from datasets.io.csv import CsvDatasetWriter
from datasets.io.json import JsonDatasetWriter
from datasets.io.sql import SqlDatasetWriter


class _InspectingPool:
    """Exercise Pool.imap synchronously while checking that jobs stay lazy."""

    def __init__(self, processes):
        assert processes == 2

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def imap(self, func, jobs):
        # A list here scales linearly with the number of export batches.
        assert isinstance(jobs, Iterator)
        return map(func, jobs)


@pytest.mark.parametrize("file_format", ["csv", "json", "sql"])
def test_multiprocess_export_generates_batch_jobs_lazily(monkeypatch, file_format):
    dataset = Dataset.from_dict({"value": list(range(7))})
    monkeypatch.setattr(f"datasets.io.{file_format}.multiprocessing.Pool", _InspectingPool)

    if file_format == "sql":
        with sqlite3.connect(":memory:") as connection:
            written = SqlDatasetWriter(dataset, "exported", connection, batch_size=2, num_proc=2).write()
            values = connection.execute("SELECT value FROM exported").fetchall()
        assert written == len(dataset)
        assert values == [(i,) for i in range(7)]
    else:
        buffer = io.BytesIO()
        if file_format == "csv":
            written = CsvDatasetWriter(dataset, buffer, batch_size=2, num_proc=2).write()
            values = [int(row["value"]) for row in csv.DictReader(io.StringIO(buffer.getvalue().decode()))]
        else:
            written = JsonDatasetWriter(dataset, buffer, batch_size=2, num_proc=2).write()
            values = [json.loads(line)["value"] for line in buffer.getvalue().splitlines()]
        assert written == len(buffer.getvalue())
        assert values == list(range(7))
