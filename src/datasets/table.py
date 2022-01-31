import copy
import os
import tempfile
from functools import partial, wraps
from itertools import groupby
from typing import TYPE_CHECKING, List, Optional, Tuple, TypeVar, Union

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
from packaging import version

from . import config
from .utils.logging import get_logger


if TYPE_CHECKING:
    from .features import Features, FeatureType


logger = get_logger(__name__)

IS_PYARROW_AT_LEAST_4 = config.PYARROW_VERSION.major >= 4


def inject_arrow_table_documentation(arrow_table_method):
    def wrapper(method):
        out = wraps(arrow_table_method)(method)
        out.__doc__ = out.__doc__.replace("pyarrow.Table", "Table")
        return out

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

    @inject_arrow_table_documentation(pa.Table.validate)
    def validate(self, *args, **kwargs):
        return self.table.validate(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.equals)
    def equals(self, *args, **kwargs):
        args = tuple(arg.table if isinstance(arg, Table) else arg for arg in args)
        kwargs = {k: v.table if isinstance(v, Table) else v for k, v in kwargs}
        return self.table.equals(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_batches)
    def to_batches(self, *args, **kwargs):
        return self.table.to_batches(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_pydict)
    def to_pydict(self, *args, **kwargs):
        return self.table.to_pydict(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.to_pandas)
    def to_pandas(self, *args, **kwargs):
        return self.table.to_pandas(*args, **kwargs)

    def to_string(self, *args, **kwargs):
        return self.table.to_string(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.field)
    def field(self, *args, **kwargs):
        return self.table.field(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.column)
    def column(self, *args, **kwargs):
        return self.table.column(*args, **kwargs)

    @inject_arrow_table_documentation(pa.Table.itercolumns)
    def itercolumns(self, *args, **kwargs):
        return self.table.itercolumns(*args, **kwargs)

    @property
    def schema(self):
        return self.table.schema

    @property
    def columns(self):
        return self.table.columns

    @property
    def num_columns(self):
        return self.table.num_columns

    @property
    def num_rows(self):
        return self.table.num_rows

    @property
    def shape(self):
        return self.table.shape

    @property
    def nbytes(self):
        return self.table.nbytes

    @property
    def column_names(self):
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

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.replace_schema_metadata)
    def replace_schema_metadata(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, *args, **kwargs):
        raise NotImplementedError()

    # Additional methods that are based on the PyArrow Table methods

    def select_columns(self, columns: List[int]) -> "Table":
        """Return the table by keeping only the requested columns

        Returns:
            Table: table with only a subset of the columns
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
    @inject_arrow_table_documentation(pa.Table.from_pandas)
    def from_pandas(cls, *args, **kwargs):
        return cls(pa.Table.from_pandas(*args, **kwargs))

    @classmethod
    @inject_arrow_table_documentation(pa.Table.from_arrays)
    def from_arrays(cls, *args, **kwargs):
        return cls(pa.Table.from_arrays(*args, **kwargs))

    @classmethod
    @inject_arrow_table_documentation(pa.Table.from_pydict)
    def from_pydict(cls, *args, **kwargs):
        return cls(pa.Table.from_pydict(*args, **kwargs))

    @classmethod
    @inject_arrow_table_documentation(pa.Table.from_batches)
    def from_batches(cls, *args, **kwargs):
        return cls(pa.Table.from_batches(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, offset=0, length=None):
        # Use fast slicing here
        return InMemoryTable(self.fast_slice(offset=offset, length=length))

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        return InMemoryTable(self.table.filter(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        return InMemoryTable(self.table.flatten(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        return InMemoryTable(self.table.combine_chunks(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        return InMemoryTable(table_cast(self.table, *args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.replace_schema_metadata)
    def replace_schema_metadata(self, *args, **kwargs):
        return InMemoryTable(self.table.replace_schema_metadata(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        return InMemoryTable(self.table.add_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        return InMemoryTable(self.table.append_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        return InMemoryTable(self.table.remove_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        return InMemoryTable(self.table.set_column(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        return InMemoryTable(self.table.rename_columns(*args, **kwargs))

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, *args, **kwargs):
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
                else:
                    table = getattr(table, name)(*args, **kwargs)
        return table

    def _append_replay(self, replay: Replay) -> List[Replay]:
        replays = copy.deepcopy(self.replays)
        replays.append(replay)
        return replays

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, offset=0, length=None):
        replay = ("slice", (offset, length), {})
        replays = self._append_replay(replay)
        # Use fast slicing here
        return MemoryMappedTable(self.fast_slice(offset=offset, length=length), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, *args, **kwargs):
        replay = ("filter", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.filter(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        replay = ("flatten", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.flatten(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        replay = ("combine_chunks", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.combine_chunks(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, *args, **kwargs):
        replay = ("cast", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(table_cast(self.table, *args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.replace_schema_metadata)
    def replace_schema_metadata(self, *args, **kwargs):
        replay = ("replace_schema_metadata", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.replace_schema_metadata(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        replay = ("add_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.add_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        replay = ("append_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.append_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, *args, **kwargs):
        replay = ("remove_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.remove_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        replay = ("set_column", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.set_column(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, *args, **kwargs):
        replay = ("rename_columns", copy.deepcopy(args), copy.deepcopy(kwargs))
        replays = self._append_replay(replay)
        return MemoryMappedTable(self.table.rename_columns(*args, **kwargs), self.path, replays)

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, *args, **kwargs):
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
            axis: (``{0, 1}``, default ``0``, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            .. versionadded:: 1.6.0
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

    @inject_arrow_table_documentation(pa.Table.slice)
    def slice(self, offset=0, length=None):
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

    @inject_arrow_table_documentation(pa.Table.filter)
    def filter(self, mask, *args, **kwargs):
        table = self.table.filter(mask, *args, **kwargs)
        blocks = []
        for (offset, length), tables in zip(self._slices, self.blocks):
            submask = mask.slice(offset, length)
            blocks.append([t.filter(submask, *args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.flatten)
    def flatten(self, *args, **kwargs):
        table = self.table.flatten(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.flatten(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.combine_chunks)
    def combine_chunks(self, *args, **kwargs):
        table = self.table.combine_chunks(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.combine_chunks(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.cast)
    def cast(self, target_schema, *args, **kwargs):
        table = table_cast(self.table, target_schema, *args, **kwargs)
        blocks = []
        for subtables in self.blocks:
            new_tables = []
            fields = list(target_schema)
            for subtable in subtables:
                subfields = []
                for name in subtable.column_names:
                    subfields.append(fields.pop(next(i for i, field in enumerate(fields) if field.name == name)))
                subschema = pa.schema(subfields)
                new_tables.append(subtable.cast(subschema, *args, **kwargs))
            blocks.append(new_tables)
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.replace_schema_metadata)
    def replace_schema_metadata(self, *args, **kwargs):
        table = self.table.replace_schema_metadata(*args, **kwargs)
        blocks = []
        for tables in self.blocks:
            blocks.append([t.replace_schema_metadata(*args, **kwargs) for t in tables])
        return ConcatenationTable(table, self.blocks)

    @inject_arrow_table_documentation(pa.Table.add_column)
    def add_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.append_column)
    def append_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.remove_column)
    def remove_column(self, i, *args, **kwargs):
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

    @inject_arrow_table_documentation(pa.Table.set_column)
    def set_column(self, *args, **kwargs):
        raise NotImplementedError()

    @inject_arrow_table_documentation(pa.Table.rename_columns)
    def rename_columns(self, names, *args, **kwargs):
        table = self.table.rename_columns(names, *args, **kwargs)
        names = dict(zip(self.table.column_names, names))
        blocks = []
        for tables in self.blocks:
            blocks.append(
                [t.rename_columns([names[name] for name in t.column_names], *args, **kwargs) for t in tables]
            )
        return ConcatenationTable(table, blocks)

    @inject_arrow_table_documentation(pa.Table.drop)
    def drop(self, columns, *args, **kwargs):
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
        axis (``{0, 1}``, default ``0``, meaning over rows):
            Axis to concatenate over, where ``0`` means over rows (vertically) and ``1`` means over columns
            (horizontally).

            .. versionadded:: 1.6.0

    Returns:
        :obj:`datasets.table.Table` that is the concatenated table:
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


def _sanitize_sliced_list_arrays_for_cast(func):
    """Sanitize pyarrow.ListArray objects for pyarrow.Array.cast in case they are sliced list arrays"""

    @_wrap_for_chunked_arrays
    def _sanitize(array: pa.ListArray) -> pa.ListArray:
        """Return the same pyarrow.ListArray but with array.offset == 0 for compatibility with cast for pyarrow 3"""
        if array.offset == 0:
            return array
        elif len(array) == 0:
            return array.values.slice(0, 0)
        else:
            values_offset = array.offsets[0]  # the relevant values start at this index
            new_values = array.values.slice(values_offset.as_py())  # get the values to start at the right position
            new_offsets = pc.subtract(array.offsets, values_offset)  # update the offsets accordingly
            return pa.ListArray.from_arrays(new_offsets, new_values)

    def wrapper(array, *args, **kwargs):
        if pa.types.is_list(array.type) and config.PYARROW_VERSION < version.parse("4.0.0"):
            array = _sanitize(array)
        return func(array, *args, **kwargs)

    return wrapper


@_sanitize_sliced_list_arrays_for_cast
@_wrap_for_chunked_arrays
def array_cast(array: pa.Array, pa_type: pa.DataType, allow_number_to_str=True):
    """Improved version of pa.Array.cast

    It supports casting pa.StructArray objects to re-order the fields.
    It also let you control certain aspects of the casting, e.g. whether
    to disable numbers (floats or ints) to strings.

    Args:
        array (pa.Array): PyArrow array to cast
        pa_type (pa.DataType): target PyArrow type
        allow_number_to_str (bool, default ``True``): Whether to allow casting numbers to strings.
            Defaults to True.

    Raises:
        pa.ArrowInvalidError: if the arrow data casting fails
        TypeError: if the target type is not supported according, e.g.

            - if a field is missing
            = if casting from numbers to strings and allow_number_to_str is False

    Returns:
        pa.Array: the casted array
    """
    _c = partial(array_cast, allow_number_to_str=allow_number_to_str)
    if isinstance(array, pa.ExtensionArray):
        array = array.storage
    if isinstance(pa_type, pa.ExtensionType):
        return pa_type.wrap_array(array)
    elif pa.types.is_struct(array.type):
        if pa.types.is_struct(pa_type) and (
            set(field.name for field in pa_type) == set(field.name for field in array.type)
        ):
            arrays = [
                _c(array.field(field.name), field.type, allow_number_to_str=allow_number_to_str) for field in pa_type
            ]
            return pa.StructArray.from_arrays(arrays, fields=list(pa_type))
    elif pa.types.is_list(array.type):
        if pa.types.is_fixed_size_list(pa_type):
            if pa_type.list_size * len(array) == len(array.values):
                return pa.FixedSizeListArray.from_arrays(
                    _c(array.values, pa_type.value_type, allow_number_to_str=allow_number_to_str),
                    pa_type.list_size,
                )
        elif pa.types.is_list(pa_type):
            return pa.ListArray.from_arrays(
                array.offsets, _c(array.values, pa_type.value_type, allow_number_to_str=allow_number_to_str)
            )
    elif pa.types.is_fixed_size_list(array.type):
        if pa.types.is_fixed_size_list(pa_type):
            return pa.FixedSizeListArray.from_arrays(
                _c(array.values, pa_type.value_type, allow_number_to_str=allow_number_to_str),
                pa_type.list_size,
            )
        elif pa.types.is_list(pa_type):
            offsets_arr = pa.array(range(len(array) + 1), pa.int32())
            return pa.ListArray.from_arrays(
                offsets_arr, _c(array.values, pa_type.value_type, allow_number_to_str=allow_number_to_str)
            )
    else:
        if (
            not allow_number_to_str
            and pa.types.is_string(pa_type)
            and (pa.types.is_floating(array.type) or pa.types.is_integer(array.type))
        ):
            raise TypeError(
                f"Couldn't cast array of type {array.type} to {pa_type} since allow_number_to_str is set to {allow_number_to_str}"
            )
        return array.cast(pa_type)
    raise TypeError(f"Couldn't cast array of type\n{array.type}\nto\n{pa_type}")


@_sanitize_sliced_list_arrays_for_cast
@_wrap_for_chunked_arrays
def cast_array_to_feature(array: pa.Array, feature: "FeatureType", allow_number_to_str=True):
    """Cast an array to the arrow type that corresponds to the requested feature type.
    For custom features like Audio or Image, it takes into account the "cast_storage" methods
    they defined to enable casting from other arrow types.

    Args:
        array (pa.Array): the PyArrow array to cast
        feature (FeatureType): the target feature type
        allow_number_to_str (bool, default ``True``): Whether to allow casting numbers to strings.
            Defaults to True.

    Raises:
        pa.ArrowInvalidError: if the arrow data casting fails
        TypeError: if the target type is not supported according, e.g.

            - if a field is missing
            = if casting from numbers to strings and allow_number_to_str is False

    Returns:
        pa.Array: the casted array
    """
    from .features import Sequence, get_nested_type

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
            return pa.StructArray.from_arrays(arrays, names=list(feature))
    elif pa.types.is_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            return pa.ListArray.from_arrays(array.offsets, _c(array.values, feature[0]))
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_c(array.values, feature.feature), feature.length)
            else:
                return pa.ListArray.from_arrays(array.offsets, _c(array.values, feature.feature))
    elif pa.types.is_fixed_size_list(array.type):
        # feature must be either [subfeature] or Sequence(subfeature)
        if isinstance(feature, list):
            return pa.ListArray.from_arrays(array.offsets, _c(array.values, feature[0]))
        elif isinstance(feature, Sequence):
            if feature.length > -1:
                if feature.length * len(array) == len(array.values):
                    return pa.FixedSizeListArray.from_arrays(_c(array.values, feature.feature), feature.length)
            else:
                offsets_arr = pa.array(range(len(array) + 1), pa.int32())
                return pa.ListArray.from_arrays(offsets_arr, _c(array.values, feature.feature))
    if pa.types.is_null(array.type):
        return array_cast(array, get_nested_type(feature), allow_number_to_str=allow_number_to_str)
    elif not isinstance(feature, (Sequence, dict, list, tuple)):
        return array_cast(array, feature(), allow_number_to_str=allow_number_to_str)
    raise TypeError(f"Couldn't cast array of type\n{array.type}\nto\n{feature}")


def cast_table_to_features(table: pa.Table, features: "Features"):
    """Cast an table to the arrow schema that corresponds to the requested features.

    Args:
        table (pa.Table): PyArrow table to cast
        features (Features): target features.

    Returns:
        pa.Table: the casted table
    """
    if sorted(table.column_names) != sorted(features):
        raise ValueError(f"Couldn't cast\n{table.schema}\nto\n{features}\nbecause column names don't match")
    arrays = [cast_array_to_feature(table[name], feature) for name, feature in features.items()]
    return pa.Table.from_arrays(arrays, schema=features.arrow_schema)


def table_cast(table: pa.Table, schema: pa.Schema):
    """Improved version of pa.Table.cast

    It supports casting to feature types stored in the schema metadata.

    Args:
        table (pa.Table): PyArrow table to cast
        schema (pa.Schema): target PyArrow schema.

    Returns:
        pa.Table: the casted table
    """
    if table.schema != schema:
        from .features import Features

        return cast_table_to_features(table, Features.from_arrow_schema(schema))
    elif table.schema.metadata != schema.metadata:
        return table.replace_schema_metadata(schema.metadata)
    else:
        return table
