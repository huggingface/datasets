"""Export writers preserve configuration when write() is called repeatedly."""

import io
import json
import sqlite3

from datasets import Dataset
from datasets.io.csv import CsvDatasetWriter
from datasets.io.json import JsonDatasetWriter
from datasets.io.sql import SqlDatasetWriter


def test_repeated_json_write_keeps_orient_and_lines():
    dataset = Dataset.from_dict({"id": [1, 2], "label": ["a", "b"]})
    with io.BytesIO() as output:
        writer = JsonDatasetWriter(dataset, output, orient="values", lines=False)
        first_count = writer.write()
        first = output.getvalue()
        assert json.loads(first) == [[1, "a"], [2, "b"]]
        assert writer.write() == first_count
        assert output.getvalue() == first + first


def test_repeated_csv_write_keeps_header_and_index():
    dataset = Dataset.from_dict({"value": ["a", "b"]})
    with io.BytesIO() as output:
        writer = CsvDatasetWriter(dataset, output, header=False, index=True)
        first_count = writer.write()
        first = output.getvalue()
        assert first.startswith(b"0,a")
        assert writer.write() == first_count
        assert output.getvalue() == first + first


def test_repeated_sql_write_keeps_index_configuration():
    dataset = Dataset.from_dict({"value": [7, 8]})
    with sqlite3.connect(":memory:") as connection:
        writer = SqlDatasetWriter(dataset, "exported", connection, index=True, if_exists="replace")
        assert writer.write() == 2
        assert writer.write() == 2
        columns = [info[1] for info in connection.execute("PRAGMA table_info(exported)")]
        assert columns == ["index", "value"]
        assert connection.execute("SELECT value FROM exported").fetchall() == [(7,), (8,)]
