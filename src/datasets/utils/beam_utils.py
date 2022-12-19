from typing import Optional

import pyarrow as pa
import pyarrow.parquet as pq
from apache_beam import PTransform
from apache_beam.io import filebasedsink
from apache_beam.io.filesystem import CompressionTypes
from apache_beam.io.iobase import Write
from apache_beam.transforms import DoFn, ParDo, window
from packaging import version

from .. import config
from ..features import Features
from ..table import cast_array_to_feature, embed_table_storage


# class BeamPipeline(Pipeline):
#     """Wrapper over `apache_beam.pipeline.Pipeline` for convenience"""

#     def is_local(self):
#         runner = self._options.get_all_options().get("runner")
#         return runner in [None, "DirectRunner", "PortableRunner"]


class _RowDictionariesToArrowTable(DoFn):
    """A DoFn that consumes python dictionarys and yields a pyarrow table."""

    def __init__(
        self,
        features: Features,
        row_group_buffer_size: int = 64 * 1024 * 1024,
        record_batch_size: int = 1000,
        with_metadata: bool = True,
        embed_local_files: bool = False,
    ):
        self._features = features
        self._schema = features.arrow_schema
        self._row_group_buffer_size = row_group_buffer_size
        self._buffer = [[] for _ in range(len(self._schema.names))]
        self._buffer_size = record_batch_size
        self._record_batches = []
        self._record_batches_byte_size = 0
        self._with_metadata = with_metadata
        self._embed_local_files = embed_local_files

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
            yield window.GlobalWindows.windowed_value(table, window.GlobalWindow().max_timestamp())

    def display_data(self):
        res = super().display_data()
        res["row_group_buffer_size"] = str(self._row_group_buffer_size)
        res["buffer_size"] = str(self._buffer_size)
        return res

    def _create_table(self):
        table = pa.Table.from_batches(self._record_batches, schema=self._schema)
        if self._embed_local_files:
            table = embed_table_storage(table)
        if not self._with_metadata:
            table = table.replace_schema_metadata()
        self._record_batches = []
        self._record_batches_byte_size = 0
        return table

    def _flush_buffer(self):
        arrays = [[] for _ in range(len(self._schema.names))]
        for i, (x, y) in enumerate(zip(self._schema.names, self._buffer)):
            arrays[i] = cast_array_to_feature(pa.array(y), self._features[x])
            self._buffer[i] = []
        rb = pa.RecordBatch.from_arrays(arrays, schema=self._schema)
        self._record_batches.append(rb)
        size = 0
        for x in arrays:
            for b in x.buffers():
                if b is not None:
                    size = size + b.size
        self._record_batches_byte_size = self._record_batches_byte_size + size


##################################
# Arrow write transform and sink #
##################################


class WriteToArrow(PTransform):
    """
    A `PTransform` for writing arrow files.

    Writes arrow files from a `apache_beam.PCollection` of
    records. Each record is a dictionary with keys of a string type that
    represent column names.

    Args:
        file_path_prefix (`str`): The file path to write to. The files written will begin
            with this prefix, followed by a shard identifier (see num_shards), and
            end in a common extension, if given by file_name_suffix. In most cases,
            only this argument is specified and num_shards, shard_name_template, and
            file_name_suffix use default values.
        features (`datasets.Features`): The features to cast the batches to.
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
        with_metadata (`bool`, defaults to `True`): Whether to write the schema metadata to the arrow files.
        embed_local_files (`bool`, defaults to `False`): Whether to embed local files in the arrow files.
        mime_type (`str`, defaults to `"application/x-arrow"`): The MIME type to use for the produced files, if the filesystem
            supports specifying MIME types.
        max_records_per_shard (`int`, *optional*): Maximum number of records to write to any individual shard.
        max_bytes_per_shard (`int`, *optional*): Target maximum number of bytes to write to any
            individual shard. This may be exceeded slightly, as a new shard is
            created once this limit is hit, but the remainder of a given record, a
            subsequent newline, and a footer may cause the actual shard size
            to exceed this value.  This also tracks the uncompressed,
            not compressed, size of the shard.

    Returns:
        A `WriteToArrow` transform usable for writing.
    """

    def __init__(
        self,
        file_path_prefix: str,
        features: Features,
        row_group_buffer_size: int = 64 * 1024 * 1024,
        record_batch_size: int = 1000,
        codec: Optional[str] = None,
        file_name_suffix: str = "",
        num_shards: int = 0,
        shard_name_template: Optional[str] = None,
        mime_type: str = "application/x-arrow",
        with_metadata: bool = True,
        embed_local_files: bool = False,
        max_records_per_shard: Optional[int] = None,
        max_bytes_per_shard: Optional[int] = None,
    ):
        super().__init__()
        self._features = features
        self._schema = features.arrow_schema
        self._row_group_buffer_size = row_group_buffer_size
        self._record_batch_size = record_batch_size
        self._with_metadata = with_metadata
        self._embed_local_files = embed_local_files

        self._sink = _IpcStreamSink(
            file_path_prefix,
            self._schema,
            codec,
            file_name_suffix,
            num_shards,
            shard_name_template,
            mime_type,
            max_records_per_shard,
            max_bytes_per_shard,
        )

    def expand(self, pcoll):
        return (
            pcoll
            | ParDo(
                _RowDictionariesToArrowTable(
                    self._features,
                    row_group_buffer_size=self._row_group_buffer_size,
                    record_batch_size=self._record_batch_size,
                    with_metadata=self._with_metadata,
                    embed_local_files=self._embed_local_files,
                )
            )
            | Write(self._sink)
        )

    def display_data(self):
        return {"sink_dd": self._sink, "row_group_buffer_size": str(self._row_group_buffer_size)}


class _IpcStreamSink(filebasedsink.FileBasedSink):
    """A sink for arrow files from batches."""

    def __init__(
        self,
        file_path_prefix,
        schema,
        codec,
        file_name_suffix,
        num_shards,
        shard_name_template,
        mime_type,
        max_records_per_shard,
        max_bytes_per_shard,
    ):
        shard_size_kwargs = {}
        if config.BEAM_VERSION >= version.parse("2.41.0"):
            shard_size_kwargs = {
                "max_records_per_shard": max_records_per_shard,
                "max_bytes_per_shard": max_bytes_per_shard,
            }
        super().__init__(
            file_path_prefix,
            file_name_suffix=file_name_suffix,
            num_shards=num_shards,
            shard_name_template=shard_name_template,
            coder=None,
            mime_type=mime_type,
            compression_type=CompressionTypes.UNCOMPRESSED,
            **shard_size_kwargs,
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


####################################
# Parquet write transform and sink #
####################################


class WriteToParquet(PTransform):
    """
    A `PTransform` for writing parquet files.

    Writes parquet files from a `apache_beam.PCollection` of
    records. Each record is a dictionary with keys of a string type that
    represent column names.

    Args:
        file_path_prefix (`str`): The file path to write to. The files written will begin
            with this prefix, followed by a shard identifier (see num_shards), and
            end in a common extension, if given by file_name_suffix. In most cases,
            only this argument is specified and num_shards, shard_name_template, and
            file_name_suffix use default values.
        features (`datasets.Features`): The features to cast the batches to.
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
        use_deprecated_int96_timestamps (`bool`, *optional*): Write nanosecond resolution timestamps to
            INT96 Parquet format. Defaults to False.
        use_compliant_nested_type (`bool`, defaults to `False`): Write compliant parquet nested type (lists).
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
        mime_type (`str`, defaults to `"application/x-parquet"`): The MIME type to use for the produced files, if the filesystem
            supports specifying MIME types.
        with_metadata (`bool`, defaults to `True`): Whether to write the schema metadata to the arrow files.
        embed_local_files (`bool`, defaults to `False`): Whether to embed local files in the arrow files.
        max_records_per_shard (`int`, *optional*): Maximum number of records to write to any individual shard.
        max_bytes_per_shard (`int`, *optional*): Target maximum number of bytes to write to any
            individual shard. This may be exceeded slightly, as a new shard is
            created once this limit is hit, but the remainder of a given record, a
            subsequent newline, and a footer may cause the actual shard size
            to exceed this value.  This also tracks the uncompressed,
            not compressed, size of the shard.

    Returns:
        A `WriteToParquet` transform usable for writing.
    """

    def __init__(
        self,
        file_path_prefix: str,
        features: Features,
        row_group_buffer_size: int = 64 * 1024 * 1024,
        record_batch_size: int = 1000,
        codec: str = "none",
        use_deprecated_int96_timestamps: Optional[bool] = None,
        use_compliant_nested_type: bool = False,
        file_name_suffix: str = "",
        num_shards: int = 0,
        shard_name_template: Optional[str] = None,
        mime_type: str = "application/x-parquet",
        with_metadata: bool = True,
        embed_local_files: bool = False,
        max_records_per_shard: Optional[int] = None,
        max_bytes_per_shard: Optional[int] = None,
    ):
        super().__init__()
        self._features = features
        self._schema = features.arrow_schema
        self._row_group_buffer_size = row_group_buffer_size
        self._record_batch_size = record_batch_size
        self._with_metadata = with_metadata
        self._embed_local_files = embed_local_files

        self._sink = _ParquetSink(
            file_path_prefix,
            self._schema,
            codec,
            use_deprecated_int96_timestamps,
            use_compliant_nested_type,
            file_name_suffix,
            num_shards,
            shard_name_template,
            mime_type,
            max_records_per_shard,
            max_bytes_per_shard,
        )

    def expand(self, pcoll):
        return (
            pcoll
            | ParDo(
                _RowDictionariesToArrowTable(
                    self._features,
                    row_group_buffer_size=self._row_group_buffer_size,
                    record_batch_size=self._record_batch_size,
                    with_metadata=self._with_metadata,
                    embed_local_files=self._embed_local_files,
                )
            )
            | Write(self._sink)
        )

    def display_data(self):
        return {"sink_dd": self._sink, "row_group_buffer_size": str(self._row_group_buffer_size)}


class _ParquetSink(filebasedsink.FileBasedSink):
    """A sink for parquet files from batches."""

    def __init__(
        self,
        file_path_prefix,
        schema,
        codec,
        use_deprecated_int96_timestamps,
        use_compliant_nested_type,
        file_name_suffix,
        num_shards,
        shard_name_template,
        mime_type,
        max_records_per_shard,
        max_bytes_per_shard,
    ):
        shard_size_kwargs = {}
        if config.BEAM_VERSION >= version.parse("2.41.0"):
            shard_size_kwargs = {
                "max_records_per_shard": max_records_per_shard,
                "max_bytes_per_shard": max_bytes_per_shard,
            }
        super().__init__(
            file_path_prefix,
            file_name_suffix=file_name_suffix,
            num_shards=num_shards,
            shard_name_template=shard_name_template,
            coder=None,
            mime_type=mime_type,
            compression_type=CompressionTypes.UNCOMPRESSED,
            **shard_size_kwargs,
        )
        self._schema = schema
        self._codec = codec
        self._file_handle = None
        self._use_deprecated_int96_timestamps = use_deprecated_int96_timestamps
        self._use_compliant_nested_type = use_compliant_nested_type

    def open(self, temp_path):
        self._file_handle = super().open(temp_path)
        return pq.ParquetWriter(
            self._file_handle,
            self._schema,
            compression=self._codec,
            use_deprecated_int96_timestamps=self._use_deprecated_int96_timestamps,
            use_compliant_nested_type=self._use_compliant_nested_type,
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
