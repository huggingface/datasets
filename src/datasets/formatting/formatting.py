from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, TypeVar, Union

import numpy as np
import pandas as pd
import pyarrow as pa

from ..features import pandas_types_mapper


T = TypeVar("T")

RowFormat = TypeVar("RowFormat")
ColumnFormat = TypeVar("ColumnFormat")
BatchFormat = TypeVar("BatchFormat")


def _is_range_contiguous(key: range) -> bool:
    return key.step == 1 and key.stop >= key.start


def _raise_bad_key_type(key: Any):
    raise ValueError(
        f"Wrong key type: '{key}' of type '{type(key)}'. Expected one of int, slice, range, str or Iterable."
    )


def _query_table_with_indices_mapping(
    pa_table: pa.Table, key: Union[int, slice, range, str, Iterable], indices: pa.lib.UInt64Array
) -> pa.Table:
    if isinstance(key, int):
        return _query_table(pa_table, indices[key].as_py())
    if isinstance(key, slice):
        key = range(*key.indices(pa_table.num_rows))
    if isinstance(key, range):
        if _is_range_contiguous(key):
            return _query_table(pa_table, (i.as_py() for i in indices.slice(key.start, key.stop - key.start)))
        else:
            pass  # treat as an iterable
    if isinstance(key, str):
        pa_table = _query_table(pa_table, key)
        return _query_table(pa_table, (i.as_py() for i in indices))
    if isinstance(key, Iterable):
        return _query_table(pa_table, (indices[i].as_py() for i in key))

    _raise_bad_key_type(key)


def _query_table(pa_table: pa.Table, key: Union[int, slice, range, str, Iterable]) -> pa.Table:
    if isinstance(key, int):
        return pa_table.slice(key % pa_table.num_rows, 1)
    if isinstance(key, slice):
        key = range(*key.indices(pa_table.num_rows))
    if isinstance(key, range):
        if _is_range_contiguous(key):
            return pa_table.slice(key.start, key.stop - key.start)
        else:
            pass  # treat as an iterable
    if isinstance(key, str):
        return pa_table.drop(column for column in pa_table.column_names if column != key)
    if isinstance(key, Iterable):
        # don't use pyarrow.Table.take even for pyarrow >=1.0 (see https://issues.apache.org/jira/browse/ARROW-9773)
        return pa.concat_tables(pa_table.slice(int(i) % pa_table.num_rows, 1) for i in key)

    _raise_bad_key_type(key)


class BaseArrowExtractor(Generic[RowFormat, ColumnFormat, BatchFormat]):
    def extract_row(self, pa_table: pa.Table) -> RowFormat:
        raise NotImplementedError

    def extract_column(self, pa_table: pa.Table) -> ColumnFormat:
        raise NotImplementedError

    def extract_batch(self, pa_table: pa.Table) -> BatchFormat:
        raise NotImplementedError


def _unnest(py_dict: Dict[str, List[T]]) -> Dict[str, T]:
    return dict((key, array[0]) for key, array in py_dict.items())


class PythonArrowExtractor(BaseArrowExtractor[dict, list, dict]):
    def extract_row(self, pa_table: pa.Table) -> dict:
        return _unnest(pa_table.to_pydict())

    def extract_column(self, pa_table: pa.Table) -> list:
        return pa_table.column(0).to_pylist()

    def extract_batch(self, pa_table: pa.Table) -> dict:
        return pa_table.to_pydict()


class NumpyArrowExtractor(BaseArrowExtractor[dict, np.ndarray, dict]):
    def __init__(self, **np_array_kwargs):
        self.np_array_kwargs = np_array_kwargs

    def extract_row(self, pa_table: pa.Table) -> dict:
        return _unnest(pa_table.to_pandas(types_mapper=pandas_types_mapper).to_dict("list"))

    def extract_column(self, pa_table: pa.Table) -> np.ndarray:
        col = pa_table.to_pandas(types_mapper=pandas_types_mapper)[pa_table.column_names[0]].to_list()
        return np.array(col, copy=False, **self.np_array_kwargs)

    def extract_batch(self, pa_table: pa.Table) -> dict:
        batch = pa_table.to_pandas(types_mapper=pandas_types_mapper).to_dict("list")
        return {k: np.array(v, copy=False, **self.np_array_kwargs) for k, v in batch.items()}


class PandasArrowExtractor(BaseArrowExtractor[pd.DataFrame, pd.Series, pd.DataFrame]):
    def extract_row(self, pa_table: pa.Table) -> pd.DataFrame:
        return pa_table.to_pandas(types_mapper=pandas_types_mapper)

    def extract_column(self, pa_table: pa.Table) -> pd.Series:
        return pa_table.to_pandas(types_mapper=pandas_types_mapper)[pa_table.column_names[0]]

    def extract_batch(self, pa_table: pa.Table) -> pd.DataFrame:
        return pa_table.to_pandas(types_mapper=pandas_types_mapper)


class Formatter(Generic[RowFormat, ColumnFormat, BatchFormat]):
    python_arrow_extractor = PythonArrowExtractor
    numpy_arrow_extractor = NumpyArrowExtractor
    pandas_arrow_extractor = PandasArrowExtractor

    def __call__(self, pa_table: pa.Table, query_type: str) -> Union[RowFormat, ColumnFormat, BatchFormat]:
        if query_type == "row":
            return self.format_row(pa_table)
        elif query_type == "column":
            return self.format_column(pa_table)
        elif query_type == "batch":
            return self.format_batch(pa_table)

    def format_row(self, pa_table: pa.Table) -> RowFormat:
        raise NotImplementedError

    def format_column(self, pa_table: pa.Table) -> ColumnFormat:
        raise NotImplementedError

    def format_batch(self, pa_table: pa.Table) -> BatchFormat:
        raise NotImplementedError


class PythonFormatter(Formatter[dict, list, dict]):
    def format_row(self, pa_table: pa.Table) -> dict:
        return self.python_arrow_extractor().extract_row(pa_table)

    def format_column(self, pa_table: pa.Table) -> list:
        return self.python_arrow_extractor().extract_column(pa_table)

    def format_batch(self, pa_table: pa.Table) -> dict:
        return self.python_arrow_extractor().extract_batch(pa_table)


class NumpyFormatter(Formatter[dict, np.ndarray, dict]):
    def __init__(self, **np_array_kwargs):
        self.np_array_kwargs = np_array_kwargs

    def format_row(self, pa_table: pa.Table) -> dict:
        return self.numpy_arrow_extractor(**self.np_array_kwargs).extract_row(pa_table)

    def format_column(self, pa_table: pa.Table) -> np.ndarray:
        return self.numpy_arrow_extractor(**self.np_array_kwargs).extract_column(pa_table)

    def format_batch(self, pa_table: pa.Table) -> dict:
        return self.numpy_arrow_extractor(**self.np_array_kwargs).extract_batch(pa_table)


class PandasFormatter(Formatter):
    def format_row(self, pa_table: pa.Table) -> pd.DataFrame:
        return self.pandas_arrow_extractor().extract_row(pa_table)

    def format_column(self, pa_table: pa.Table) -> pd.Series:
        return self.pandas_arrow_extractor().extract_column(pa_table)

    def format_batch(self, pa_table: pa.Table) -> pd.DataFrame:
        return self.pandas_arrow_extractor().extract_batch(pa_table)


class CustomFormatter(Formatter[dict, ColumnFormat, dict]):
    def __init__(self, transform: Callable[[dict], dict]):
        self.transform = transform

    def format_row(self, pa_table: pa.Table) -> dict:
        formatted_batch = self.format_batch(pa_table)
        if not isinstance(formatted_batch, dict):
            raise TypeError(
                f"Custom formatting function must return a dict to be able to pick a row, but got {formatted_batch}"
            )
        return _unnest(formatted_batch)

    def format_column(self, pa_table: pa.Table) -> ColumnFormat:
        formatted_batch = self.format_batch(pa_table)
        if not isinstance(formatted_batch, dict):
            raise TypeError(
                f"Custom formatting function must return a dict to be able to pick a column, but got {formatted_batch}"
            )
        return formatted_batch[pa_table.column_names[0]]

    def format_batch(self, pa_table: pa.Table) -> dict:
        batch = self.python_arrow_extractor().extract_batch(pa_table)
        return self.transform(batch)


def _check_valid_column_key(key: str, columns: List[str]) -> None:
    if key not in columns:
        raise ValueError("Column {} not in the dataset. Current columns in the dataset: {}".format(key, columns))


def _check_valid_index_key(key: Union[int, slice, range, Iterable], size: int) -> None:
    if isinstance(key, int):
        if (key < 0 and key + size < 0) or (key >= size):
            raise ValueError(f"Invalid key: {key} is out of bounds for size {size}")
        return
    if isinstance(key, slice):
        key = range(*key.indices(size))
    if isinstance(key, range):
        _check_valid_index_key(key.start, size=size)
    elif isinstance(key, Iterable):
        _check_valid_index_key(int(max(key)), size=size)
        _check_valid_index_key(int(min(key)), size=size)
    else:
        _raise_bad_key_type(key)


def key_to_query_type(key: Union[int, slice, range, str, Iterable]) -> str:
    if isinstance(key, int):
        return "row"
    elif isinstance(key, str):
        return "column"
    elif isinstance(key, (slice, range, Iterable)):
        return "batch"
    _raise_bad_key_type(key)


def query_table(
    pa_table: pa.Table, key: Union[int, slice, range, str, Iterable], indices: Optional[pa.lib.UInt64Array] = None
) -> pa.Table:
    # Check if key is valid
    if not isinstance(key, (int, slice, range, str, Iterable)):
        _raise_bad_key_type(key)
    if isinstance(key, str):
        _check_valid_column_key(key, pa_table.column_names)
    else:
        size = len(indices) if indices is not None else pa_table.num_rows
        _check_valid_index_key(key, size)
    # Query the main table
    if indices is None:
        pa_subtable = _query_table(pa_table, key)
    else:
        pa_subtable = _query_table_with_indices_mapping(pa_table, key, indices=indices)
    return pa_subtable


def format_table(
    pa_table: pa.Table,
    key: Union[int, slice, range, str, Iterable],
    formatter: Formatter,
    format_columns: Optional[list] = None,
    output_all_columns=False,
):
    query_type = key_to_query_type(key)
    python_formatter = PythonFormatter()
    if format_columns is None:
        return formatter(pa_table, query_type=query_type)
    elif query_type == "column":
        if key in format_columns:
            return formatter(pa_table, query_type)
        else:
            return python_formatter(pa_table, query_type=query_type)
    else:
        pa_table_to_format = pa_table.drop(col for col in pa_table.column_names if col not in format_columns)
        formatted_output = formatter(pa_table_to_format, query_type=query_type)
        if isinstance(formatted_output, dict) and output_all_columns:
            pa_table_with_remaining_columns = pa_table.drop(
                col for col in pa_table.column_names if col in format_columns
            )
            remaining_columns_dict = python_formatter(pa_table_with_remaining_columns, query_type=query_type)
            formatted_output.update(remaining_columns_dict)
        return formatted_output
