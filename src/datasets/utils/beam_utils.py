from typing import Optional

import pyarrow as pa
from apache_beam import PTransform
from apache_beam.io import filebasedsink
from apache_beam.io.filesystem import CompressionTypes
from apache_beam.io.iobase import Write
from apache_beam.transforms import ParDo
from packaging import version

from ..config import BEAM_VERSION


if BEAM_VERSION >= version.parse("2.44.0"):
    from apache_beam.io.parquetio import _RowDictionariesToArrowTable
else:
    # Copied from https://github.com/apache/beam/blob/bdfd27e62885bd736c5600d0c6496bf96fe66a77/sdks/python/apache_beam/io/parquetio.py#L88
    from apache_beam.transforms import DoFn, window

    class _RowDictionariesToArrowTable(DoFn):
        """A DoFn that consumes python dictionarys and yields a pyarrow table."""

        def __init__(self, schema, row_group_buffer_size=64 * 1024 * 1024, record_batch_size=1000):
            self._schema = schema
            self._row_group_buffer_size = row_group_buffer_size
            self._buffer = [[] for _ in range(len(schema.names))]
            self._buffer_size = record_batch_size
            self._record_batches = []
            self._record_batches_byte_size = 0

        def process(self, row):
            if len(self._buffer[0]) >= self._buffer_size:
                self._flush_buffer()

            if self._record_batches_byte_size >= self._row_group_buffer_size:
                table = self._create_table()
                yield table

            # reorder the data in columnar format.
            for i, n in enumerate(self._schema.names):
                self._buffer[i].append(row[n])

        def finish_bundle(self):
            if len(self._buffer[0]) > 0:
                self._flush_buffer()
            if self._record_batches_byte_size > 0:
                table = self._create_table()
                yield window.GlobalWindows.windowed_value_at_end_of_window(table)

        def display_data(self):
            res = super().display_data()
            res["row_group_buffer_size"] = str(self._row_group_buffer_size)
            res["buffer_size"] = str(self._buffer_size)

            return res

        def _create_table(self):
            table = pa.Table.from_batches(self._record_batches, schema=self._schema)
            self._record_batches = []
            self._record_batches_byte_size = 0
            return table

        def _flush_buffer(self):
            arrays = [[] for _ in range(len(self._schema.names))]
            for x, y in enumerate(self._buffer):
                arrays[x] = pa.array(y, type=self._schema.types[x])
                self._buffer[x] = []
            rb = pa.RecordBatch.from_arrays(arrays, schema=self._schema)
            self._record_batches.append(rb)
            size = 0
            for x in arrays:
                for b in x.buffers():
                    if b is not None:
                        size = size + b.size
            self._record_batches_byte_size = self._record_batches_byte_size + size


class WriteToArrow(PTransform):
    """
    A `PTransform` for writing arrow files.

    Writes arrow files from a `apache_beam.PCollection` of
    records. Each record is a dictionary with keys of a string type that
    represent column names.

    This transform is inspired by `apache_beam.io.parquetio.WriteToParquet`.

    Args:
        file_path_prefix (`str`): The file path to write to. The files written will begin
            with this prefix, followed by a shard identifier (see num_shards), and
            end in a common extension, if given by file_name_suffix. In most cases,
            only this argument is specified and num_shards, shard_name_template, and
            file_name_suffix use default values.
        schema (`pa.Schema`): The schema to use, as type of `pyarrow.Schema`.
        row_group_buffer_size (`int`, defaults to `64 * 1024 * 1024`):
            The byte size of the row group buffer. Note that
            this size is for uncompressed data on the memory and normally much
            bigger than the actual row group size written to a file.
        record_batch_size (`int`, defaults to `1000`): The number of records in each record batch. Record
            batch is a basic unit used for storing data in the row group buffer.
            A higher record batch size implies low granularity on a row group buffer
            size. For configuring a row group size based on the number of records,
            set ``row_group_buffer_size`` to 1 and use ``record_batch_size`` to
            adjust the value.
        codec (`str`, *optional*): The codec to use for block-level compression. Any string supported
            by the pyarrow specification is accepted.
        file_name_suffix (`str`, defaults to `""`): Suffix for the files written.
        num_shards (`int`, defaults to `0`): The number of files (shards) used for output. If not set, the
            service will decide on the optimal number of shards.
            Constraining the number of shards is likely to reduce
            the performance of a pipeline.  Setting this value is not recommended
            unless you require a specific number of output files.
        shard_name_template (`str`, *optional*): A template string containing placeholders for
            the shard number and shard count. When constructing a filename for a
            particular shard number, the upper-case letters 'S' and 'N' are
            replaced with the 0-padded shard number and shard count respectively.
            This argument can be '' in which case it behaves as if num_shards was
            set to 1 and only one file will be generated. The default pattern used
            is '-SSSSS-of-NNNNN' if None is passed as the shard_name_template.
        mime_type (`str`, defaults to `"application/x-arrow"`): The MIME type to use for the produced files, if the filesystem
            supports specifying MIME types.

    Returns:
        A `WriteToArrow` transform usable for writing.
    """

    def __init__(
        self,
        file_path_prefix: str,
        schema: pa.Schema,
        row_group_buffer_size: int = 64 * 1024 * 1024,
        record_batch_size: int = 1000,
        codec: Optional[str] = None,
        file_name_suffix: str = "",
        num_shards: int = 0,
        shard_name_template: Optional[str] = None,
        mime_type: str = "application/x-arrow",
    ):
        super().__init__()
        self._schema = schema
        self._row_group_buffer_size = row_group_buffer_size
        self._record_batch_size = record_batch_size

        self._sink = _IpcStreamSink(
            file_path_prefix, schema, codec, file_name_suffix, num_shards, shard_name_template, mime_type
        )

    def expand(self, pcoll):
        return (
            pcoll
            | ParDo(_RowDictionariesToArrowTable(self._schema, self._row_group_buffer_size, self._record_batch_size))
            | Write(self._sink)
        )

    def display_data(self):
        return {"sink_dd": self._sink, "row_group_buffer_size": str(self._row_group_buffer_size)}


class _IpcStreamSink(filebasedsink.FileBasedSink):
    """A sink for arrow files from batches."""

    def __init__(self, file_path_prefix, schema, codec, file_name_suffix, num_shards, shard_name_template, mime_type):
        super().__init__(
            file_path_prefix,
            file_name_suffix=file_name_suffix,
            num_shards=num_shards,
            shard_name_template=shard_name_template,
            coder=None,
            mime_type=mime_type,
            compression_type=CompressionTypes.UNCOMPRESSED,
        )
        self._schema = schema
        self._codec = codec
        self._file_handle = None

    def open(self, temp_path):
        self._file_handle = super().open(temp_path)
        return pa.RecordBatchStreamWriter(
            self._file_handle, self._schema, options=pa.ipc.IpcWriteOptions(compression=self._codec)
        )

    def write_record(self, writer, table: pa.Table):
        writer.write_table(table)

    def close(self, writer):
        writer.close()
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

    def display_data(self):
        res = super().display_data()
        res["codec"] = str(self._codec)
        res["schema"] = str(self._schema)
        return res
