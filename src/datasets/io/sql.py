import multiprocessing
import time
from typing import TYPE_CHECKING, Optional, Union

import pyarrow as pa
import pyarrow.compute as pc

from .. import Dataset, Features, config
from ..formatting import query_table
from ..packaged_modules.sql.sql import Sql
from ..utils import tqdm as hf_tqdm
from .abc import AbstractDatasetInputStream


if TYPE_CHECKING:
    import sqlite3

    import sqlalchemy


class SqlDatasetReader(AbstractDatasetInputStream):
    def __init__(
        self,
        sql: Union[str, "sqlalchemy.sql.Selectable"],
        con: Union[str, "sqlalchemy.engine.Connection", "sqlalchemy.engine.Engine", "sqlite3.Connection"],
        features: Optional[Features] = None,
        cache_dir: str = None,
        keep_in_memory: bool = False,
        **kwargs,
    ):
        super().__init__(features=features, cache_dir=cache_dir, keep_in_memory=keep_in_memory, **kwargs)
        self.builder = Sql(
            cache_dir=cache_dir,
            features=features,
            sql=sql,
            con=con,
            **kwargs,
        )

    def read(self):
        download_config = None
        download_mode = None
        verification_mode = None
        base_path = None

        self.builder.download_and_prepare(
            download_config=download_config,
            download_mode=download_mode,
            verification_mode=verification_mode,
            base_path=base_path,
        )

        # Build dataset for splits
        dataset = self.builder.as_dataset(split="train", in_memory=self.keep_in_memory)
        return dataset


# Arrow types whose Python values sqlite3 binds to what pandas + SQLAlchemy bind (it stores NaN as NULL, like None)
_SQLITE_AS_IS = {pa.bool_(), pa.null(), pa.string(), pa.large_string(), pa.binary(), pa.large_binary()}
_SQLITE_AS_IS |= {pa.int8(), pa.int16(), pa.int32(), pa.int64(), pa.uint8(), pa.uint16(), pa.uint32()}
_SQLITE_AS_IS |= {pa.float16(), pa.float32(), pa.float64()}
# dates and naive datetimes, bound as SQLAlchemy's text if in Python's years 1-9999 (pandas raises for others)
_SQLITE_AS_TEXT = {pa.date32(), pa.timestamp("s"), pa.timestamp("ms"), pa.timestamp("us")}
# batches are converted for this long (no transaction open), then written in one transaction: a group of at most
# this many rows (or one batch) and bytes of Arrow data (a larger batch is written by pandas, as today)
_GROUP_SECONDS, _GROUP_ROWS, _GROUP_BYTES = 0.005, 100_000, 16 * 2**20
# then other writers can take the lock for as long as the group held it, but at most for what pandas spends per row
# without it (~1 us), so that writing large rows (that hold the lock longer) isn't slower than with pandas
_GROUP_PAUSE_PER_ROW = 1e-6


def _sqlite_rows(table: pa.Table) -> Optional[list[tuple]]:
    """The rows of `table` as pandas + SQLAlchemy bind them to SQLite, or None if some dates are out of range."""
    columns = []
    for column in table.columns:
        if column.type in _SQLITE_AS_TEXT:
            years = pc.min_max(pc.year(column))
            if years["min"].is_valid and not 1 <= years["min"].as_py() <= years["max"].as_py() <= 9999:
                return None
            column = column.cast(pa.timestamp("us")) if pa.types.is_timestamp(column.type) else column
            column = column.cast(pa.string())  # SQLAlchemy's formats: "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS.ffffff"
        columns.append(column.to_pylist())
    return list(zip(*columns))


class SqlDatasetWriter:
    def __init__(
        self,
        dataset: Dataset,
        name: str,
        con: Union[str, "sqlalchemy.engine.Connection", "sqlalchemy.engine.Engine", "sqlite3.Connection"],
        batch_size: Optional[int] = None,
        num_proc: Optional[int] = None,
        **to_sql_kwargs,
    ):
        if num_proc is not None and num_proc <= 0:
            raise ValueError(f"num_proc {num_proc} must be an integer > 0.")

        self.dataset = dataset
        self.name = name
        self.con = con
        self.batch_size = batch_size if batch_size else config.DEFAULT_MAX_BATCH_SIZE
        self.num_proc = num_proc
        self.to_sql_kwargs = to_sql_kwargs

    def write(self) -> int:
        _ = self.to_sql_kwargs.pop("sql", None)
        _ = self.to_sql_kwargs.pop("con", None)
        index = self.to_sql_kwargs.pop("index", False)

        if self._sqlite_groups(index):
            return self._write_sqlite(index, **self.to_sql_kwargs)
        written = self._write(index=index, **self.to_sql_kwargs)
        return written

    def _sqlite_groups(self, index) -> bool:
        """Whether `_write_sqlite` writes this export: one process, a SQLite file URI, `to_sql`'s defaults but
        `if_exists`, supported column types, and pandas 2 or later (pandas 1 binds datetimes in nanoseconds)."""
        if (self.num_proc or 1) > 1 or index is not False or self.to_sql_kwargs.keys() - {"if_exists"}:
            return False
        try:
            import sqlalchemy

            url = sqlalchemy.engine.make_url(self.con) if isinstance(self.con, str) else None
            # other drivers (e.g. aiosqlite) keep pandas' path, and so does a database in memory (one per connection)
            if url is None or (url.get_backend_name(), url.get_driver_name()) != ("sqlite", "pysqlite"):
                return False
            if url.database in (None, "", ":memory:") or config.PANDAS_VERSION.major < 2:
                return False
        except Exception:  # e.g. no SQLAlchemy, not a URL: pandas raises
            return False
        return all(t in _SQLITE_AS_IS | _SQLITE_AS_TEXT for t in self.dataset.data.schema.types)

    def _write_sqlite(self, index, **to_sql_kwargs) -> int:
        """`_write`, but after the first batch (pandas creates the table) batches are converted with no transaction
        open, then written in groups, one transaction each, with pandas' INSERT and values. A failed group is rolled
        back and pandas writes its batches, as `_write`; if the export is cut short, a group's rows can be missing."""
        import sqlalchemy

        written, group, start, data, indices = 0, [], 0.0, self.dataset.data, self.dataset._indices

        def write_group(pause=True) -> int:
            batches, group[:] = group[:], []
            try:  # built after the first batch: pandas raises its own errors first (e.g. for an empty table name)
                # a NullPool closes its connection; if the database is locked for 0.1 s, pandas writes the group
                kwargs = {"poolclass": sqlalchemy.pool.NullPool, "connect_args": {"timeout": 0.1}}
                engine = sqlalchemy.create_engine(self.con, **kwargs)
                table = sqlalchemy.table(self.name, *map(sqlalchemy.column, self.dataset.column_names))
                insert = str(table.insert().compile(dialect=engine.dialect))
                with engine.begin() as connection:
                    dbapi_connection = connection.connection.dbapi_connection
                    if dbapi_connection.isolation_level is None or getattr(dbapi_connection, "autocommit", 0) is True:
                        raise RuntimeError("autocommit (a connect listener): a replay would write some rows twice")
                    if dbapi_connection.execute("PRAGMA journal_mode").fetchone()[0] == "off":
                        raise RuntimeError("journal_mode=OFF (a connect listener): a rollback would be undefined")
                    locked = time.perf_counter()
                    num_rows = sum(connection.exec_driver_sql(insert, r).rowcount or len(r) for _, r, _ in batches)
            except Exception:  # e.g. a constraint failed in one of the batches: rolled back
                num_rows = None
            if num_rows is None:  # pandas writes the batches, out of the `except` (its error isn't chained to ours)
                return sum(self._batch_sql((offset, index, to_sql_kwargs)) for offset, *_ in batches)
            if pause:  # committed: the lock is free for as long as the group held it (see _GROUP_PAUSE_PER_ROW)
                time.sleep(min(time.perf_counter() - locked, _GROUP_PAUSE_PER_ROW * num_rows))
            return num_rows

        for offset in hf_tqdm(
            range(0, len(self.dataset), self.batch_size), unit="ba", desc="Creating SQL from Arrow format"
        ):
            if not offset:  # pandas writes the first batch: it creates the table
                written += self._batch_sql((offset, index, to_sql_kwargs))
                continue
            batch = query_table(data, slice(offset, offset + self.batch_size), indices=indices)
            # one chunk per column is faster to measure and convert than one per row (an indices mapping); a batch
            # estimated (from its first row) as larger than a group is neither copied nor measured: pandas writes it
            if (size := batch.slice(0, 1).nbytes * batch.num_rows) <= _GROUP_BYTES:
                batch = batch.combine_chunks()
                size = batch.nbytes
            before = group[-1][2] if group else 0  # Arrow bytes of the group, written before converting if it's full
            full = len(group) * self.batch_size + batch.num_rows > _GROUP_ROWS or before + size > _GROUP_BYTES
            if group and (full or time.perf_counter() - start >= _GROUP_SECONDS):
                written += write_group()
            try:
                rows = _sqlite_rows(batch) if size <= _GROUP_BYTES else None
            except Exception:  # e.g. invalid UTF-8: the batch goes through pandas (after the group), which raises
                rows = None
            if rows is None:  # e.g. dates out of range, or a large batch: pandas writes it after the group
                written += (write_group() if group else 0) + self._pandas_sql(batch, offset, index, to_sql_kwargs)
                continue
            start = start if group else time.perf_counter()  # from the end of the first conversion
            group.append((offset, rows, (group[-1][2] if group else 0) + size))
            del rows  # only the group holds the rows
        return written + (write_group(pause=False) if group else 0)

    def _batch_sql(self, args):
        offset, index, to_sql_kwargs = args
        batch = query_table(
            table=self.dataset.data,
            key=slice(offset, offset + self.batch_size),
            indices=self.dataset._indices,
        )
        return self._pandas_sql(batch, offset, index, to_sql_kwargs)

    def _pandas_sql(self, batch, offset, index, to_sql_kwargs):
        to_sql_kwargs = {**to_sql_kwargs, "if_exists": "append"} if offset > 0 else to_sql_kwargs
        df = batch.to_pandas(integer_object_nulls=True)
        num_rows = df.to_sql(self.name, self.con, index=index, **to_sql_kwargs)
        return num_rows or len(df)

    def _write(self, index, **to_sql_kwargs) -> int:
        """Writes the pyarrow table as SQL to a database.

        Caller is responsible for opening and closing the SQL connection.
        """
        written = 0

        if self.num_proc is None or self.num_proc == 1:
            for offset in hf_tqdm(
                range(0, len(self.dataset), self.batch_size),
                unit="ba",
                desc="Creating SQL from Arrow format",
            ):
                written += self._batch_sql((offset, index, to_sql_kwargs))
        else:
            num_rows, batch_size = len(self.dataset), self.batch_size
            with multiprocessing.Pool(self.num_proc) as pool:
                for num_rows in hf_tqdm(
                    pool.imap(
                        self._batch_sql,
                        [(offset, index, to_sql_kwargs) for offset in range(0, num_rows, batch_size)],
                    ),
                    total=(num_rows // batch_size) + 1 if num_rows % batch_size else num_rows // batch_size,
                    unit="ba",
                    desc="Creating SQL from Arrow format",
                ):
                    written += num_rows

        return written
