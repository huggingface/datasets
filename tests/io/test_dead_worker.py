import contextlib
import os
import sqlite3

import pytest

from datasets import Dataset
from datasets.io.csv import CsvDatasetWriter
from datasets.io.json import JsonDatasetWriter
from datasets.io.sql import SqlDatasetWriter

from ..utils import fail_after, require_not_windows, require_sqlalchemy


# The batch functions run in the pool workers: one of them dies abruptly, as on an OOM kill


class DyingWorkerCsvDatasetWriter(CsvDatasetWriter):
    def _batch_csv(self, args):
        if args[0] == 20 and os.getpid() != self.parent_pid:
            os._exit(1)
        return super()._batch_csv(args)


class DyingWorkerJsonDatasetWriter(JsonDatasetWriter):
    def _batch_json(self, args):
        if args[0] == 20 and os.getpid() != self.parent_pid:
            os._exit(1)
        return super()._batch_json(args)


class DyingWorkerSqlDatasetWriter(SqlDatasetWriter):
    def _batch_sql(self, args):
        if args[0] == 20 and os.getpid() != self.parent_pid:
            os._exit(1)
        return super()._batch_sql(args)


@require_not_windows
@pytest.mark.parametrize("writer_cls", [DyingWorkerCsvDatasetWriter, DyingWorkerJsonDatasetWriter])
def test_dataset_to_file_num_proc_raises_if_a_worker_dies(writer_cls, tmp_path):
    dataset = Dataset.from_dict({"a": list(range(100))})
    writer = writer_cls(dataset, str(tmp_path / "out"), batch_size=10, num_proc=2)
    writer.parent_pid = os.getpid()
    with fail_after(10), pytest.raises(RuntimeError, match="One of the subprocesses has abruptly died"):
        writer.write()


@require_not_windows
@require_sqlalchemy
def test_dataset_to_sql_num_proc_raises_if_a_worker_dies(tmp_path):
    db_path = str(tmp_path / "out.db")
    with contextlib.closing(sqlite3.connect(db_path)) as con, con:
        con.execute("CREATE TABLE dataset (a BIGINT)")  # the workers then only append
    dataset = Dataset.from_dict({"a": list(range(100))})
    writer = DyingWorkerSqlDatasetWriter(
        dataset, "dataset", "sqlite:///" + db_path, batch_size=10, num_proc=2, if_exists="append"
    )
    writer.parent_pid = os.getpid()
    with fail_after(10), pytest.raises(RuntimeError, match="One of the subprocesses has abruptly died"):
        writer.write()
