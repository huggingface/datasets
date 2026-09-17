"""TsFile (table model) packaged builder — per-device wide format.

Each output row corresponds to a single device (identified by its TAG values).
The ``time`` column and every FIELD column are Arrow ``list<...>`` columns
holding the entire time series for that device. When the same device is
present in multiple TsFiles within a split, its data is merged across files
and the resulting lists are sorted in ascending time order.

Output schema layout::

    <tag1>:    string
    <tag2>:    string                   (one column per TAG)
    ...
    time:      list<timestamp[unit, tz]>
    <field1>:  list<original_type>      (one column per FIELD)
    <field2>:  list<original_type>
    ...

Reading model
-------------
Data is fetched **per device** via ``TsFileReader.query_table`` with a
push-down ``tag_filter``. For each split the builder:

1. Opens every input file once, calls ``get_all_devices`` to enumerate the
   ``(tag-tuple) → [files]`` index across all shards.
2. Iterates the index in stable order. For each device, streams Arrow
   batches from every contributing file, concatenates and sorts by time,
   and emits one wide row.

Peak memory is bounded by **one device's** total payload across the split,
not by the split's total size.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Literal, Optional

import numpy as np
import pyarrow as pa

import datasets
from datasets.builder import Key
from datasets.table import table_cast
from datasets.utils.tqdm import tqdm


logger = datasets.utils.logging.get_logger(__name__)


# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------


def _arrow_type(ts_dtype, *, unit: str, tz: Optional[str]) -> pa.DataType:
    """Map a tsfile ``TSDataType`` to its Arrow representation."""
    from tsfile.constants import TSDataType

    return {
        TSDataType.BOOLEAN: pa.bool_(),
        TSDataType.INT32: pa.int32(),
        TSDataType.INT64: pa.int64(),
        TSDataType.FLOAT: pa.float32(),
        TSDataType.DOUBLE: pa.float64(),
        TSDataType.TEXT: pa.string(),
        TSDataType.STRING: pa.string(),
        TSDataType.TIMESTAMP: pa.timestamp(unit, tz=tz),
        TSDataType.DATE: pa.date32(),
        TSDataType.BLOB: pa.binary(),
    }.get(ts_dtype, pa.string())


def _promote_tsdatatype(a, b):
    """Return the widest of two ``TSDataType`` values.

    Mirrors IoTDB's ``ALTER COLUMN ... SET DATA TYPE`` rules:

    - ``INT32 → INT64 → DOUBLE``
    - ``INT32 → FLOAT → DOUBLE``

    ``INT64`` and ``FLOAT`` cannot widen losslessly into either, so their
    join is ``DOUBLE``. Non-numeric or otherwise unrelated pairs raise.
    """
    if a == b:
        return a

    from tsfile.constants import TSDataType

    table = {
        (TSDataType.INT32, TSDataType.INT64): TSDataType.INT64,
        (TSDataType.INT32, TSDataType.FLOAT): TSDataType.FLOAT,
        (TSDataType.INT32, TSDataType.DOUBLE): TSDataType.DOUBLE,
        (TSDataType.INT64, TSDataType.FLOAT): TSDataType.DOUBLE,
        (TSDataType.INT64, TSDataType.DOUBLE): TSDataType.DOUBLE,
        (TSDataType.FLOAT, TSDataType.DOUBLE): TSDataType.DOUBLE,
    }
    if (a, b) in table:
        return table[(a, b)]
    if (b, a) in table:
        return table[(b, a)]
    raise ValueError(
        f"Incompatible column types across files: {a.name} vs {b.name}. "
        "Only numeric widening (INT32→INT64→DOUBLE, INT32→FLOAT→DOUBLE) is supported."
    )


def _to_epoch(value: Any, unit: str) -> int:
    """Coerce a timestamp boundary to an integer epoch in ``unit``.

    Accepts ``int`` (raw epoch in ``unit``), ``datetime``/``date``,
    ISO-8601 ``str``, or any ``pa.Scalar`` of timestamp type.
    """
    if isinstance(value, bool):  # bool is a subclass of int; reject explicitly
        raise TypeError(f"start_time/end_time must be a timestamp, got bool: {value!r}")
    if isinstance(value, int):
        return value
    try:
        # Normalize the various input shapes into something pa.scalar() can absorb
        # under a `timestamp[unit]` target type.
        if isinstance(value, _dt.datetime):
            if value.tzinfo is not None:
                value = value.astimezone(_dt.timezone.utc).replace(tzinfo=None)
        elif isinstance(value, _dt.date):
            value = _dt.datetime(value.year, value.month, value.day)
        elif isinstance(value, str):
            value = _dt.datetime.fromisoformat(value)
        return pa.scalar(value, type=pa.timestamp(unit)).value
    except (pa.ArrowInvalid, pa.ArrowTypeError, TypeError, ValueError) as e:
        raise TypeError(
            f"start_time/end_time must be a datetime, date, pa.TimestampScalar, "
            f"ISO-8601 str, or int epoch; got {type(value).__name__}: {value!r}"
        ) from e


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------


@dataclass
class TsFileConfig(datasets.BuilderConfig):
    """BuilderConfig for TsFile (table model) — per-device wide format.

    Args:
        table_name (`str`, *optional*):
            Name of the table to read. When unset, the first table found in
            the first valid file is used. Lookups are case-insensitive.
        columns (`list[str]`, *optional*):
            Subset of FIELD columns to keep. TAG columns and the TIME column
            are *always* returned (they identify the device / its timeline
            and cannot be excluded). Names that refer to TAG or TIME columns,
            or to fields absent from every file, resolve quietly: TAGs/TIME
            are emitted as usual, and never-seen fields become all-null list
            columns. When unset, all FIELDs are returned.
        start_time, end_time (`datetime`, `date`, `pa.TimestampScalar`, ISO-8601 `str`, or `int`, *optional*):
            Inclusive timestamp range. Either bound may be omitted.
            ``datetime`` values are taken in their own tz (UTC if naive);
            ``int`` is interpreted as a raw epoch in ``timestamp_unit``.
        input_batch_size (`int`, *optional*, defaults to 65_536):
            Maximum number of rows fetched per Arrow batch from
            ``TsFileReader.query_table``. Controls peak memory while
            streaming a single device.
        output_batch_size (`int`, *optional*, defaults to 32):
            Number of devices (output dataset rows) packed into each Arrow
            record batch yielded to the writer. Also the granularity at
            which the dataset progress bar advances; smaller values give
            more responsive feedback on slow per-device reads, larger ones
            reduce per-batch overhead.
        features (`Features`, *optional*):
            Final Features schema. When provided, the metadata scan over
            input files is skipped.
        on_bad_files (`Literal["error", "warn", "skip"]`, *optional*, defaults to "error"):
            What to do if a file cannot be opened or lacks the requested table.
        timestamp_unit (`Literal["s", "ms", "us", "ns"]`, *optional*, defaults to "ms"):
            Time unit for the timestamp column. IoTDB defaults to milliseconds.
        timestamp_tz (`str`, *optional*):
            Time zone for the timestamp column. ``None`` means timezone-naive.
    """

    table_name: Optional[str] = None
    columns: Optional[list[str]] = None
    start_time: Optional[Any] = None
    end_time: Optional[Any] = None
    input_batch_size: int = 65_536
    output_batch_size: int = 32
    features: Optional[datasets.Features] = None
    on_bad_files: Literal["error", "warn", "skip"] = "error"
    timestamp_unit: Literal["s", "ms", "us", "ns"] = "ms"
    timestamp_tz: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.input_batch_size is None or self.input_batch_size <= 0:
            raise ValueError(f"`input_batch_size` must be a positive integer, got {self.input_batch_size}")
        if self.output_batch_size is None or self.output_batch_size <= 0:
            raise ValueError(f"`output_batch_size` must be a positive integer, got {self.output_batch_size}")
        if self.columns is not None and len(self.columns) == 0:
            raise ValueError("`columns` must be a non-empty list when provided.")
        if self.timestamp_unit not in ("s", "ms", "us", "ns"):
            raise ValueError(f"`timestamp_unit` must be one of 's', 'ms', 'us', 'ns', got {self.timestamp_unit!r}")
        if self.on_bad_files not in ("error", "warn", "skip"):
            raise ValueError(f"`on_bad_files` must be one of 'error', 'warn', 'skip', got {self.on_bad_files!r}")
        if self.start_time is not None:
            self.start_time = _to_epoch(self.start_time, self.timestamp_unit)
        if self.end_time is not None:
            self.end_time = _to_epoch(self.end_time, self.timestamp_unit)


# ---------------------------------------------------------------------------
# Internal sentinels
# ---------------------------------------------------------------------------


class _SkipSplit(Exception):
    """Raised internally to abort emitting a split entirely."""


class _MissingTableError(ValueError):
    def __init__(self, table: Optional[str], available):
        super().__init__(f"Table {table!r} not found in file. Available tables: {available}")


_TSFILE_MAGIC = b"TsFile"


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


class TsFile(datasets.ArrowBasedBuilder):
    """Per-device wide-format builder for TsFile (table model)."""

    BUILDER_CONFIG_CLASS = TsFileConfig

    # ----- builder hooks ------------------------------------------------

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._table: Optional[str] = None
        self._time_col: str = "time"
        self._tag_cols: list[str] = []
        self._field_inner: dict[str, pa.DataType] = {}
        self._requested_fields: Optional[list[str]] = None  # lowercased

    def _info(self):
        if (
            self.config.columns is not None
            and self.config.features is not None
            and not set(self.config.columns).issubset(set(self.config.features))
        ):
            raise ValueError(
                "Every entry in `columns` must also appear in `features`, but got "
                f"columns={self.config.columns} and features={list(self.config.features)}"
            )
        return datasets.DatasetInfo(features=self.config.features)

    def _split_generators(self, dl_manager):
        if not self.config.data_files:
            raise ValueError(f"At least one data file must be specified, but got data_files={self.config.data_files}")
        dl_manager.download_config.extract_on_the_fly = True
        data_files = dl_manager.download(self.config.data_files)

        # Lowercase user-facing names to match tsfile's case-insensitive convention.
        self._table = self.config.table_name.lower() if self.config.table_name else None
        self._requested_fields = [c.lower() for c in self.config.columns] if self.config.columns else None

        all_files = [f for files in data_files.values() for f in files]
        scan = self._scan_metadata(all_files)
        if scan is None:
            raise ValueError(
                "Could not infer schema from any of the provided files. "
                "Set `features` explicitly or check the input files."
            )
        self._table = scan["table"]
        self._time_col = scan["time_col"]
        self._tag_cols = scan["tag_cols"]
        self._field_inner = scan["field_inner"]

        if self.info.features is None:
            self.info.features = self._build_features()

        return [
            datasets.SplitGenerator(name=split, gen_kwargs={"files": list(files)})
            for split, files in data_files.items()
        ]

    def _generate_shards(self, files):
        yield from files

    def _generate_tables(self, files):
        target_schema = self.info.features.arrow_schema
        try:
            yield from self._fold_split(files, target_schema)
        except _SkipSplit:
            return

    # ----- metadata scan ------------------------------------------------

    def _scan_metadata(self, files) -> Optional[dict]:
        """Walk every file and unify table name, TAG columns, FIELD types."""
        from tsfile.constants import TIME_COLUMN, ColumnCategory

        wanted_table = self._table
        wanted_fields = set(self._requested_fields) if self._requested_fields is not None else None

        table: Optional[str] = wanted_table
        time_col: Optional[str] = None
        tag_cols: list[str] = []
        tag_seen: set[str] = set()
        # Per-field widest TSDataType seen so far (we map to Arrow at the end).
        field_widest: dict = {}

        for file in files:
            try:
                with self._open_reader(file) as reader:
                    schemas = self._schemas_by_lc(reader)
                    self._require_table_model(file, schemas)
                    if table is None:
                        table = next(iter(schemas))
                    if table not in schemas:
                        raise _MissingTableError(table, list(schemas))
                    for col in schemas[table].get_columns():
                        name = col.get_column_name()
                        cat = col.get_category()
                        ts_dtype = col.get_data_type()
                        if cat == ColumnCategory.TIME:
                            time_col = name
                        elif cat == ColumnCategory.TAG:
                            if name not in tag_seen:
                                tag_seen.add(name)
                                tag_cols.append(name)
                        else:  # FIELD
                            if wanted_fields is not None and name not in wanted_fields:
                                continue
                            prev = field_widest.get(name)
                            field_widest[name] = ts_dtype if prev is None else _promote_tsdatatype(prev, ts_dtype)
            except Exception as e:
                if self._should_reraise(file, e):
                    raise
                continue

        if table is None:
            return None

        unit = self.config.timestamp_unit
        tz = self.config.timestamp_tz

        if self._requested_fields is not None:
            # Honor user order; silently drop names that turned out to be TAGs
            # or the TIME column (TAGs are emitted as their own scalar columns
            # and TIME is always emitted as a list column — neither may also
            # appear as a list-typed field, which would collide on schema name).
            reserved = tag_seen | {time_col} if time_col is not None else tag_seen
            field_inner: dict[str, pa.DataType] = {}
            for name in self._requested_fields:
                if name in reserved:
                    continue
                ts_dtype = field_widest.get(name)
                if ts_dtype is not None:
                    field_inner[name] = _arrow_type(ts_dtype, unit=unit, tz=tz)
                else:
                    # Field never appeared in any file — keep as a nullable
                    # float64 list, fully filled with nulls at read time.
                    field_inner[name] = pa.float64()
        else:
            field_inner = {n: _arrow_type(d, unit=unit, tz=tz) for n, d in field_widest.items()}

        return {
            "table": table,
            "time_col": time_col or TIME_COLUMN,
            "tag_cols": tag_cols,
            "field_inner": field_inner,
        }

    def _build_features(self) -> datasets.Features:
        unit = self.config.timestamp_unit
        tz = self.config.timestamp_tz
        fields: list[pa.Field] = [pa.field(t, pa.string()) for t in self._tag_cols]
        fields.append(pa.field(self._time_col, pa.list_(pa.timestamp(unit, tz=tz))))
        for name, inner in self._field_inner.items():
            fields.append(pa.field(name, pa.list_(inner)))
        return datasets.Features.from_arrow_schema(pa.schema(fields))

    # ----- per-split folding -------------------------------------------

    def _fold_split(self, files, target_schema: pa.Schema):
        """Stream every device in this split via per-device tag-filter pushdown.

        Open one ``TsFileReader`` per file, build a cross-file device index
        keyed by ``(tag-tuple)``, then iterate devices in stable order. For
        each device, ``query_table(tag_filter=...)`` reads only that device's
        rows from each contributing file, so peak memory is bounded by one
        device's payload across the split — never the split's total size.
        """
        if self._table is None:
            raise _SkipSplit

        readers: dict[str, Any] = {}
        try:
            for file in files:
                try:
                    readers[file] = self._open_reader(file)
                except Exception as e:
                    if self._should_reraise(file, e):
                        raise
                    continue

            device_index, file_meta = self._build_device_index(readers)
            if not device_index:
                return

            yield from self._iter_device_batches(device_index, file_meta, readers, target_schema)
        finally:
            for reader in readers.values():
                try:
                    reader.close()
                except Exception:
                    pass

    def _build_device_index(self, readers: dict):
        """Walk every open reader and build the cross-file device index.

        Returns ``(device_index, file_meta)``:

        - ``device_index``: list of ``(device_key, [file_path, ...])`` pairs
          in stable first-seen order. ``device_key`` is a tuple aligned to
          ``self._tag_cols`` (the unified tag-column order).
        - ``file_meta``: maps each readable file to its per-file context
          (``tag_cols``, ``field_cols``, ``time_col``).
        """
        from tsfile.constants import ColumnCategory

        device_to_files: dict[tuple, list[str]] = {}
        device_order: list[tuple] = []
        file_meta: dict[str, dict] = {}
        # ``self._table`` was lowercased either by user-input normalization in
        # ``_split_generators`` or by ``_schemas_by_lc`` during auto-detect.
        table_lc = self._table

        files_iter = tqdm(
            readers.items(),
            total=len(readers),
            desc="Indexing TsFile devices",
            unit="file",
        )

        for file, reader in files_iter:
            try:
                schemas = self._schemas_by_lc(reader)
                self._require_table_model(file, schemas)
                if table_lc not in schemas:
                    raise _MissingTableError(table_lc, list(schemas))
                schema = schemas[table_lc]

                file_tag_cols: list[str] = []
                file_field_cols: set[str] = set()
                time_col = self._time_col
                for col in schema.get_columns():
                    name = col.get_column_name()
                    cat = col.get_category()
                    if cat == ColumnCategory.TIME:
                        time_col = name
                    elif cat == ColumnCategory.TAG:
                        file_tag_cols.append(name)
                    elif cat == ColumnCategory.FIELD:
                        file_field_cols.add(name)

                file_meta[file] = {
                    "tag_cols": file_tag_cols,
                    "field_cols": file_field_cols,
                    "time_col": time_col,
                }

                for device in reader.get_all_devices():
                    if device.table_name is None or device.table_name.lower() != table_lc:
                        continue
                    file_tag_values = list(device.segments[1 : 1 + len(file_tag_cols)])
                    file_tag_dict = dict(zip(file_tag_cols, file_tag_values))
                    unified_key = tuple(file_tag_dict.get(c) for c in self._tag_cols)
                    if any(v is None for v in unified_key):
                        raise ValueError(
                            f"Device in file '{file}' has missing tag values: "
                            f"{dict(zip(self._tag_cols, unified_key))}. "
                            "Schema-evolution devices with NULL tag values are not "
                            "supported because tsfile lacks an IS NULL tag filter."
                        )
                    if unified_key not in device_to_files:
                        device_to_files[unified_key] = []
                        device_order.append(unified_key)
                    device_to_files[unified_key].append(file)
            except Exception as e:
                if self._should_reraise(file, e):
                    raise
                file_meta.pop(file, None)
                continue

        device_index = [(key, device_to_files[key]) for key in device_order]
        return device_index, file_meta

    def _iter_device_batches(self, device_index, file_meta, readers, target_schema: pa.Schema):
        """Materialize devices in order and emit packed Arrow tables."""
        field_names = list(self._field_inner.keys())
        rows: list[dict] = []
        batch_idx = 0
        for device_key, contributing_files in device_index:
            time_chunks: list[np.ndarray] = []
            field_chunks: dict[str, list] = {f: [] for f in field_names}
            for file in contributing_files:
                if file not in file_meta:
                    continue
                try:
                    ts_arr, vals = self._read_device_from_file(readers[file], file_meta[file], device_key)
                except Exception as e:
                    if self._should_reraise(file, e):
                        raise
                    continue
                if len(ts_arr) == 0:
                    continue
                time_chunks.append(ts_arr)
                for f in field_names:
                    field_chunks[f].append(vals.get(f))  # None → all-null contribution
            if not time_chunks:
                continue  # device produced no rows in time range → skip

            row = self._finalize_device(device_key, time_chunks, field_chunks, field_names)
            rows.append(row)
            if len(rows) >= self.config.output_batch_size:
                yield Key(0, batch_idx), self._rows_to_table(rows, target_schema)
                rows = []
                batch_idx += 1
        if rows:
            yield Key(0, batch_idx), self._rows_to_table(rows, target_schema)

    def _read_device_from_file(self, reader, meta: dict, device_key: tuple) -> tuple:
        """Stream one device's rows from one file via ``query_table`` pushdown.

        Returns ``(timestamps, {field_name: values})``. The dict only includes
        field columns that this file owns *and* that the builder requested;
        callers fill missing fields with all-null contributions.
        """
        from tsfile import tag_eq

        file_tag_cols: list[str] = meta["tag_cols"]
        file_field_cols: set[str] = meta["field_cols"]
        time_col: str = meta["time_col"]

        # Build the tag filter only over this file's tag columns. The unified
        # device key carries one value per builder tag; map back by name.
        unified_to_value = dict(zip(self._tag_cols, device_key))
        tag_filter = None
        for c in file_tag_cols:
            v = unified_to_value.get(c)
            if v is None:
                # Caught earlier in _build_device_index; defensive guard.
                return np.array([], dtype=np.int64), {}
            expr = tag_eq(c, str(v))
            tag_filter = expr if tag_filter is None else tag_filter & expr

        # Project: requested fields ∩ this file's fields. ``query_table``
        # always returns the time column, but it requires at least one
        # non-time column — fall back to any owned field if the user's
        # selection has nothing in this file.
        requested = list(self._field_inner.keys())
        fields_to_query = [f for f in requested if f in file_field_cols]
        fallback_only = False
        if not fields_to_query:
            if not file_field_cols:
                return np.array([], dtype=np.int64), {}
            fields_to_query = [next(iter(file_field_cols))]
            fallback_only = True

        kwargs: dict = {"tag_filter": tag_filter, "batch_size": self.config.input_batch_size}
        if self.config.start_time is not None:
            kwargs["start_time"] = self.config.start_time
        if self.config.end_time is not None:
            kwargs["end_time"] = self.config.end_time

        ts_parts: list[np.ndarray] = []
        field_parts: dict[str, list] = {f: [] for f in fields_to_query}
        with reader.query_table(self._table, fields_to_query, **kwargs) as rs:
            while True:
                batch = rs.read_arrow_batch()
                if batch is None:
                    break
                if batch.num_rows == 0:
                    continue
                ts_parts.append(np.asarray(batch.column(time_col).to_numpy(), dtype=np.int64))
                for f in fields_to_query:
                    col = batch.column(f)
                    # tsfile's arrow reader tags TIMESTAMP / DATE field columns
                    # with a fixed unit (e.g. ``timestamp[ns]``) regardless of
                    # the value's original write unit. Reinterpret as raw
                    # int64/int32 ticks so the downstream
                    # ``pa.array(type=timestamp[<our unit>])`` treats them as
                    # ticks in the unit declared by our schema, instead of
                    # cross-unit casting (which would raise on data loss).
                    if pa.types.is_timestamp(col.type):
                        field_parts[f].append(col.cast(pa.int64()).to_numpy(zero_copy_only=False))
                    elif pa.types.is_date(col.type):
                        field_parts[f].append(col.cast(pa.int32()).to_numpy(zero_copy_only=False))
                    else:
                        field_parts[f].append(col.to_numpy(zero_copy_only=False))

        if not ts_parts:
            return np.array([], dtype=np.int64), {}
        ts_full = np.concatenate(ts_parts) if len(ts_parts) > 1 else ts_parts[0]
        vals_full = {f: (np.concatenate(parts) if len(parts) > 1 else parts[0]) for f, parts in field_parts.items()}

        # Defensive boundary mask: native query paths may emit rows just
        # outside the requested window in some chunk-boundary cases.
        if self.config.start_time is not None or self.config.end_time is not None:
            lo = self.config.start_time if self.config.start_time is not None else np.iinfo(np.int64).min
            hi = self.config.end_time if self.config.end_time is not None else np.iinfo(np.int64).max
            mask = (ts_full >= lo) & (ts_full <= hi)
            if not mask.all():
                ts_full = ts_full[mask]
                vals_full = {f: arr[mask] for f, arr in vals_full.items()}

        # Drop the fallback "pick one" column from the user-visible payload.
        if fallback_only:
            vals_full = {}
        return ts_full, vals_full

    def _finalize_device(
        self,
        device_key: tuple,
        time_chunks: list,
        field_chunks: dict,
        field_names: list[str],
    ) -> dict:
        """Concatenate per-file chunks, sort by time, and return one row.

        Raises ``ValueError`` if the same timestamp appears more than once
        for a device (within or across files) — tsfile's per-device timeline
        is required to be unique-by-timestamp.
        """
        time_arr = np.concatenate(time_chunks) if time_chunks else np.array([], dtype=np.int64)
        n_total = len(time_arr)

        if n_total > 0:
            sort_idx = np.argsort(time_arr, kind="stable")
            time_sorted = time_arr[sort_idx]
            if n_total > 1:
                dup_mask = time_sorted[1:] == time_sorted[:-1]
                if dup_mask.any():
                    dup_ts = int(time_sorted[1:][dup_mask][0])
                    raise ValueError(
                        f"Duplicate timestamp {dup_ts} for device "
                        f"{dict(zip(self._tag_cols, device_key))}. "
                        "Cross-file or within-file duplicate timestamps are not supported."
                    )
        else:
            sort_idx = None
            time_sorted = time_arr

        row: dict = {}
        for tag_name, tag_val in zip(self._tag_cols, device_key):
            row[tag_name] = None if tag_val is None else str(tag_val)
        row[self._time_col] = time_sorted

        for fname in field_names:
            chunks = field_chunks.get(fname, [])
            materialized: list = []
            for tchunk, fchunk in zip(time_chunks, chunks):
                if fchunk is None:
                    materialized.append(np.full(len(tchunk), None, dtype=object))
                else:
                    materialized.append(fchunk)
            arr = np.concatenate(materialized) if materialized else np.array([], dtype=object)
            if sort_idx is not None and len(arr) == n_total:
                arr = arr[sort_idx]
            row[fname] = arr
        return row

    # ----- arrow assembly ----------------------------------------------

    def _rows_to_table(self, rows: list[dict], target_schema: pa.Schema) -> pa.Table:
        """Convert a batch of row dicts into an Arrow table matching ``target_schema``."""
        arrays: list[pa.Array] = []
        for f in target_schema:
            values = [r[f.name] for r in rows]
            if pa.types.is_list(f.type):
                arrays.append(self._build_list_array(values, f.type))
            else:
                arrays.append(pa.array(values, type=f.type))
        pa_table = pa.Table.from_arrays(arrays, names=[f.name for f in target_schema])
        return table_cast(pa_table, target_schema)

    @staticmethod
    def _build_list_array(values: list, list_type: pa.ListType) -> pa.ListArray:
        """Build a ``ListArray`` from a list of per-row 1D arrays / sequences."""
        inner_type = list_type.value_type
        offsets = [0]
        flat_chunks: list = []
        total = 0
        for v in values:
            if v is None:
                length = 0
            else:
                length = len(v)
                flat_chunks.append(v)
            total += length
            offsets.append(total)

        if flat_chunks:
            try:
                flat = np.concatenate([np.asarray(c) for c in flat_chunks])
            except ValueError:
                # Heterogeneous shapes / dtypes → fall back to a Python list.
                flat = []
                for c in flat_chunks:
                    flat.extend(list(c))
            flat_arr = pa.array(flat, type=inner_type, from_pandas=True)
        else:
            flat_arr = pa.array([], type=inner_type)

        return pa.ListArray.from_arrays(pa.array(offsets, type=pa.int32()), flat_arr)

    # ----- file / error handling ---------------------------------------

    @staticmethod
    def _open_reader(file: str):
        """Open a file as a ``TsFileReader`` after verifying its magic header.

        The C library's ``TsFileReader`` constructor silently returns an
        invalid handle for non-tsfile inputs, and any subsequent call on it
        segfaults. The 6-byte ``TsFile`` magic header is checked first to
        bail out cleanly.
        """
        from tsfile import TsFileReader

        try:
            with open(file, "rb") as fh:
                header = fh.read(len(_TSFILE_MAGIC))
        except OSError as e:
            raise ValueError(f"Cannot open file {file!r}: {e}") from e
        if header != _TSFILE_MAGIC:
            raise ValueError(f"File {file!r} is not a valid TsFile (bad magic header).")
        return TsFileReader(file)

    @staticmethod
    def _require_table_model(file: str, schemas) -> None:
        if not schemas:
            raise ValueError(
                f"File {file!r} is a tree-model TsFile, which is not supported. "
                "Only table-model TsFiles can be loaded."
            )

    @staticmethod
    def _schemas_by_lc(reader) -> dict:
        """Return ``get_all_table_schemas()`` keyed by lowercased table name.

        TsFile / IoTDB treat table names case-insensitively, but the Python
        binding's ``get_all_table_schemas()`` returns a dict keyed by whatever
        casing the file was written with. Lowercasing the keys here lets all
        downstream lookups use a single canonical form.
        """
        return {name.lower(): schema for name, schema in reader.get_all_table_schemas().items()}

    def _should_reraise(self, file: str, exc: BaseException) -> bool:
        """Apply ``on_bad_files`` policy. Returns True iff the caller should re-raise."""
        mode = self.config.on_bad_files
        if mode == "error":
            logger.error(f"Failed to read file '{file}' with error {type(exc).__name__}: {exc}")
            return True
        if mode == "warn":
            logger.warning(f"Skipping bad file '{file}'. {type(exc).__name__}: {exc}")
        else:
            logger.debug(f"Skipping bad file '{file}'. {type(exc).__name__}: {exc}")
        return False
