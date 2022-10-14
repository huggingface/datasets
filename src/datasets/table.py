import copy
import os
import tempfile
import warnings
from functools import partial
from itertools import groupby
from typing import TYPE_CHECKING, Callable, List, Optional, Tuple, TypeVar, Union

import numpy as np
import pyarrow as pa

from . import config
from .utils.logging import get_logger


if TYPE_CHECKING:
    from .features.features import Features, FeatureType


logger = get_logger(__name__)


def inject_arrow_table_documentation(arrow_table_method):
    def wrapper(fn):
        fn.__doc__ = arrow_table_method.__doc__ + (fn.__doc__ if fn.__doc__ is not None else "")
        fn.__doc__ = fn.__doc__.replace("pyarrow.Table", "Table")
        if hasattr(arrow_table_method, "__annotations__"):
            fn.__annotations__ = arrow_table_method.__annotations__
        return fn

    return wrapper


def _in_memory_arrow_table_from_file(filename: str) -> pa.Table:
    in_memory_stream = pa.input_stream(filename)
    opened_stream = pa.ipc.open_stream(in_memory_stream)
    pa_table = opened_stream.read_all()
    return pa_table


def _in_memory_arrow_table_from_buffer(buffer: pa.Buffer) -> pa.Table:
    stream = pa.BufferReader(buffer)
    opened_stream = pa.ipc.open_stream(stream)
    table = opened_stream.read_all()
    return table


def _memory_mapped_arrow_table_from_file(filename: str) -> pa.Table:
    memory_mapped_stream = pa.memory_map(filename)
    opened_stream = pa.ipc.open_stream(memory_mapped_stream)
    pa_table = opened_stream.read_all()
    return pa_table


def _write_table_to_file(table: pa.Table, filename: str) -> int:
    with open(filename, "wb") as sink:
        writer = pa.RecordBatchStreamWriter(sink=sink, schema=table.schema)
        batches: List[pa.RecordBatch] = table.to_batches()
        for batch in batches:
            writer.write_batch(batch)
        writer.close()
        return sum(batch.nbytes for batch in batches)


def _deepcopy(x, memo: dict):
    """deepcopy a regular class instance"""
    cls = x.__class__
    result = cls.__new__(cls)
    memo[id(x)] = result
    for k, v in x.__dict__.items():
        setattr(result, k, copy.deepcopy(v, memo))
    return result


def _interpolation_search(arr: List[int], x: int) -> int:
    """
    Return the position i of a sorted array so that arr[i] <= x < arr[i+1]

    Args:
        arr (:obj:`List[int]`): non-empty sorted list of integers
        x (:obj:`int`): query

    Returns:
        `int`: the position i so that arr[i] <= x < arr[i+1]

    Raises:
        `IndexError`: if the array is empty or if the query is outside the array values
    """
    i, j = 0, len(arr) - 1
    while i < j and arr[i] <= x < arr[j]:
        k = i + ((j - i) * (x - arr[i]) // (arr[j] - arr[i]))
        if arr[k] <= x < arr[k + 1]:
            return k
        elif arr[k] < x:
            i, j = k + 1, j
        else:
            i, j = i, k
    raise IndexError(f"Invalid query '{x}' for size {arr[-1] if len(arr) else 'none'}.")


class IndexedTableMixin:
    def __init__(self, table: pa.Table):
        self._schema = table.schema
        self._batches = [recordbatch for recordbatch in table.to_batches() if len(recordbatch) > 0]
        self._offsets: np.ndarray = np.cumsum([0] + [len(b) for b in self._batches], dtype=np.int64)

    def fast_gather(self, indices: Union[List[int], np.ndarray]) -> pa.Table:
        """
        Create a pa.Table by gathering the records at the records at the specified indices. Should be faster
        than pa.concat_tables(table.fast_slice(int(i) % table.num_rows, 1) for i in indices) since NumPy can compute
        the binary searches in parallel, highly optimized C
        """
        if not len(indices):
            raise ValueError("Indices must be non-empty")
        batch_indices = np.searchsorted(self._offsets, indices, side="right") - 1
        return pa.Table.from_batches(
            [
                self._batches[batch_idx].slice(i - self._offsets[batch_idx], 1)
                for batch_idx, i in zip(batch_indices, indices)
            ],
            schema=self._schema,
        )

    def fast_slice(self, offset=0, length=None) -> pa.Table:
        """
        Slice the Table using interpolation search.
        The behavior is the same as :obj:`pyarrow.Table.slice` but it's significantly faster.

        Interpolation search is used to find the start and end indexes of the batches we want to keep.
        The batches to keep are then concatenated to form the sliced Table.
        """
        if offset < 0:
            raise IndexError("Offset must be non-negative")
        elif offset >= self._offsets[-1] or (length is not None and length <= 0):
            return pa.Table.from_batches([], schema=self._schema)
        i = _interpolation_search(self._offsets, offset)
        if length is None or length + offset >= self._offsets[-1]:
            batches = self._batches[i:]
            batches[0] = batches[0].slice(offset - self._offsets[i])
        else:
            j = _interpolation_search(self._offsets, offset + length - 1)
            batches = self._batches[i : j + 1]
            batches[-1] = batches[-1].slice(0, offset + length - self._offsets[j])
            batches[0] = batches[0].slice(offset - self._offsets[i])
        return pa.Table.from_batches(batches, schema=self._schema)


class Table(IndexedTableMixin):
    """
    Wraps a pyarrow Table by using composition.
    This is the base class for InMemoryTable, MemoryMappedTable and ConcatenationTable.

    It implements all the basic attributes/methods of the pyarrow Table class except
    the Table transforms: slice, filter, flatten, combine_chunks, cast, add_column,
    append_column, remove_column, set_column, rename_columns and drop.

    The implementation of these methods differs for the subclasses.
    """

    def __init__(self, table: pa.Table):
        super().__init__(table)
        self.table = table

    def __deepcopy__(self, memo: dict):
        # arrow tables are immutable, so there's no need to copy self.table
        # moreover calling deepcopy on a pyarrow table seems to make pa.total_allocated_bytes() decrease for some reason
        # by adding it to the memo, self.table won't be copied
        memo[id(self.table)] = self.table
        # same for the recordbatches used by the index
        memo[id(self._batches)] = list(self._batches)
        return _deepcopy(self, memo)

    def __getstate__(self):
        # We can't pickle objects that are bigger than 4GiB, or it causes OverflowError
        # So we write the table on disk instead
        if self.table.nbytes >= config.MAX_TABLE_NBYTES_FOR_PICKLING:
            table = self.table
            with tempfile.NamedTemporaryFile("wb", delete=False, suffix=".arrow") as tmp_file:
                filename = tmp_file.name
                logger.debug(
                    f"Attempting to pickle a table bigger than 4GiB. Writing it on the disk instead at {filename}"
                )
                _write_table_to_file(table=table, filename=filename)
                return {"path": filename}
        else:
            return {"table": self.table}

    def __setstate__(self, state):
        if "path" in state:
            filename = state["path"]
            logger.debug(f"Unpickling a big table from the disk at {filename}")
            table = _in_memory_arrow_table_from_file(filename)
            logger.debug(f"Removing temporary table file at {filename}")
            os.remove(filename)
        else:
            table = state["table"]
        Table.__init__(self, table)

    def validate(self, *args, **kwargs):
        """
        Perform validation checks.  An exception is raised if validation fails.

        By default only cheap validation checks are run.  Pass `full=True`
        for thorough validation checks (potentially O(n)).

        Args:
            full (:obj:`bool`, defaults to :obj:`False`):
                If True, run expensive checks, otherwise cheap checks only.

        Raises:
            pa.lib.ArrowInvalid: if validation fails
        """
        return self.table.validate(*args, **kwargs)

    def equals(self, *args, **kwargs):
        """
        Check if contents of two tables are equal.

        Args:
            other (:class:`datasets.table.Table`):
                Table to compare against.
            check_metadata (:obj:`bool`, defaults to :obj:`False`):
                Whether schema metadata equality should be checked as well.

        Returns:
            :obj:`bool`
        """
        args = tuple(arg.table if isinstance(arg, Table) else arg for arg in args)
        kwargs = {k: v.table if isinstance(v, Table) else v for k, v in kwargs}
        return self.table.equals(*args, **kwargs)

    def to_batches(self, *args, **kwargs):
        """
        Convert Table to list of (contiguous) RecordBatch objects.

        Args:
            max_chunksize (:obj:`int`, defaults to `None`):
                Maximum size for RecordBatch chunks. Individual chunks may be
                smaller depending on the chunk layout of individual columns.

        Returns:
            :obj:`List[pyarrow.RecordBatch]`:
        """
        return self.table.to_batches(*args, **kwargs)

    def to_pydict(self, *args, **kwargs):
        """
        Convert the Table to a dict or OrderedDict.

        Returns:
            :obj:`dict`
        """
        return self.table.to_pydict(*args, **kwargs)

    def to_pylist(self, *args, **kwargs):
        """
        Convert the Table to a list

        Returns:
            :obj:`list`
        """
        try:
            return self.table.to_pylist(*args, **kwargs)
        except AttributeError:  # pyarrow <7 does not have to_pylist, so we use to_pydict
            pydict = self.table.to_pydict(*args, **kwargs)
            return [{k: pydict[k][i] for k in pydict} for i in range(len(self.table))]

    def to_pandas(self, *args, **kwargs):
        """
        Convert to a pandas-compatible NumPy array or DataFrame, as appropriate

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                Arrow MemoryPool to use for allocations. Uses the default memory
                pool is not passed.
            strings_to_categorical (:obj:`bool`, defaults to :obj:`False`):
                Encode string (UTF8) and binary types to pandas.Categorical.
            categories (:obj:`list`, defaults to :obj:`empty`):
                List of fields that should be returned as pandas.Categorical. Only
                applies to table-like data structures.
            zero_copy_only (:obj:`bool`, defaults to :obj:`False`):
                Raise an ArrowException if this function call would require copying
                the underlying data.
            integer_object_nulls (:obj:`bool`, defaults to :obj:`False`):
                Cast integers with nulls to objects
            date_as_object (:obj:`bool`, defaults to :obj:`True`):
                Cast dates to objects. If False, convert to datetime64[ns] dtype.
            timestamp_as_object (:obj:`bool`, defaults to :obj:`False`):
                Cast non-nanosecond timestamps (np.datetime64) to objects. This is
                useful if you have timestamps that don't fit in the normal date
                range of nanosecond timestamps (1678 CE-2262 CE).
                If False, all timestamps are converted to datetime64[ns] dtype.
            use_threads (:obj:`bool`, defaults to :obj:`True`):
                Whether to parallelize the conversion using multiple threads.
            deduplicate_objects (:obj:`bool`, defaults to :obj:`False`):
                Do not create multiple copies Python objects when created, to save
                on memory use. Conversion will be slower.
            ignore_metadata (:obj:`bool`, defaults to :obj:`False`):
                If True, do not use the 'pandas' metadata to reconstruct the
                DataFrame index, if present
            safe (:obj:`bool`, defaults to :obj:`True`):
                For certain data types, a cast is needed in order to store the
                data in a pandas DataFrame or Series (e.g. timestamps are always
                stored as nanoseconds in pandas). This option controls whether it
                is a safe cast or not.
            split_blocks (:obj:`bool`, defaults to :obj:`False`):
                If True, generate one internal "block" for each column when
                creating a pandas.DataFrame from a RecordBatch or Table. While this
                can temporarily reduce memory note that various pandas operations
                can trigger "consolidation" which may balloon memory use.
            self_destruct (:obj:`bool`, defaults to :obj:`False`):
                EXPERIMENTAL: If True, attempt to deallocate the originating Arrow
                memory while converting the Arrow object to pandas. If you use the
                object after calling to_pandas with this option it will crash your
                program.
            types_mapper (:obj:`function`, defaults to :obj:`None`):
                A function mapping a pyarrow DataType to a pandas ExtensionDtype.
                This can be used to override the default pandas type for conversion
                of built-in pyarrow types or in absence of pandas_metadata in the
                Table schema. The function receives a pyarrow DataType and is
                expected to return a pandas ExtensionDtype or ``None`` if the
                default conversion should be used for that type. If you have
                a dictionary mapping, you can pass ``dict.get`` as function.

        Returns:
            :obj:`pandas.Series` or :obj:`pandas.DataFrame`: :obj:`pandas.Series` or :obj:`pandas.DataFrame` depending on type of object
        """
        return self.table.to_pandas(*args, **kwargs)

    def to_string(self, *args, **kwargs):
        return self.table.to_string(*args, **kwargs)

    def to_reader(self, *args, **kwargs):
        """
        Convert the Table to a RecordBatchReader.

        Note that this method is zero-copy, it merely exposes the same data under a different API.

        Args:
            max_chunksize (:obj:`int`, defaults to :obj:`None`)
                Maximum size for RecordBatch chunks. Individual chunks may be smaller depending
                on the chunk layout of individual columns.

        Returns:
            :obj:`pyarrow.RecordBatchReader`

        <Tip warning={true}>

        pyarrow >= 8.0.0 needs to be installed to use this method.

        </Tip>
        """
        if config.PYARROW_VERSION.major < 8:
            raise NotImplementedError("`pyarrow>=8.0.0` is required to use this method")
        return self.table.to_reader(*args, **kwargs)

    def field(self, *args, **kwargs):
        """
        Select a schema field by its column name or numeric index.

        Args:
            i (:obj:`Union[int, str]`):
                The index or name of the field to retrieve.

        Returns:
            :obj:`pyarrow.Field`:
        """
        return self.table.field(*args, **kwargs)

    def column(self, *args, **kwargs):
        """
        Select a column by its column name, or numeric index.

        Args:
            i (:obj:`Union[int, str]`):
                The index or name of the column to retrieve.

        Returns:
            :obj:`pyarrow.ChunkedArray`:
        """
        return self.table.column(*args, **kwargs)

    def itercolumns(self, *args, **kwargs):
        """
        Iterator over all columns in their numerical order.

        Yields:
            :obj:`pyarrow.ChunkedArray`:
        """
        return self.table.itercolumns(*args, **kwargs)

    @property
    def schema(self):
        """
        Schema of the table and its columns.

        Returns:
            :obj:`pyarrow.Schema`:
        """
        return self.table.schema

    @property
    def columns(self):
        """
        List of all columns in numerical order.

        Returns:
            :obj:`List[pa.ChunkedArray]`:
        """
        return self.table.columns

    @property
    def num_columns(self):
        """
        Number of columns in this table.

        Returns:
            int:
        """
        return self.table.num_columns

    @property
    def num_rows(self):
        """
        Number of rows in this table.

        Due to the definition of a table, all columns have the same number of
        rows.

        Returns:
            int:
        """
        return self.table.num_rows

    @property
    def shape(self):
        """
        Dimensions of the table: (#rows, #columns).

        Returns:
            :obj:`(int, int)`: Number of rows and number of columns.
        """
        return self.table.shape

    @property
    def nbytes(self):
        """
        Total number of bytes consumed by the elements of the table.
        """
        return self.table.nbytes

    @property
    def column_names(self):
        """
        Names of the table's columns
        """
        return self.table.column_names

    def __eq__(self, other):
        return self.equals(other)

    def __getitem__(self, i):
        return self.table[i]

    def __len__(self):
        return len(self.table)

    def __repr__(self):
        return self.table.__repr__().replace("pyarrow.Table", self.__class__.__name__)

    def __str__(self):
        return self.table.__str__().replace("pyarrow.Table", self.__class__.__name__)

    def slice(self, *args, **kwargs):
        """
        Compute zero-copy slice of this Table

        Args:
            offset (:obj:`int`, defaults to :obj:`0`):
                Offset from start of table to slice
            length (:obj:`int`, defaults to :obj:`None`):
                Length of slice (default is until end of table starting from
                offset)

        Returns:
            :class:`datasets.table.Table`:
        """
        raise NotImplementedError()

    def filter(self, *args, **kwargs):
        """
        Select records from a Table. See pyarrow.compute.filter for full usage.
        """
        raise NotImplementedError()

    def flatten(self, *args, **kwargs):
        """
        Flatten this Table.  Each column with a struct type is flattened
        into one column per struct field.  Other columns are left unchanged.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        raise NotImplementedError()

    def combine_chunks(self, *args, **kwargs):
        """
        Make a new table by combining the chunks this table has.

        All the underlying chunks in the ChunkedArray of each column are
        concatenated into zero or one chunk.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        raise NotImplementedError()

    def cast(self, *args, **kwargs):
        """
        Cast table values to another schema

        Args:
            target_schema (:obj:`Schema`):
                Schema to cast to, the names and order of fields must match
            safe (:obj:`bool`, defaults to :obj:`True`):
                Check for overflows or other unsafe conversions

        Returns:
            :class:`datasets.table.Table`:
        """
        raise NotImplementedError()

    def replace_schema_metadata(self, *args, **kwargs):
        """
        EXPERIMENTAL: Create shallow copy of table by replacing schema
        key-value metadata with the indicated new metadata (which may be None,
        which deletes any existing metadata

        Args:
            metadata (:obj:`dict`, defaults to :obj:`None`):

        Returns:
            :class:`datasets.table.Table`: shallow_copy
        """
        raise NotImplementedError()

    def add_column(self, *args, **kwargs):
        """
        Add column to Table at position.

        A new table is returned with the column added, the original table
        object is left unchanged.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`: New table with the passed column added.
        """
        raise NotImplementedError()

    def append_column(self, *args, **kwargs):
        """
        Append column at end of columns.

        Args:
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:  New table with the passed column added.
        """
        raise NotImplementedError()

    def remove_column(self, *args, **kwargs):
        """
        Create new Table with the indicated column removed.

        Args:
            i (:obj:`int`):
                Index of column to remove.

        Returns:
            :class:`datasets.table.Table`: New table without the column.
        """
        raise NotImplementedError()

    def set_column(self, *args, **kwargs):
        """
        Replace column in Table at position.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`: New table with the passed column set.
        """
        raise NotImplementedError()

    def rename_columns(self, *args, **kwargs):
        """
        Create new table with columns renamed to provided names.
        """
        raise NotImplementedError()

    def drop(self, *args, **kwargs):
        """
        Drop one or more columns and return a new table.

        Args:
            columns (:obj:`List[str]`):
                List of field names referencing existing columns.

        Raises:
            KeyError : if any of the passed columns name are not existing.

        Returns:
            :class:`datasets.table.Table`: New table without the columns.
        """
        raise NotImplementedError()

    # Additional methods that are based on the PyArrow Table methods

    def select_columns(self, columns: List[int]) -> "Table":
        """Return the table by keeping only the requested columns

        Returns:
            :class:`datasets.table.Table`: table with only a subset of the columns
        """
        for column_to_remove in set(range(len(self.column_names))) - set(columns):
            self = self.remove_column(column_to_remove)
        return self


class TableBlock(Table):
    """
    TableBlock is the allowed class inside a ConcanetationTable.
    Only MemoryMappedTable and InMemoryTable are TableBlock.
    This is because we don't want a ConcanetationTable made out of other ConcanetationTables.
    """

    pass


class InMemoryTable(TableBlock):
    """
    The table is said in-memory when it is loaded into the user's RAM.

    Pickling it does copy all the data using memory.
    Its implementation is simple and uses the underlying pyarrow Table methods directly.

    This is different from the MemoryMapped table, for which pickling doesn't copy all the
    data in memory. For a MemoryMapped, unpickling instead reloads the table from the disk.

    InMemoryTable must be used when data fit in memory, while MemoryMapped are reserved for
    data bigger than memory or when you want the memory footprint of your application to
    stay low.
    """

    @classmethod
    def from_file(cls, filename: str):
        table = _in_memory_arrow_table_from_file(filename)
        return cls(table)

    @classmethod
    def from_buffer(cls, buffer: pa.Buffer):
        table = _in_memory_arrow_table_from_buffer(buffer)
        return cls(table)

    @classmethod
    def from_pandas(cls, *args, **kwargs):
        """
        Convert pandas.DataFrame to an Arrow Table.

        The column types in the resulting Arrow Table are inferred from the
        dtypes of the pandas.Series in the DataFrame. In the case of non-object
        Series, the NumPy dtype is translated to its Arrow equivalent. In the
        case of `object`, we need to guess the datatype by looking at the
        Python objects in this Series.

        Be aware that Series of the `object` dtype don't carry enough
        information to always lead to a meaningful Arrow type. In the case that
        we cannot infer a type, e.g. because the DataFrame is of length 0 or
        the Series only contains None/nan objects, the type is set to
        null. This behavior can be avoided by constructing an explicit schema
        and passing it to this function.

        Args:
            df (:obj:`pandas.DataFrame`):
            schema (:obj:`pyarrow.Schema`, optional):
                The expected schema of the Arrow Table. This can be used to
                indicate the type of columns if we cannot infer it automatically.
                If passed, the output will have exactly this schema. Columns
                specified in the schema that are not found in the DataFrame columns
                or its index will raise an error. Additional columns or index
                levels in the DataFrame which are not specified in the schema will
                be ignored.
            preserve_index (:obj:`bool`, optional):
                Whether to store the index as an additional column in the resulting
                ``Table``. The default of None will store the index as a column,
                except for RangeIndex which is stored as metadata only. Use
                ``preserve_index=True`` to force it to be stored as a column.
            nthreads (:obj:`int`, defaults to :obj:`None` (may use up to system CPU count threads))
                If greater than 1, convert columns to Arrow in parallel using
                indicated number of threads
            columns (:obj:`List[str]`, optional):
               List of column to be converted. If None, use all columns.
            safe (:obj:`bool`, defaults to :obj:`True`):
               Check for overflows or other unsafe conversions

        Returns:
            :class:`datasets.table.Table`:

        Examples:
        ```python
        >>> import pandas as pd
        >>> import pyarrow as pa
        >>> df = pd.DataFrame({
            ...     'int': [1, 2],
            ...     'str': ['a', 'b']
            ... })
        >>> pa.Table.from_pandas(df)
        <pyarrow.lib.Table object at 0x7f05d1fb1b40>
        ```
        """
        return cls(pa.Table.from_pandas(*args, **kwargs))

    @classmethod
    def from_arrays(cls, *args, **kwargs):
        """
        Construct a Table from Arrow arrays

        Args:
            arrays (:obj:`List[Union[pyarrow.Array, pyarrow.ChunkedArray]]`):
                Equal-length arrays that should form the table.
            names (:obj:`List[str]`, optional):
                Names for the table columns. If not passed, schema must be passed
            schema (:obj:`Schema`, defaults to :obj:`None`):
                Schema for the created table. If not passed, names must be passed
            metadata (:obj:`Union[dict, Mapping]`, default None):
                Optional metadata for the schema (if inferred).

        Returns:
            :class:`datasets.table.Table`:
        """
        return cls(pa.Table.from_arrays(*args, **kwargs))

    @classmethod
    def from_pydict(cls, *args, **kwargs):
        """
        Construct a Table from Arrow arrays or columns

        Args:
            mapping (:obj:`Union[dict, Mapping]`):
                A mapping of strings to Arrays or Python lists.
            schema (:obj:`Schema`, defaults to :obj:`None`):
                If not passed, will be inferred from the Mapping values
            metadata (:obj:`Union[dict, Mapping]`, default None):
                Optional metadata for the schema (if inferred).

        Returns:
            :class:`datasets.table.Table`:
        """
        return cls(pa.Table.from_pydict(*args, **kwargs))

    @classmethod
    def from_pylist(cls, mapping, *args, **kwargs):
        """
        Construct a Table from list of rows / dictionaries.

        Args:
            mapping (:obj:`List[dict]`):
                A mapping of strings to row values.
            schema (:obj:`Schema`, defaults to :obj:`None`):
                If not passed, will be inferred from the Mapping values
            metadata (:obj:`Union[dict, Mapping]`, default None):
                Optional metadata for the schema (if inferred).

        Returns:
            :class:`datasets.table.Table`:
        """
        try:
            return cls(pa.Table.from_pylist(mapping, *args, **kwargs))
        except AttributeError:  # pyarrow <7 does not have from_pylist, so we convert and use from_pydict
            mapping = {k: [r.get(k) for r in mapping] for k in mapping[0]} if mapping else {}
            return cls(pa.Table.from_pydict(mapping, *args, **kwargs))

    @classmethod
    def from_batches(cls, *args, **kwargs):
        """
        Construct a Table from a sequence or iterator of Arrow RecordBatches.

        Args:
            batches (:obj:`Union[Sequence[pyarrow.RecordBatch], Iterator[pyarrow.RecordBatch]]`):
                Sequence of RecordBatch to be converted, all schemas must be equal.
            schema (:obj:`Schema`, defaults to :obj:`None`):
                If not passed, will be inferred from the first RecordBatch.

        Returns:
            :class:`datasets.table.Table`:
        """
        return cls(pa.Table.from_batches(*args, **kwargs))

    def slice(self, offset=0, length=None):
        """
        Compute zero-copy slice of this Table

        Args:
            offset (:obj:`int`, defaults to :obj:`0`):
                Offset from start of table to slice
            length (:obj:`int`, defaults to :obj:`None`):
                Length of slice (default is until end of table starting from
                offset)

        Returns:
            :class:`datasets.table.Table`:
        """
        # Use fast slicing here
        return InMemoryTable(self.fast_slice(offset=offset, length=length))

    def filter(self, *args, **kwargs):
        """
        Select records from a Table. See pyarrow.compute.filter for full usage.
        """
        return InMemoryTable(self.table.filter(*args, **kwargs))

    def flatten(self, *args, **kwargs):
        """
        Flatten this Table.  Each column with a struct type is flattened
        into one column per struct field.  Other columns are left unchanged.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        return InMemoryTable(table_flatten(self.table, *args, **kwargs))

    def combine_chunks(self, *args, **kwargs):
        """
        Make a new table by combining the chunks this table has.

        All the underlying chunks in the ChunkedArray of each column are
        concatenated into zero or one chunk.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        return InMemoryTable(self.table.combine_chunks(*args, **kwargs))

    def cast(self, *args, **kwargs):
        """
        Cast table values to another schema

        Args:
            target_schema (:obj:`Schema`):
                Schema to cast to, the names and order of fields must match
            safe (:obj:`bool`, defaults to :obj:`True`):
                Check for overflows or other unsafe conversions

        Returns:
            :class:`datasets.table.Table`:
        """
        return InMemoryTable(table_cast(self.table, *args, **kwargs))

    def replace_schema_metadata(self, *args, **kwargs):
        """
        EXPERIMENTAL: Create shallow copy of table by replacing schema
        key-value metadata with the indicated new metadata (which may be None,
        which deletes any existing metadata

        Args:
            metadata (:obj:`dict`, defaults to :obj:`None`):

        Returns:
            :class:`datasets.table.Table`: shallow_copy
        """
        return InMemoryTable(self.table.replace_schema_metadata(*args, **kwargs))

    def add_column(self, *args, **kwargs):
        """
        Add column to Table at position.

        A new table is returned with the column added, the original table
        object is left unchanged.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`: New table with the passed column added.
        """
        return InMemoryTable(self.table.add_column(*args, **kwargs))

    def append_column(self, *args, **kwargs):
        """
        Append column at end of columns.

        Args:
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column added.
        """
        return InMemoryTable(self.table.append_column(*args, **kwargs))

    def remove_column(self, *args, **kwargs):
        """
        Create new Table with the indicated column removed.

        Args:
            i (:obj:`int`):
                Index of column to remove.

        Returns:
            :class:`datasets.table.Table`:
                New table without the column.
        """
        return InMemoryTable(self.table.remove_column(*args, **kwargs))

    def set_column(self, *args, **kwargs):
        """
        Replace column in Table at position.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column set.
        """
        return InMemoryTable(self.table.set_column(*args, **kwargs))

    def rename_columns(self, *args, **kwargs):
        """
        Create new table with columns renamed to provided names.
        """
        return InMemoryTable(self.table.rename_columns(*args, **kwargs))

    def drop(self, *args, **kwargs):
        """
        Drop one or more columns and return a new table.

        Args:
            columns (:obj:`List[str]`):
                List of field names referencing existing columns.

        Raises:
            KeyError : if any of the passed columns name are not existing.

        Returns:
            :class:`datasets.table.Table`:
                New table without the columns.
        """
        return InMemoryTable(self.table.drop(*args, **kwargs))


# The MemoryMappedTable needs replays to properly reload tables from the disk
Replay = Tuple[str, tuple, dict]


class MemoryMappedTable(TableBlock):
    """
    The table is said memory mapped when it doesn't use the user's RAM but loads the data
    from the disk instead.

    Pickling it doesn't copy the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replay" when reloading the table from the disk.

    Its implementation requires to store an history of all the transforms that were applied
    to the underlying pyarrow Table, so that they can be "replayed" when reloading the Table
    from the disk.

    This is different from the InMemoryTable table, for which pickling does copy all the
    data in memory.

    InMemoryTable must be used when data fit in memory, while MemoryMapped are reserved for
    data bigger than memory or when you want the memory footprint of your application to
    stay low.
    """

    def __init__(self, table: pa.Table, path: str, replays: Optional[List[Replay]] = None):
        super().__init__(table)
        self.path = path
        self.replays: List[Replay] = replays if replays is not None else []

    @classmethod
    def from_file(cls, filename: str, replays=None):
        table = _memory_mapped_arrow_table_from_file(filename)
        table = cls._apply_replays(table, replays)
        return cls(table, filename, replays)

    def __getstate__(self):
        return {"path": self.path, "replays": self.replays}

    def __setstate__(self, state):
        path = state["path"]
        replays = state["replays"]
        table = _memory_mapped_arrow_table_from_file(path)
        table = self._apply_replays(table, replays)
        MemoryMappedTable.__init__(self, table, path=path, replays=replays)

    @staticmethod
    def _apply_replays(table: pa.Table, replays: Optional[List[Replay]] = None) -> pa.Table:
        if replays is not None:
            for name, args, kwargs in replays:
                if name == "cast":
                    table = table_cast(table, *args, **kwargs)
                elif name == "flatten":
                    table = table_flatten(table, *args, **kwargs)
                else:
                    table = getattr(table, name)(*args, **kwargs)
        return table

    def _append_replay(self, replay: Replay) -> List[Replay]:
        replays = copy.deepcopy(self.replays)
        replays.append(replay)
        return replays

    def slice(self, offset=0, length=None):
        """
        Compute zero-copy slice of this Table

        Args:
            offset (:obj:`int`, defaults to :obj:`0`):
                Offset from start of table to slice
            length (:obj:`int`, defaults to :obj:`None`):
                Length of slice (default is until end of table starting from
                offset)

        Returns:
            :class:`datasets.table.Table`:
        """
        replay = ("slice", (offset, length), {})
        replays = self._append_replay(replay)
        # Use fast slicing here
        return MemoryMappedTable(self.fast_slice(offset=offset, length=length), self.path, replays)

    def filter(self, *args, **kwargs):
        """
        Select records from a Table. See pyarrow.compute.filter for full usage.
        """
        replay = ("filter", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.filter(*args, **kwargs), self.path, replays)

    def flatten(self, *args, **kwargs):
        """
        Flatten this Table.  Each column with a struct type is flattened
        into one column per struct field.  Other columns are left unchanged.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        replay = ("flatten", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(table_flatten(self.table, *args, **kwargs), self.path, replays)

    def combine_chunks(self, *args, **kwargs):
        """
        Make a new table by combining the chunks this table has.

        All the underlying chunks in the ChunkedArray of each column are
        concatenated into zero or one chunk.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        replay = ("combine_chunks", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.combine_chunks(*args, **kwargs), self.path, replays)

    def cast(self, *args, **kwargs):
        """
        Cast table values to another schema

        Args:
            target_schema (:obj:`Schema`):
                Schema to cast to, the names and order of fields must match
            safe (:obj:`bool`, defaults to :obj:`True`):
                Check for overflows or other unsafe conversions

        Returns:
            :class:`datasets.table.Table`:
        """
        replay = ("cast", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(table_cast(self.table, *args, **kwargs), self.path, replays)

    def replace_schema_metadata(self, *args, **kwargs):
        """
        EXPERIMENTAL: Create shallow copy of table by replacing schema
        key-value metadata with the indicated new metadata (which may be None,
        which deletes any existing metadata

        Args:
            metadata (:obj:`dict`, defaults to :obj:`None`):

        Returns:
            :class:`datasets.table.Table`: shallow_copy
        """
        replay = ("replace_schema_metadata", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.replace_schema_metadata(*args, **kwargs), self.path, replays)

    def add_column(self, *args, **kwargs):
        """
        Add column to Table at position.

        A new table is returned with the column added, the original table
        object is left unchanged.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`: New table with the passed column added.
        """
        replay = ("add_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.add_column(*args, **kwargs), self.path, replays)

    def append_column(self, *args, **kwargs):
        """
        Append column at end of columns.

        Args:
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column added.
        """
        replay = ("append_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.append_column(*args, **kwargs), self.path, replays)

    def remove_column(self, *args, **kwargs):
        """
        Create new Table with the indicated column removed.

        Args:
            i (:obj:`int`):
                Index of column to remove.

        Returns:
            :class:`datasets.table.Table`:
                New table without the column.
        """
        replay = ("remove_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.remove_column(*args, **kwargs), self.path, replays)

    def set_column(self, *args, **kwargs):
        """
        Replace column in Table at position.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column set.
        """
        replay = ("set_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.set_column(*args, **kwargs), self.path, replays)

    def rename_columns(self, *args, **kwargs):
        """
        Create new table with columns renamed to provided names.
        """
        replay = ("rename_columns", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.rename_columns(*args, **kwargs), self.path, replays)

    def drop(self, *args, **kwargs):
        """
        Drop one or more columns and return a new table.

        Args:
            columns (:obj:`List[str]`):
                List of field names referencing existing columns.

        Raises:
            KeyError : if any of the passed columns name are not existing.

        Returns:
            :class:`datasets.table.Table`:
                New table without the columns.
        """
        replay = ("drop", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.drop(*args, **kwargs), self.path, replays)


# A ConcatenationTable is the concatenation of several tables.
# The ``blocks`` attributes stores a list of list of blocks.
# The first axis concatenates the tables along the axis 0 (it appends rows),
# while the second axis concatenates tables along the axis 1 (it appends columns).
TableBlockContainer = TypeVar("TableBlockContainer", TableBlock, List[TableBlock], List[List[TableBlock]])


class ConcatenationTable(Table):
    """
    The table comes from the concatenation of several tables called blocks.
    It enables concatenation on both axis 0 (append rows) and axis 1 (append columns).

    The underlying tables are called "blocks" and can be either InMemoryTable
    or MemoryMappedTable objects.
    This allows to combine tables that come from memory or that are memory mapped.
    When a ConcatenationTable is pickled, then each block is pickled:
    - the InMemoryTable objects are pickled by copying all the data in memory;
    - the MemoryMappedTable objects are pickled without copying the data into memory.
    Instead, only the path to the memory mapped arrow file is pickled, as well as the list
    of transforms to "replays" when reloading the table from the disk.

    Its implementation requires to store each block separately.
    The ``blocks`` attributes stores a list of list of blocks.
    The first axis concatenates the tables along the axis 0 (it appends rows),
    while the second axis concatenates tables along the axis 1 (it appends columns).

    If some columns are missing when concatenating on axis 0, they are filled with null values.
    This is done using `pyarrow.concat_tables(tables, promote=True)`.

    You can access the fully combined table by accessing the ConcatenationTable.table attribute,
    and the blocks by accessing the ConcatenationTable.blocks attribute.
    """

    def __init__(self, table: pa.Table, blocks: List[List[TableBlock]]):
        super().__init__(table)
        self.blocks = blocks
        # Check that all the blocks have the right type.
        # Only InMemoryTable and MemoryMappedTable are allowed.
        for subtables in blocks:
            for subtable in subtables:
                if not isinstance(subtable, TableBlock):
                    raise TypeError(
                        "The blocks of a ConcatenationTable must be InMemoryTable or MemoryMappedTable objects"
                        f", but got {subtable}."
                    )

    def __getstate__(self):
        return {"blocks": self.blocks}

    def __setstate__(self, state):
        blocks = state["blocks"]
        table = self._concat_blocks_horizontally_and_vertically(blocks)
        ConcatenationTable.__init__(self, table, blocks=blocks)

    @staticmethod
    def _concat_blocks(blocks: List[Union[TableBlock, pa.Table]], axis: int = 0) -> pa.Table:
        pa_tables = [table.table if hasattr(table, "table") else table for table in blocks]
        if axis == 0:
            # we set promote=True to fill missing columns with null values
            return pa.concat_tables(pa_tables, promote=True)
        elif axis == 1:
            for i, table in enumerate(pa_tables):
                if i == 0:
                    pa_table = table
                else:
                    for name, col in zip(table.column_names, table.columns):
                        pa_table = pa_table.append_column(name, col)
            return pa_table
        else:
            raise ValueError("'axis' must be either 0 or 1")

    @classmethod
    def _concat_blocks_horizontally_and_vertically(cls, blocks: List[List[TableBlock]]) -> pa.Table:
        pa_tables_to_concat_vertically = []
        for i, tables in enumerate(blocks):
            if not tables:
                continue
            pa_table_horizontally_concatenated = cls._concat_blocks(tables, axis=1)
            pa_tables_to_concat_vertically.append(pa_table_horizontally_concatenated)
        return cls._concat_blocks(pa_tables_to_concat_vertically, axis=0)

    @classmethod
    def _merge_blocks(cls, blocks: TableBlockContainer, axis: Optional[int] = None) -> TableBlockContainer:
        if axis is not None:
            merged_blocks = []
            for is_in_memory, block_group in groupby(blocks, key=lambda x: isinstance(x, InMemoryTable)):
                if is_in_memory:
                    block_group = [InMemoryTable(cls._concat_blocks(list(block_group), axis=axis))]
                merged_blocks += list(block_group)
        else:  # both
            merged_blocks = [cls._merge_blocks(row_block, axis=1) for row_block in blocks]
            if all(len(row_block) == 1 for row_block in merged_blocks):
                merged_blocks = cls._merge_blocks(
                    [block for row_block in merged_blocks for block in row_block], axis=0
                )
        return merged_blocks

    @classmethod
    def _consolidate_blocks(cls, blocks: TableBlockContainer) -> TableBlockContainer:
        if isinstance(blocks, TableBlock):
            return blocks
        elif isinstance(blocks[0], TableBlock):
            return cls._merge_blocks(blocks, axis=0)
        else:
            return cls._merge_blocks(blocks)

    @classmethod
    def from_blocks(cls, blocks: TableBlockContainer) -> "ConcatenationTable":
        blocks = cls._consolidate_blocks(blocks)
        if isinstance(blocks, TableBlock):
            table = blocks
            return cls(table.table, [[table]])
        elif isinstance(blocks[0], TableBlock):
            table = cls._concat_blocks(blocks, axis=0)
            blocks = [[t] for t in blocks]
            return cls(table, blocks)
        else:
            table = cls._concat_blocks_horizontally_and_vertically(blocks)
            return cls(table, blocks)

    @classmethod
    def from_tables(cls, tables: List[Union[pa.Table, Table]], axis: int = 0) -> "ConcatenationTable":
        """Create ConcatenationTable from list of tables.

        Args:
            tables (list of :class:`Table` or list of :obj:`pyarrow.Table`): List of tables.
            axis: (``{0, 1}``, defaults to :obj:`0`, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            *New in version 1.6.0*
        """

        def to_blocks(table):
            if isinstance(table, pa.Table):
                return [[InMemoryTable(table)]]
            elif isinstance(table, ConcatenationTable):
                return copy.deepcopy(table.blocks)
            else:
                return [[table]]

        def _split_like(blocks_to_split, blocks_like):
            splits = []
            offset = 0
            for block_row in blocks_like:
                length = block_row[0].num_rows
                splits.append((offset, length))
                offset += length
            return [
                [block.slice(offset=split[0], length=split[1]) for block in blocks_to_split[0]] for split in splits
            ]

        def _extend_blocks(result, blocks: List[List[TableBlock]], axis: int = 0):
            if axis == 0:
                result.extend(blocks)
            elif axis == 1:
                if len(result) == 1 and len(blocks) > 1:
                    result = _split_like(result, blocks)  # Split result
                elif len(blocks) == 1 and len(result) > 1:
                    blocks = _split_like(blocks, result)  # Split blocks
                # TODO: This assumes each block_row has the same num_rows
                for i, row_blocks in enumerate(blocks):
                    result[i].extend(row_blocks)
            return result

        blocks = to_blocks(tables[0])
        for table in tables[1:]:
            table_blocks = to_blocks(table)
            blocks = _extend_blocks(blocks, table_blocks, axis=axis)
        return cls.from_blocks(blocks)

    @property
    def _slices(self):
        offset = 0
        for tables in self.blocks:
            length = len(tables[0])
            yield (offset, length)
            offset += length

    def slice(self, offset=0, length=None):
        """
        Compute zero-copy slice of this Table

        Args:
            offset (:obj:`int`, defaults to :obj:`0`):
                Offset from start of table to slice
            length (:obj:`int`, defaults to :obj:`None`):
                Length of slice (default is until end of table starting from
                offset)

        Returns:
            :class:`datasets.table.Table`:
        """
        table = self.table.slice(offset, length=length)
        length = length if length is not None else self.num_rows - offset
        blocks = []
        for tables in self.blocks:
            n_rows = len(tables[0])
            if length == 0:
                break
            elif n_rows <= offset:
                offset = offset - n_rows
            elif n_rows <= offset + length:
                blocks.append([t.slice(offset) for t in tables])
                length, offset = length + offset - n_rows, 0
            else:
                blocks.append([t.slice(offset, length) for t in tables])
                length, offset = 0, 0
        return ConcatenationTable(table, blocks)

    def filter(self, mask, *args, **kwargs):
        """
        Select records from a Table. See pyarrow.compute.filter for full usage.
        """
        table = self.table.filter(mask, *args, **kwargs)
        blocks = []
        for (offset, length), tables in zip(self._slices, self.blocks):
            submask = mask.slice(offset, length)
            blocks.append([t.filter(submask, *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    def flatten(self, *args, **kwargs):
        """
        Flatten this Table.  Each column with a struct type is flattened
        into one column per struct field.  Other columns are left unchanged.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        table = table_flatten(self.table, *args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.flatten(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    def combine_chunks(self, *args, **kwargs):
        """
        Make a new table by combining the chunks this table has.

        All the underlying chunks in the ChunkedArray of each column are
        concatenated into zero or one chunk.

        Args:
            memory_pool (:obj:`MemoryPool`, defaults to :obj:`None`):
                For memory allocations, if required, otherwise use default pool

        Returns:
            :class:`datasets.table.Table`:
        """
        table = self.table.combine_chunks(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.combine_chunks(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    def cast(self, target_schema, *args, **kwargs):
        """
        Cast table values to another schema

        Args:
            target_schema (:obj:`Schema`):
                Schema to cast to, the names and order of fields must match
            safe (:obj:`bool`, defaults to :obj:`True`):
                Check for overflows or other unsafe conversions

        Returns:
            :class:`datasets.table.Table`:
        """
        from .features import Features

        table = table_cast(self.table, target_schema, *args, **kwargs)
        target_features = Features.from_arrow_schema(target_schema)
        blocks = []
        for subtables in self.blocks:
            new_tables = []
            fields = list(target_schema)
            for subtable in subtables:
                subfields = []
                for name in subtable.column_names:
                    subfields.append(fields.pop(next(i for i, field in enumerate(fields) if field.name == name)))
                subfeatures = Features({subfield.name: target_features[subfield.name] for subfield in subfields})
                subschema = subfeatures.arrow_schema
                new_tables.append(subtable.cast(subschema, *args, **kwargs))
            blocks.append(new_tables)
        return ConcatenationTable(table, blocks)

    def replace_schema_metadata(self, *args, **kwargs):
        """
        EXPERIMENTAL: Create shallow copy of table by replacing schema
        key-value metadata with the indicated new metadata (which may be None,
        which deletes any existing metadata

        Args:
            metadata (:obj:`dict`, defaults to :obj:`None`):

        Returns:
            :class:`datasets.table.Table`: shallow_copy
        """
        table = self.table.replace_schema_metadata(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.replace_schema_metadata(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, self.blocks)

    def add_column(self, *args, **kwargs):
        """
        Add column to Table at position.

        A new table is returned with the column added, the original table
        object is left unchanged.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`: New table with the passed column added.
        """
        raise NotImplementedError()

    def append_column(self, *args, **kwargs):
        """
        Append column at end of columns.

        Args:
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column added.
        """
        raise NotImplementedError()

    def remove_column(self, i, *args, **kwargs):
        """
        Create new Table with the indicated column removed.

        Args:
            i (:obj:`int`):
                Index of column to remove.

        Returns:
            :class:`datasets.table.Table`:
                New table without the column.
        """
        table = self.table.remove_column(i, *args, **kwargs)
        name = self.table.column_names[i]
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [
                    t.remove_column(t.column_names.index(name), *args, **kwargs) if name in t.column_names else t
                    for t in tables
                ]
            )
        return ConcatenationTable(table, blocks)

    def set_column(self, *args, **kwargs):
        """
        Replace column in Table at position.

        Args:
            i (:obj:`int`):
                Index to place the column at.
            field_ (:obj:`Union[str, pyarrow.Field]`):
                If a string is passed then the type is deduced from the column
                data.
            column (:obj:`Union[pyarrow.Array, List[pyarrow.Array]]`):
                Column data.

        Returns:
            :class:`datasets.table.Table`:
                New table with the passed column set.
        """
        raise NotImplementedError()

    def rename_columns(self, names, *args, **kwargs):
        """
        Create new table with columns renamed to provided names.
        """
        table = self.table.rename_columns(names, *args, **kwargs)
        names = dict(zip(self.table.column_names, names))
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [t.rename_columns([names[name] for name in t.column_names], *args, **kwargs) for t in tables]
            )
        return ConcatenationTable(table, blocks)

    def drop(self, columns, *args, **kwargs):
        """
        Drop one or more columns and return a new table.

        Args:
            columns (:obj:`List[str]`):
                List of field names referencing existing columns.

        Raises:
            KeyError : if any of the passed columns name are not existing.

        Returns:
            :class:`datasets.table.Table`:
                New table without the columns.
        """
        table = self.table.drop(columns)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.drop([c for c in columns if c in t.column_names], *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)


def concat_tables(tables: List[Table], axis: int = 0) -> Table:
    """
    Concatenate tables.

    Args:
        tables (list of :class:`Table`): List of tables to be concatenated.
        axis (``{0, 1}``, defaults to :obj:`0`, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            *New in version 1.6.0*

    Returns:
        :class:`datasets.table.Table`:
            If the number of input tables is > 1, then the returned table is a :obj:`datasets.table.ConcatenationTable`.
            Otherwise if there's only one table, it is returned as is.
    """
    tables = list(tables)
    if len(tables) == 1:
        return tables[0]
    return ConcatenationTable.from_tables(tables, axis=axis)


def list_table_cache_files(table: Table) -> List[str]:
    """
    Get the cache files that are loaded by the table.
    Cache file are used when parts of the table come from the disk via memory mapping.

    Returns:
        :obj:`List[str]`: a list of paths to the cache files loaded by the table
    """
    if isinstance(table, ConcatenationTable):
        cache_files = []
        for subtables in table.blocks:
            for subtable in subtables:
                cache_files += list_table_cache_files(subtable)
        return cache_files
    elif isinstance(table, MemoryMappedTable):
        return [table.path]
    else:
        return []


def _wrap_for_chunked_arrays(func):
    """Apply the function on each chunk of a pyarrow.ChunkedArray, or on the array directly"""

    def wrapper(array, *args, **kwargs):
        if isinstance(array, pa.ChunkedArray):
            return pa.chunked_array([func(chunk, *args, **kwargs) for chunk in array.chunks])
        else:
            return func(array, *args, **kwargs)

    return wrapper


@_wrap_for_chunked_arrays
def array_cast(array: pa.Array, pa_type: pa.DataType, allow_number_to_str=True):
    """Improved version of pa.Array.cast

    It supports casting pa.StructArray objects to re-order the fields.
    It also let you control certain aspects of the casting, e.g. whether
    to disable numbers (floats or ints) to strings.

    Args:
        array (pa.Array): PyArrow array to cast
        pa_type (pa.DataType): target PyArrow type
        allow_number_to_str (bool, defaults to :obj:`True`): Whether to allow casting numbers to strings.
            Defaults to True.

    Raises:
        pa.ArrowInvalidError: if the arrow data casting fails
        TypeError: if the target type is not supported according, e.g.

            - if a field is missing
            = if casting from numbers to strings and allow_number_to_str is False

    Returns:
        :obj:`List[pyarrow.Array]`: the casted array
    """
    _c = partial(array_cast, allow_number_to_str=allow_number_to_str)
    if isinstance(array, pa.ExtensionArray):
        array = array.storage
    if isinstance(pa_type, pa.ExtensionType):
        return pa_type.wrap_array(array)
    elif array.type == pa_type:
        return array
    elif pa.types.is_struct(array.type):
        if pa.types.is_struct(pa_type) and (
            set(field.name for field in pa_type) == set(field.name for field in array.type)
        ):
            arrays = [_c(array.field(field.name), field.type) for field in pa_type]
            return pa.StructArray.from_arrays(arrays, fields=list(pa_type), mask=array.is_null())
    elif pa.types.is_list(array.type):
        if pa.types.is_fixed_size_list(pa_type):
            if pa_type.list_size * len(array) == len(array.values):
                return pa.FixedSizeListArray.from_arrays(
                    _c(array.values, pa_type.value_type),
                    pa_type.list_size,
                )
        elif pa.types.is_list(pa_type):
            if array.null_count > 0:
                warnings.warn(
                    f"None values are converted to empty lists when converting array to {pa_type}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                )
            return pa.ListArray.from_arrays(array.offsets, _c(array.values, pa_type.value_type))
    elif pa.types.is_fixed_size_list(array.type):
        if pa.types.is_fixed_size_list(pa_type):
            return pa.FixedSizeListArray.from_arrays(
                _c(array.values, pa_type.value_type),
                pa_type.list_size,
            )
        elif pa.types.is_list(pa_type):
            offsets_arr = pa.array(range(len(array) + 1), pa.int32())
            if array.null_count > 0:
                warnings.warn(
                    f"None values are converted to empty lists when converting array to {pa_type}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                )
            return pa.ListArray.from_arrays(offsets_arr, _c(array.values, pa_type.value_type))
    else:
        if (
            not allow_number_to_str
            and pa.types.is_string(pa_type)
            and (pa.types.is_floating(array.type) or pa.types.is_integer(array.type))
        ):
            raise TypeError(
                f"Couldn't cast array of type {array.type} to {pa_type} since allow_number_to_str is set to {allow_number_to_str}"
            )
        if pa.types.is_null(pa_type) and not pa.types.is_null(array.type):
            raise TypeError(f"Couldn't cast array of type {array.type} to {pa_type}")
        return array.cast(pa_type)
    raise TypeError(f"Couldn't cast array of type\n{array.type}\nto\n{pa_type}")


@_wrap_for_chunked_arrays
def cast_array_to_feature(array: pa.Array, feature: "FeatureType", allow_number_to_str=True):
    """Cast an array to the arrow type that corresponds to the requested feature type.
    For custom features like Audio or Image, it takes into account the "cast_storage" methods
    they defined to enable casting from other arrow types.

    Args:
        array (pa.Array): the PyArrow array to cast
        feature (FeatureType): the target feature type
        allow_number_to_str (bool, defaults to :obj:`True`): Whether to allow casting numbers to strings.
            Defaults to True.

    Raises:
        pa.ArrowInvalidError: if the arrow data casting fails
        TypeError: if the target type is not supported according, e.g.

            - if a field is missing
            = if casting from numbers to strings and allow_number_to_str is False

    Returns:
        array (:obj:`pyarrow.Array`): the casted array
    """
    from .features.features import Sequence, get_nested_type

    _c = partial(cast_array_to_feature, allow_number_to_str=allow_number_to_str)

    if isinstance(array, pa.ExtensionArray):
        array = array.storage
    if hasattr(feature, "cast_storage"):
        return feature.cast_storage(array)
    elif pa.types.is_struct(array.type):
        # feature must be a dict or Sequence(subfeatures_dict)
        if isinstance(feature, Sequence) and isinstance(feature.feature, dict):
            feature = {
                name: Sequence(subfeature, length=feature.length) for name, subfeature in feature.feature.items()
            }
        if isinstance(feature, dict) and set(field.name for field in array.type) == set(feature):
            arrays = [_c(array.field(name), subfeature) for name, subfeature in feature.items()]
            return pa.StructArray.from_arrays(arrays, names=list(feature), mask=array.is_null())
    elif pa.types.is_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            casted_values = _c(array.values, feature[0])
            if casted_values.type == array.values.type:
                return array
            else:
                if array.null_count > 0:
                    warnings.warn(
                        f"None values are converted to empty lists when converting array to {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                    )
                return pa.ListArray.from_arrays(array.offsets, casted_values)
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_c(array.values, feature.feature), feature.length)
            else:
                casted_values = _c(array.values, feature.feature)
                if casted_values.type == array.values.type:
                    return array
                else:
                    if array.null_count > 0:
                        warnings.warn(
                            f"None values are converted to empty lists when converting array to {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                        )
                    return pa.ListArray.from_arrays(array.offsets, _c(array.values, feature.feature))
    elif pa.types.is_fixed_size_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            if array.null_count > 0:
                warnings.warn(
                    f"None values are converted to empty lists when converting array to {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                )
            return pa.ListArray.from_arrays(array.offsets, _c(array.values, feature[0]))
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_c(array.values, feature.feature), feature.length)
            else:
                offsets_arr = pa.array(range(len(array) + 1), pa.int32())
                if array.null_count > 0:
                    warnings.warn(
                        f"None values are converted to empty lists when converting array to {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                    )
                return pa.ListArray.from_arrays(offsets_arr, _c(array.values, feature.feature))
    if pa.types.is_null(array.type):
        return array_cast(array, get_nested_type(feature), allow_number_to_str=allow_number_to_str)
    elif not isinstance(feature, (Sequence, dict, list, tuple)):
        return array_cast(array, feature(), allow_number_to_str=allow_number_to_str)
    raise TypeError(f"Couldn't cast array of type\n{array.type}\nto\n{feature}")


@_wrap_for_chunked_arrays
def embed_array_storage(array: pa.Array, feature: "FeatureType"):
    """Embed data into an arrays's storage.
    For custom features like Audio or Image, it takes into account the "embed_storage" methods
    they defined to enable embedding external data (e.g. an image file) into an other arrow types.

    <Added version="2.4.0"/>

    Args:
        array (pa.Array): the PyArrow array in which to embed data
        feature (FeatureType): array features

    Raises:
        TypeError: if the target type is not supported according, e.g.

            - if a field is missing

    Returns:
         array (:obj:`pyarrow.Array`): the casted array
    """
    from .features import Sequence

    _e = embed_array_storage

    if isinstance(array, pa.ExtensionArray):
        array = array.storage
    if hasattr(feature, "embed_storage"):
        return feature.embed_storage(array)
    elif pa.types.is_struct(array.type):
        # feature must be a dict or Sequence(subfeatures_dict)
        if isinstance(feature, Sequence) and isinstance(feature.feature, dict):
            feature = {
                name: Sequence(subfeature, length=feature.length) for name, subfeature in feature.feature.items()
            }
        if isinstance(feature, dict):
            arrays = [_e(array.field(name), subfeature) for name, subfeature in feature.items()]
            return pa.StructArray.from_arrays(arrays, names=list(feature), mask=array.is_null())
    elif pa.types.is_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            if array.null_count > 0:
                warnings.warn(
                    f"None values are converted to empty lists when embedding array storage with {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                )
            return pa.ListArray.from_arrays(array.offsets, _e(array.values, feature[0]))
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_e(array.values, feature.feature), feature.length)
            else:
                casted_values = _e(array.values, feature.feature)
                if casted_values.type == array.values.type:
                    return array
                else:
                    if array.null_count > 0:
                        warnings.warn(
                            f"None values are converted to empty lists when embedding array storage with {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                        )
                    return pa.ListArray.from_arrays(array.offsets, _e(array.values, feature.feature))
    elif pa.types.is_fixed_size_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            if array.null_count > 0:
                warnings.warn(
                    f"None values are converted to empty lists when embedding array storage with {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                )
            return pa.ListArray.from_arrays(array.offsets, _e(array.values, feature[0]))
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_e(array.values, feature.feature), feature.length)
            else:
                offsets_arr = pa.array(range(len(array) + 1), pa.int32())
                if array.null_count > 0:
                    warnings.warn(
                        f"None values are converted to empty lists when embedding array storage with {feature}. More info: https://github.com/huggingface/datasets/issues/3676. This will raise an error in a future major version of `datasets`"
                    )
                return pa.ListArray.from_arrays(offsets_arr, _e(array.values, feature.feature))
    if not isinstance(feature, (Sequence, dict, list, tuple)):
        return array
    raise TypeError(f"Couldn't embed array of type\n{array.type}\nwith\n{feature}")


def cast_table_to_features(table: pa.Table, features: "Features"):
    """Cast a table to the arrow schema that corresponds to the requested features.

    Args:
        table (:obj:`pyarrow.Table`): PyArrow table to cast
        features (Features): target features.

    Returns:
        table (:obj:`pyarrow.Table`): the casted table
    """
    if sorted(table.column_names) != sorted(features):
        raise ValueError(f"Couldn't cast\n{table.schema}\nto\n{features}\nbecause column names don't match")
    arrays = [cast_array_to_feature(table[name], feature) for name, feature in features.items()]
    return pa.Table.from_arrays(arrays, schema=features.arrow_schema)


def cast_table_to_schema(table: pa.Table, schema: pa.Schema):
    """Cast a table to the arrow schema. Different from `cast_table_to_features`, this method can preserve nullability.

    Args:
        table (pa.Table): PyArrow table to cast
        features (Features): target features.

    Returns:
        pa.Table: the casted table
    """
    from .features import Features

    features = Features.from_arrow_schema(schema)
    if sorted(table.column_names) != sorted(features):
        raise ValueError(f"Couldn't cast\n{table.schema}\nto\n{features}\nbecause column names don't match")
    arrays = [cast_array_to_feature(table[name], feature) for name, feature in features.items()]
    return pa.Table.from_arrays(arrays, schema=schema)


def embed_table_storage(table: pa.Table):
    """Embed external data into a table's storage.

    <Added version="2.4.0"/>

    Args:
        table (:obj:`pyarrow.Table`): PyArrow table in which to embed data

    Returns:
        table (:obj:`pyarrow.Table`): the table with embedded data
    """
    from .features.features import Features, require_storage_embed

    features = Features.from_arrow_schema(table.schema)
    arrays = [
        embed_array_storage(table[name], feature) if require_storage_embed(feature) else table[name]
        for name, feature in features.items()
    ]
    return pa.Table.from_arrays(arrays, schema=features.arrow_schema)


def table_cast(table: pa.Table, schema: pa.Schema):
    """Improved version of pa.Table.cast.

    It supports casting to feature types stored in the schema metadata.

    Args:
        table (:obj:`pyarrow.Table`): PyArrow table to cast
        schema (:obj:`pyarrow.Schema`): target PyArrow schema.

    Returns:
        table (:obj:`pyarrow.Table`): the casted table
    """
    if table.schema != schema:
        return cast_table_to_schema(table, schema)
    elif table.schema.metadata != schema.metadata:
        return table.replace_schema_metadata(schema.metadata)
    else:
        return table


def table_flatten(table: pa.Table):
    """Improved version of pa.Table.flatten.

    It behaves as pa.Table.flatten in a sense it does 1-step flatten of the columns with a struct type into one column per struct field,
    but updates the metadata and skips decodable features unless the `decode` attribute of these features is set to False.

    Args:
        table (Table): PyArrow table to flatten

    Returns:
        Table: the flattened table
    """
    from .features import Features

    features = Features.from_arrow_schema(table.schema)
    if any(hasattr(subfeature, "flatten") and subfeature.flatten() == subfeature for subfeature in features.values()):
        flat_arrays = []
        flat_column_names = []
        for field in table.schema:
            array = table.column(field.name)
            subfeature = features[field.name]
            if pa.types.is_struct(field.type) and (
                not hasattr(subfeature, "flatten") or subfeature.flatten() != subfeature
            ):
                flat_arrays.extend(array.flatten())
                flat_column_names.extend([f"{field.name}.{subfield.name}" for subfield in field.type])
            else:
                flat_arrays.append(array)
                flat_column_names.append(field.name)
        flat_table = pa.Table.from_arrays(
            flat_arrays,
            names=flat_column_names,
        )
    else:
        flat_table = table.flatten()
    # Preserve complex types in the metadata
    flat_features = features.flatten(max_depth=2)
    flat_features = Features({column_name: flat_features[column_name] for column_name in flat_table.column_names})
    return flat_table.replace_schema_metadata(flat_features.arrow_schema.metadata)


def table_visitor(table: pa.Table, function: Callable[[pa.Array], None]):
    """Visit all arrays in a table and apply a function to them.

    Args:
        table (:obj:`pyarrow.Table`): PyArrow table to visit
        function (Callable[[pa.Array], None]): function to apply to each array
    """
    from .features import Features, Sequence

    features = Features.from_arrow_schema(table.schema)

    def _visit(array, feature):
        if isinstance(array, pa.ChunkedArray):
            for chunk in array.chunks:
                _visit(chunk, feature)
        else:
            if isinstance(array, pa.ExtensionArray):
                array = array.storage
            function(array, feature)
            if pa.types.is_struct(array.type) and not hasattr(feature, "cast_storage"):
                if isinstance(feature, Sequence) and isinstance(feature.feature, dict):
                    feature = {
                        name: Sequence(subfeature, length=feature.length)
                        for name, subfeature in feature.feature.items()
                    }
                for name, subfeature in feature.items():
                    _visit(array.field(name), subfeature)
            elif pa.types.is_list(array.type):
                if isinstance(feature, list):
                    _visit(array.values, feature[0])
                elif isinstance(feature, Sequence):
                    _visit(array.values, feature.feature)

    for name, feature in features.items():
        _visit(table[name], feature)


def table_iter(pa_table: pa.Table, batch_size: int, drop_last_batch=False):
    """Iterate over sub-tables of size `batch_size`.

    Requires pyarrow>=8.0.0

    Args:
        table (:obj:`pyarrow.Table`): PyArrow table to iterate over
        batch_size (:obj:`int`): size of each sub-table to yield
        drop_last_batch (:obj:`bool`, default `False`): Drop the last batch  if it is smaller than `batch_size`
    """
    if config.PYARROW_VERSION.major < 8:
        raise RuntimeError(f"pyarrow>=8.0.0 is needed to use table_iter but you have {config.PYARROW_VERSION}")
    chunks_buffer = []
    chunks_buffer_size = 0
    for chunk in pa_table.to_reader(max_chunksize=batch_size):
        if len(chunk) == 0:
            continue
        elif chunks_buffer_size + len(chunk) < batch_size:
            chunks_buffer.append(chunk)
            chunks_buffer_size += len(chunk)
            continue
        elif chunks_buffer_size + len(chunk) == batch_size:
            chunks_buffer.append(chunk)
            yield pa.Table.from_batches(chunks_buffer)
            chunks_buffer = []
            chunks_buffer_size = 0
        else:
            cropped_chunk_length = batch_size - chunks_buffer_size
            chunks_buffer.append(chunk.slice(0, cropped_chunk_length))
            yield pa.Table.from_batches(chunks_buffer)
            chunks_buffer = [chunk.slice(cropped_chunk_length, len(chunk) - cropped_chunk_length)]
            chunks_buffer_size = len(chunk) - cropped_chunk_length
    if not drop_last_batch and chunks_buffer:
        yield pa.Table.from_batches(chunks_buffer)
