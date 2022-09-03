from sqlite3 import connect

import pandas as pd
import pyarrow as pa
import pytest

from datasets import ClassLabel, Features, Value
from datasets.packaged_modules.sql.sql import Sql


@pytest.fixture
def sqlite_file(tmp_path):
    filename = str(tmp_path / "malformed_file.sqlite")
    with connect(filename) as conn:
        pd.DataFrame.from_dict({"header1": [1, 10], "header2": [2, 20], "label": ["good", "bad"]}).to_sql(
            "TABLE_NAME", con=conn
        )
    return filename


def test_csv_cast_label(sqlite_file):
    table_name = "TABLE_NAME"
    with connect(sqlite_file) as conn:
        labels = pd.read_sql(f"SELECT * FROM {table_name}", conn)["label"].tolist()
    sql = Sql(
        features=Features(
            {"header1": Value("int32"), "header2": Value("int32"), "label": ClassLabel(names=["good", "bad"])}
        ),
        table_name=table_name,
    )
    generator = sql._generate_tables([[sqlite_file]])
    pa_table = pa.concat_tables([table for _, table in generator])
    assert pa_table.schema.field("label").type == ClassLabel(names=["good", "bad"])()
    generated_content = pa_table.to_pydict()["label"]
    assert generated_content == [ClassLabel(names=["good", "bad"]).str2int(label) for label in labels]
