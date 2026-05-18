"""Tests for the per-device wide-format TsFile builder."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any, Sequence

import pyarrow as pa
import pytest
from tsfile import ColumnCategory, ColumnSchema, TableSchema, Tablet, TsFileWriter
from tsfile.constants import TSDataType

from datasets import IterableDataset, load_dataset
from datasets.builder import InvalidConfigName
from datasets.data_files import DataFilesList
from datasets.packaged_modules.tsfile.tsfile import TsFileConfig, _to_epoch


# ---------------------------------------------------------------------------
# Time-base constants
# ---------------------------------------------------------------------------
#
# Every fixture's timestamps live in a disjoint epoch-ms slice off ``T0`` so
# that, when two files of the same device are merged, the resulting
# time-sorted order is fully determined by writer-side timestamps. This lets
# the assertions below check both *content* and *order* unambiguously.
T0 = 1_700_000_000_000  # base: single_device, multi_device, all_types
T_EVOLVED = T0 + 500_000  # evolved file (after single_device's 5 points)
T_INT32 = T0 + 1_000_000
T_INT64 = T0 + 2_000_000
T_FLOAT = T0 + 3_000_000


# ---------------------------------------------------------------------------
# Generic writer
# ---------------------------------------------------------------------------


# A row maps column name -> Python value, plus a special "time" -> int (epoch).
Row = dict[str, Any]
ColumnSpec = tuple[str, TSDataType, ColumnCategory]


def _write_tsfile(path: str, tables: Sequence[tuple[str, Sequence[ColumnSpec], Sequence[Sequence[Row]]]]) -> None:
    """Write one or more tables, each as one or more tablets, to ``path``.

    Each ``tables`` entry is ``(table_name, columns, tablets)`` where:

    - ``columns`` is the table schema as ``[(name, TSDataType, ColumnCategory), ...]``;
      it must include exactly one TIME column called ``"time"``.
    - ``tablets`` is a list of tablets; each tablet is a list of row dicts. A
      row dict must carry ``"time"`` plus every TAG/FIELD column in the table.
    """
    writer = TsFileWriter(path)
    try:
        # Register schemas first so multiple-table files validate up-front.
        for table_name, columns, _ in tables:
            writer.register_table(TableSchema(table_name, [ColumnSchema(*c) for c in columns]))

        for table_name, columns, tablets in tables:
            non_time = [(n, t) for (n, t, c) in columns if c != ColumnCategory.TIME]
            col_names = [n for n, _ in non_time]
            col_types = [t for _, t in non_time]
            for rows in tablets:
                tablet = Tablet(col_names, col_types, len(rows))
                tablet.set_table_name(table_name)
                for i, row in enumerate(rows):
                    tablet.add_timestamp(i, row["time"])
                    for name in col_names:
                        tablet.add_value_by_name(name, i, row[name])
                writer.write_table(tablet)
    finally:
        writer.close()


# ---------------------------------------------------------------------------
# Per-fixture writers (each declarative + tiny)
# ---------------------------------------------------------------------------


def _write_single_device(path: str) -> None:
    """One device 'd1', two DOUBLE fields, 5 points starting at T0."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("temperature", TSDataType.DOUBLE, ColumnCategory.FIELD),
        ("humidity", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    rows = [{"time": T0 + i * 1000, "device": "d1", "temperature": 20.0 + i, "humidity": 50.0 + i} for i in range(5)]
    _write_tsfile(path, [("mytable", cols, [rows])])


def _write_multi_device(path: str) -> None:
    """Three devices, 3 points each, all sharing the same field schema."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("temperature", TSDataType.DOUBLE, ColumnCategory.FIELD),
        ("humidity", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    tablets = [
        [{"time": T0 + i * 1000, "device": dev, "temperature": 10.0 + i, "humidity": 50.0 + i} for i in range(3)]
        for dev in ("d1", "d2", "d3")
    ]
    _write_tsfile(path, [("plant", cols, tablets)])


def _write_evolved(path: str) -> None:
    """Same table+device as single_device, plus a new ``voltage`` field."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("temperature", TSDataType.DOUBLE, ColumnCategory.FIELD),
        ("humidity", TSDataType.DOUBLE, ColumnCategory.FIELD),
        ("voltage", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    rows = [
        {
            "time": T_EVOLVED + i * 1000,
            "device": "d1",
            "temperature": 30.0 + i,
            "humidity": 60.0 + i,
            "voltage": 220.0 + i,
        }
        for i in range(3)
    ]
    _write_tsfile(path, [("mytable", cols, [rows])])


def _write_numeric_field(path: str, ts_type: TSDataType, base_ts: int, value_fn) -> None:
    """One device 'd1' with a single numeric ``temperature`` field."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("temperature", ts_type, ColumnCategory.FIELD),
    ]
    rows = [{"time": base_ts + i * 1000, "device": "d1", "temperature": value_fn(i)} for i in range(3)]
    _write_tsfile(path, [("mytable", cols, [rows])])


def _write_two_tables(path: str) -> None:
    """Two distinct tables in one file: ``table_a`` (registered first) and ``table_b``."""
    a_cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("a", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    b_cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("b", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    a_rows = [{"time": 1_000 + i, "device": "d1", "a": float(i)} for i in range(2)]
    b_rows = [{"time": 2_000 + i, "device": "d1", "b": 100.0 + i} for i in range(2)]
    _write_tsfile(path, [("table_a", a_cols, [a_rows]), ("table_b", b_cols, [b_rows])])


def _write_all_types(path: str) -> None:
    """Every supported TSDataType represented as a FIELD."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("tag", TSDataType.STRING, ColumnCategory.TAG),
        ("col_boolean", TSDataType.BOOLEAN, ColumnCategory.FIELD),
        ("col_int32", TSDataType.INT32, ColumnCategory.FIELD),
        ("col_int64", TSDataType.INT64, ColumnCategory.FIELD),
        ("col_float", TSDataType.FLOAT, ColumnCategory.FIELD),
        ("col_double", TSDataType.DOUBLE, ColumnCategory.FIELD),
        ("col_text", TSDataType.TEXT, ColumnCategory.FIELD),
        ("col_string", TSDataType.STRING, ColumnCategory.FIELD),
        ("col_timestamp", TSDataType.TIMESTAMP, ColumnCategory.FIELD),
        ("col_date", TSDataType.DATE, ColumnCategory.FIELD),
        ("col_blob", TSDataType.BLOB, ColumnCategory.FIELD),
    ]
    rows = [
        {
            "time": T0 + i * 1000,
            "tag": "d1",
            "col_boolean": i % 2 == 0,
            "col_int32": 100 + i,
            "col_int64": 1_000_000 + i,
            "col_float": 1.5 + i,
            "col_double": 100.5 + i,
            "col_text": f"text_{i}",
            "col_string": f"str_{i}",
            "col_timestamp": 1_600_000_000_000 + i * 1000,
            "col_date": date(2024, 1, 1 + i),
            "col_blob": f"blob{i}".encode(),
        }
        for i in range(3)
    ]
    _write_tsfile(path, [("alltypes", cols, [rows])])


def _write_large_device(path: str, n_points: int = 200) -> None:
    """Single device with many points, used to exercise multi-batch concat."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("v", TSDataType.INT64, ColumnCategory.FIELD),
    ]
    rows = [{"time": T0 + i, "device": "d1", "v": i} for i in range(n_points)]
    _write_tsfile(path, [("mytable", cols, [rows])])


def _write_two_devices_subset(path: str, devices: Sequence[str], base_ts: int) -> None:
    """A multi-device fixture used to assemble cross-file device sets."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("v", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    tablets = [[{"time": base_ts + i * 1000, "device": dev, "v": float(i)} for i in range(3)] for dev in devices]
    _write_tsfile(path, [("mytable", cols, tablets)])


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def make_tsfile(tmp_path):
    """Factory fixture: ``make_tsfile("name", writer_fn, *args, **kwargs)``."""

    def _make(name: str, writer_fn, *args, **kwargs) -> str:
        p = str(tmp_path / f"{name}.tsfile")
        writer_fn(p, *args, **kwargs)
        return p

    return _make


@pytest.fixture
def tsfile_path(make_tsfile):
    return make_tsfile("sample", _write_single_device)


@pytest.fixture
def multi_device_tsfile_path(make_tsfile):
    return make_tsfile("multi", _write_multi_device)


@pytest.fixture
def evolved_tsfile_path(make_tsfile):
    return make_tsfile("evolved", _write_evolved)


@pytest.fixture
def two_tables_tsfile_path(make_tsfile):
    return make_tsfile("two_tables", _write_two_tables)


@pytest.fixture
def all_types_tsfile_path(make_tsfile):
    return make_tsfile("alltypes", _write_all_types)


# ---------------------------------------------------------------------------
# Config-level
# ---------------------------------------------------------------------------


def test_config_raises_when_invalid_name():
    with pytest.raises(InvalidConfigName, match="Bad characters"):
        TsFileConfig(name="name-with-*-invalid-character")


@pytest.mark.parametrize("data_files", ["str_path", ["str_path"], DataFilesList(["str_path"], [()])])
def test_config_raises_when_invalid_data_files(data_files):
    with pytest.raises(ValueError, match="Expected a DataFilesDict"):
        TsFileConfig(name="name", data_files=data_files)


@pytest.mark.parametrize(
    "kwargs, match",
    [
        ({"input_batch_size": 0}, "input_batch_size"),
        ({"output_batch_size": 0}, "output_batch_size"),
        ({"columns": []}, "non-empty"),
        ({"timestamp_unit": "minute"}, "timestamp_unit"),
        ({"on_bad_files": "boom"}, "on_bad_files"),
    ],
)
def test_config_rejects_invalid_values(kwargs, match):
    with pytest.raises(ValueError, match=match):
        TsFileConfig(name="x", **kwargs)


def test_config_normalizes_time_bounds():
    cfg = TsFileConfig(
        name="x",
        start_time=pa.scalar(1500, type=pa.timestamp("ms")),
        end_time=2000,
    )
    assert cfg.start_time == 1500
    assert cfg.end_time == 2000


# ---------------------------------------------------------------------------
# _to_epoch unit tests
# ---------------------------------------------------------------------------


def test_to_epoch_int_passthrough():
    assert _to_epoch(1234, "ms") == 1234


def test_to_epoch_naive_datetime():
    assert _to_epoch(datetime(1970, 1, 1, 0, 0, 1), "ms") == 1000


@pytest.mark.parametrize(
    "aware",
    [
        datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=8))),
        "2024-01-01T00:00:00+08:00",
    ],
    ids=["datetime", "iso_string"],
)
def test_to_epoch_aware_inputs_normalized_to_utc(aware):
    # 2024-01-01T00:00:00 in UTC+8 == 2023-12-31T16:00:00 UTC.
    naive_utc = datetime(2023, 12, 31, 16, 0, 0)
    assert _to_epoch(aware, "ms") == _to_epoch(naive_utc, "ms")


def test_to_epoch_date():
    assert _to_epoch(date(1970, 1, 2), "ms") == 86_400_000


def test_to_epoch_iso_string():
    assert _to_epoch("1970-01-01T00:00:01", "ms") == 1000


def test_to_epoch_pa_scalar():
    assert _to_epoch(pa.scalar(1500, type=pa.timestamp("ms")), "ms") == 1500


def test_to_epoch_rejects_bool():
    with pytest.raises(TypeError, match="bool"):
        _to_epoch(True, "ms")


@pytest.mark.parametrize("value", [object(), b"bytes", "not-a-date"])
def test_to_epoch_rejects_garbage(value):
    with pytest.raises(TypeError, match="must be a"):
        _to_epoch(value, "ms")


# ---------------------------------------------------------------------------
# End-to-end: single device, full table
# ---------------------------------------------------------------------------


def test_load_full_table(tsfile_path):
    ds = load_dataset("tsfile", data_files=tsfile_path)["train"]

    # One row per device. TAG = scalar string; time + fields = lists.
    assert ds.column_names == ["device", "time", "temperature", "humidity"]
    assert len(ds) == 1
    row = ds[0]
    assert row["device"] == "d1"
    assert len(row["time"]) == 5
    assert row["time"][0] == datetime(2023, 11, 14, 22, 13, 20)
    assert row["time"][-1] == datetime(2023, 11, 14, 22, 13, 24)
    assert row["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0]
    assert row["humidity"] == [50.0, 51.0, 52.0, 53.0, 54.0]


def test_load_with_field_subset(tsfile_path):
    ds = load_dataset("tsfile", data_files=tsfile_path, columns=["temperature"])["train"]
    assert ds.column_names == ["device", "time", "temperature"]
    assert ds[0]["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0]


def test_columns_are_lowercased(tsfile_path):
    ds = load_dataset("tsfile", data_files=tsfile_path, columns=["TEMPERATURE", "Humidity"])["train"]
    assert ds.column_names == ["device", "time", "temperature", "humidity"]


def test_columns_request_tag_is_silently_ignored(tsfile_path):
    """Passing a TAG name in `columns` is a no-op (TAGs are always emitted)."""
    ds = load_dataset("tsfile", data_files=tsfile_path, columns=["device", "temperature"])["train"]

    assert ds.column_names == ["device", "time", "temperature"]
    assert ds.features["device"].dtype == "string"
    assert ds.features["temperature"].feature.dtype == "float64"
    assert ds["device"] == ["d1"]
    assert ds[0]["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0]


def test_columns_request_time_is_silently_ignored(tsfile_path):
    """Passing the TIME column name in `columns` is a no-op (TIME is always emitted)."""
    ds = load_dataset("tsfile", data_files=tsfile_path, columns=["time", "temperature"])["train"]

    # `time` should appear exactly once, and as the real timestamp list — not
    # as a duplicate all-null float64 list column.
    assert ds.column_names == ["device", "time", "temperature"]
    assert ds.features["time"].feature.dtype.startswith("timestamp")
    row = ds[0]
    assert len(row["time"]) == 5
    assert row["time"][0] == datetime(2023, 11, 14, 22, 13, 20)
    assert row["time"][-1] == datetime(2023, 11, 14, 22, 13, 24)
    assert row["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0]


def test_columns_request_only_time(tsfile_path):
    """`columns=["time"]` should still produce TAG + TIME, with no FIELD list columns."""
    ds = load_dataset("tsfile", data_files=tsfile_path, columns=["time"])["train"]

    assert ds.column_names == ["device", "time"]
    assert ds.features["time"].feature.dtype.startswith("timestamp")
    row = ds[0]
    assert row["device"] == "d1"
    assert len(row["time"]) == 5
    assert row["time"][0] == datetime(2023, 11, 14, 22, 13, 20)
    assert row["time"][-1] == datetime(2023, 11, 14, 22, 13, 24)


def test_columns_unknown_field_filled_with_null(tsfile_path):
    ds = load_dataset(
        "tsfile",
        data_files=tsfile_path,
        columns=["temperature", "voltage"],  # voltage is absent
    )["train"]

    assert ds.column_names == ["device", "time", "temperature", "voltage"]
    row = ds[0]
    assert row["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0]
    assert row["voltage"] == [None] * 5


def test_columns_all_unknown_still_returns_time_and_tags(tsfile_path):
    ds = load_dataset(
        "tsfile",
        data_files=tsfile_path,
        columns=["nonexistent_a", "nonexistent_b"],
    )["train"]

    assert ds.column_names == ["device", "time", "nonexistent_a", "nonexistent_b"]
    row = ds[0]
    assert row["device"] == "d1"
    assert len(row["time"]) == 5
    assert row["nonexistent_a"] == [None] * 5
    assert row["nonexistent_b"] == [None] * 5


# ---------------------------------------------------------------------------
# Time-range filtering
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "start, end",
    [
        # pa.scalar from datetime
        (
            pa.scalar(datetime(2023, 11, 14, 22, 13, 21), type=pa.timestamp("ms")),
            pa.scalar(datetime(2023, 11, 14, 22, 13, 23), type=pa.timestamp("ms")),
        ),
        # pa.scalar from int epoch
        (
            pa.scalar(T0 + 1000, type=pa.timestamp("ms")),
            pa.scalar(T0 + 3000, type=pa.timestamp("ms")),
        ),
        # plain int epoch
        (T0 + 1000, T0 + 3000),
        # datetime
        (datetime(2023, 11, 14, 22, 13, 21), datetime(2023, 11, 14, 22, 13, 23)),
        # ISO-8601 string
        ("2023-11-14T22:13:21", "2023-11-14T22:13:23"),
    ],
)
def test_load_with_time_range_inputs(tsfile_path, start, end):
    ds = load_dataset("tsfile", data_files=tsfile_path, start_time=start, end_time=end)["train"]
    assert len(ds[0]["time"]) == 3


# ---------------------------------------------------------------------------
# Multi-device & cross-file folding
# ---------------------------------------------------------------------------


def test_load_multi_device_one_row_per_device(multi_device_tsfile_path):
    ds = load_dataset("tsfile", data_files=multi_device_tsfile_path)["train"]

    assert len(ds) == 3
    assert sorted(ds["device"]) == ["d1", "d2", "d3"]
    for row in ds:
        assert len(row["time"]) == 3
        assert row["temperature"] == [10.0, 11.0, 12.0]
        assert row["humidity"] == [50.0, 51.0, 52.0]


def test_schema_evolution_merges_same_device(tsfile_path, evolved_tsfile_path):
    """Same device d1 in two files → one row, lists merged in time order."""
    ds = load_dataset("tsfile", data_files=[tsfile_path, evolved_tsfile_path])["train"]

    assert "voltage" in ds.column_names
    assert len(ds) == 1
    row = ds[0]
    assert row["device"] == "d1"
    # 5 (old) + 3 (new) points, fully time-ordered.
    assert len(row["time"]) == 8
    # Old file lacked `voltage` → null on its 5 points; new file fills the rest.
    assert row["voltage"] == [None] * 5 + [220.0, 221.0, 222.0]
    # `temperature` is present in both files, contiguous in the merged order.
    assert row["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0, 30.0, 31.0, 32.0]


def test_multi_file_multi_device_partial_overlap(make_tsfile):
    """Two files × two devices each, with one device shared.

    File A: devices {d1, d2}; file B: devices {d2, d3}. The merged dataset
    must have 3 rows (one per unique device), and d2 must have *6* points
    (3 from each file) sorted by time.
    """
    fa = make_tsfile("a", _write_two_devices_subset, devices=["d1", "d2"], base_ts=T0)
    fb = make_tsfile("b", _write_two_devices_subset, devices=["d2", "d3"], base_ts=T0 + 100_000)

    ds = load_dataset("tsfile", data_files=[fa, fb])["train"]
    by_dev = {row["device"]: row for row in ds}
    assert set(by_dev) == {"d1", "d2", "d3"}
    assert len(by_dev["d1"]["time"]) == 3
    assert len(by_dev["d3"]["time"]) == 3
    # Shared device gets all 6 points, time-sorted (file A first, then B).
    assert len(by_dev["d2"]["time"]) == 6
    assert by_dev["d2"]["v"] == [0.0, 1.0, 2.0, 0.0, 1.0, 2.0]


# ---------------------------------------------------------------------------
# Type promotion across files
# ---------------------------------------------------------------------------


def test_type_promotion_int32_to_int64(make_tsfile):
    int32_path = make_tsfile("narrow", _write_numeric_field, TSDataType.INT32, T_INT32, lambda i: 10 + i)
    int64_path = make_tsfile("wide", _write_numeric_field, TSDataType.INT64, T_INT64, lambda i: 1_000_000 + i)

    ds = load_dataset("tsfile", data_files=[int32_path, int64_path])["train"]
    assert len(ds) == 1
    assert ds.features["temperature"].feature.dtype == "int64"
    # int32 timestamps come earlier (T_INT32 < T_INT64).
    assert ds[0]["temperature"] == [10, 11, 12, 1_000_000, 1_000_001, 1_000_002]


def test_type_promotion_float_to_double(make_tsfile):
    float_path = make_tsfile("narrow", _write_numeric_field, TSDataType.FLOAT, T_FLOAT, lambda i: 1.5 + i)
    double_path = make_tsfile("wide", _write_single_device)

    ds = load_dataset("tsfile", data_files=[float_path, double_path])["train"]
    assert len(ds) == 1
    assert ds.features["temperature"].feature.dtype == "float64"
    # double fixture lives at T0..T0+4s; float at T_FLOAT (later).
    assert ds[0]["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0, 1.5, 2.5, 3.5]


def test_type_promotion_int32_to_double(make_tsfile):
    int32_path = make_tsfile("int", _write_numeric_field, TSDataType.INT32, T_INT32, lambda i: 10 + i)
    double_path = make_tsfile("double", _write_single_device)

    ds = load_dataset("tsfile", data_files=[int32_path, double_path])["train"]
    assert len(ds) == 1
    # INT32 + DOUBLE → DOUBLE (two-step widening).
    assert ds.features["temperature"].feature.dtype == "float64"
    assert ds[0]["temperature"] == [20.0, 21.0, 22.0, 23.0, 24.0, 10.0, 11.0, 12.0]


# ---------------------------------------------------------------------------
# All-types
# ---------------------------------------------------------------------------


def test_load_all_supported_types(all_types_tsfile_path):
    ds = load_dataset("tsfile", data_files=all_types_tsfile_path)["train"]

    assert len(ds) == 1
    assert ds.column_names == [
        "tag",
        "time",
        "col_boolean",
        "col_int32",
        "col_int64",
        "col_float",
        "col_double",
        "col_text",
        "col_string",
        "col_timestamp",
        "col_date",
        "col_blob",
    ]
    row = ds[0]
    assert row["tag"] == "d1"
    assert row["col_boolean"] == [True, False, True]
    assert row["col_int32"] == [100, 101, 102]
    assert row["col_int64"] == [1_000_000, 1_000_001, 1_000_002]
    assert row["col_float"] == [1.5, 2.5, 3.5]
    assert row["col_double"] == [100.5, 101.5, 102.5]
    assert row["col_text"] == ["text_0", "text_1", "text_2"]
    assert row["col_string"] == ["str_0", "str_1", "str_2"]
    assert row["col_timestamp"][0] == datetime(2020, 9, 13, 12, 26, 40)
    assert row["col_date"][0] == date(2024, 1, 1)
    assert row["col_date"][2] == date(2024, 1, 3)
    assert row["col_blob"][0] == b"blob0"
    assert row["col_blob"][2] == b"blob2"


# ---------------------------------------------------------------------------
# Multi-table file: explicit `table_name` selection
# ---------------------------------------------------------------------------


def test_default_table_is_first(two_tables_tsfile_path):
    ds = load_dataset("tsfile", data_files=two_tables_tsfile_path)["train"]
    # `table_a` registered first → default pick.
    assert "a" in ds.column_names
    assert "b" not in ds.column_names


def test_explicit_table_name(two_tables_tsfile_path):
    ds = load_dataset("tsfile", data_files=two_tables_tsfile_path, table_name="table_b")["train"]
    assert "b" in ds.column_names
    assert "a" not in ds.column_names


# ---------------------------------------------------------------------------
# Streaming (IterableDataset)
# ---------------------------------------------------------------------------


def test_streaming_yields_same_rows(multi_device_tsfile_path):
    ds = load_dataset("tsfile", data_files=multi_device_tsfile_path, streaming=True)["train"]
    assert isinstance(ds, IterableDataset)
    rows = list(ds)
    assert len(rows) == 3
    assert sorted(r["device"] for r in rows) == ["d1", "d2", "d3"]
    for r in rows:
        assert r["temperature"] == [10.0, 11.0, 12.0]


# ---------------------------------------------------------------------------
# Timezone
# ---------------------------------------------------------------------------


def test_load_with_timezone(make_tsfile):
    """`timestamp_tz="UTC"` round-trips: list values come back tz-aware."""
    path = make_tsfile("tz", _write_single_device)
    ds = load_dataset("tsfile", data_files=path, timestamp_tz="UTC")["train"]
    ts = ds[0]["time"][0]
    assert ts.tzinfo is not None
    # Same wall-clock as the naive case, attached to UTC.
    assert ts == datetime(2023, 11, 14, 22, 13, 20, tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Large-batch / multi-chunk concat
# ---------------------------------------------------------------------------


def test_large_device_with_small_batch_size(make_tsfile):
    """Force multiple Arrow batches per device → exercise the concat path."""
    path = make_tsfile("big", _write_large_device, n_points=200)
    ds = load_dataset("tsfile", data_files=path, input_batch_size=64)["train"]
    assert len(ds) == 1
    row = ds[0]
    assert len(row["time"]) == 200
    assert row["v"] == list(range(200))


# ---------------------------------------------------------------------------
# Duplicate-timestamp detection (cross-file)
# ---------------------------------------------------------------------------


def test_duplicate_timestamp_across_files_raises(make_tsfile):
    """Same device, same ts in two files → `_finalize_device` must raise."""
    cols = [
        ("time", TSDataType.TIMESTAMP, ColumnCategory.TIME),
        ("device", TSDataType.STRING, ColumnCategory.TAG),
        ("v", TSDataType.DOUBLE, ColumnCategory.FIELD),
    ]
    rows = [{"time": 5_000, "device": "d1", "v": 1.0}]

    a = make_tsfile("dupA", lambda p: _write_tsfile(p, [("mytable", cols, [rows])]))
    b = make_tsfile("dupB", lambda p: _write_tsfile(p, [("mytable", cols, [rows])]))

    with pytest.raises(Exception) as excinfo:
        load_dataset("tsfile", data_files=[a, b])
    # The ValueError is wrapped by `_prepare_split_single` into a
    # DatasetGenerationError; check the cause chain for the original message.
    chain = [excinfo.value, *(_iter_causes(excinfo.value))]
    assert any("Duplicate timestamp" in str(e) for e in chain)


def _iter_causes(exc: BaseException):
    while exc.__cause__ is not None:
        exc = exc.__cause__
        yield exc


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def test_on_bad_files_skip(tmp_path, tsfile_path):
    bad = tmp_path / "broken.tsfile"
    bad.write_bytes(b"not a real tsfile")

    ds = load_dataset(
        "tsfile",
        data_files=[tsfile_path, str(bad)],
        on_bad_files="skip",
    )["train"]
    assert len(ds) == 1
    assert len(ds[0]["time"]) == 5


def test_on_bad_files_warn(tmp_path, tsfile_path, caplog):
    bad = tmp_path / "broken.tsfile"
    bad.write_bytes(b"not a real tsfile")

    with caplog.at_level(logging.WARNING, logger="datasets.packaged_modules.tsfile.tsfile"):
        ds = load_dataset(
            "tsfile",
            data_files=[tsfile_path, str(bad)],
            on_bad_files="warn",
        )["train"]
    assert len(ds) == 1
    assert any("Skipping bad file" in rec.message for rec in caplog.records)


def test_on_bad_files_default_raises(tmp_path, tsfile_path):
    bad = tmp_path / "broken.tsfile"
    bad.write_bytes(b"not a real tsfile")

    with pytest.raises(Exception) as excinfo:
        load_dataset("tsfile", data_files=[tsfile_path, str(bad)])
    chain = [excinfo.value, *(_iter_causes(excinfo.value))]
    assert any("not a valid TsFile" in str(e) for e in chain)
