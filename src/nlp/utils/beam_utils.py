import logging
import os

import pyarrow as pa
import pyarrow.parquet as pq
from apache_beam.io import filebasedsink
from apache_beam.io.filesystem import CompressionTypes
from apache_beam.io.filesystems import FileSystems
from apache_beam.io.iobase import Write
from apache_beam.pipeline import Pipeline
from apache_beam.transforms import PTransform


CHUNK_SIZE = 2 << 20  # 2mb
logger = logging.getLogger(__name__)


class BeamPipeline(Pipeline):
    """Wrapper over `apache_beam.pipeline.Pipeline` for convenience"""

    def is_local(self):
        runner = self._options.get_all_options().get("runner")
        return runner in [None, "DirectRunner", "PortableRunner"]


def upload_local_to_remote(local_file_path, remote_file_path, force_upload=False):
    """Use the Beam Filesystems to upload to a remote directory on gcs/s3/hdfs..."""
    fs = FileSystems
    if fs.exists(remote_file_path):
        if force_upload:
            logger.info("Remote path already exist: {}. Overwriting it as force_upload=True.".format(remote_file_path))
        else:
            logger.info("Remote path already exist: {}. Skipping it as force_upload=False.".format(remote_file_path))
            return
    with fs.create(remote_file_path) as remote_file:
        with open(local_file_path, "rb") as local_file:
            chunk = local_file.read(CHUNK_SIZE)
            while chunk:
                remote_file.write(chunk)
                chunk = local_file.read(CHUNK_SIZE)


def download_remote_to_local(remote_file_path, local_file_path, force_download=False):
    """Use the Beam Filesystems to download from a remote directory on gcs/s3/hdfs..."""
    fs = FileSystems
    if os.path.exists(local_file_path):
        if force_download:
            logger.info("Local path already exist: {}. Overwriting it as force_upload=True.".format(remote_file_path))
        else:
            logger.info("Local path already exist: {}. Skipping it as force_upload=False.".format(remote_file_path))
            return
    with fs.open(remote_file_path) as remote_file:
        with open(local_file_path, "wb") as local_file:
            chunk = remote_file.read(CHUNK_SIZE)
            while chunk:
                local_file.write(chunk)
                chunk = remote_file.read(CHUNK_SIZE)


class WriteToParquet(PTransform):
    """
    From `apache_beam.io.parquetio.WriteToParquet`, but with a fix for the jira issue `BEAM-10022`.
    Only the method `_flush_buffer` is different from the original implementation.

        A ``PTransform`` for writing parquet files.

        This ``PTransform`` is currently experimental. No backward-compatibility
        guarantees.
    """

    def __init__(
        self,
        file_path_prefix,
        schema,
        row_group_buffer_size=64 * 1024 * 1024,
        record_batch_size=1000,
        codec="none",
        use_deprecated_int96_timestamps=False,
        file_name_suffix="",
        num_shards=0,
        shard_name_template=None,
        mime_type="application/x-parquet",
    ):
        """Initialize a WriteToParquet transform.
        (from apache_beam.io.parquetio, only ._flush_buffer() is different)

        Writes parquet files from a :class:`~apache_beam.pvalue.PCollection` of
        records. Each record is a dictionary with keys of a string type that
        represent column names. Schema must be specified like the example below.

        .. testsetup::

            from tempfile import NamedTemporaryFile
            import glob
            import os
            import pyarrow

            filename = NamedTemporaryFile(delete=False).name

        .. testcode::

            with beam.Pipeline() as p:
                records = p | 'Read' >> beam.Create(
                        [{'name': 'foo', 'age': 10}, {'name': 'bar', 'age': 20}]
                )
                _ = records | 'Write' >> beam.io.WriteToParquet(filename,
                        pyarrow.schema(
                                [('name', pyarrow.binary()), ('age', pyarrow.int64())]
                        )
                )

        .. testcleanup::

            for output in glob.glob('{}*'.format(filename)):
                os.remove(output)

        For more information on supported types and schema, please see the pyarrow
        document.

        Args:
            file_path_prefix: The file path to write to. The files written will begin
                with this prefix, followed by a shard identifier (see num_shards), and
                end in a common extension, if given by file_name_suffix. In most cases,
                only this argument is specified and num_shards, shard_name_template, and
                file_name_suffix use default values.
            schema: The schema to use, as type of ``pyarrow.Schema``.
            row_group_buffer_size: The byte size of the row group buffer. Note that
                this size is for uncompressed data on the memory and normally much
                bigger than the actual row group size written to a file.
            record_batch_size: The number of records in each record batch. Record
                batch is a basic unit used for storing data in the row group buffer.
                A higher record batch size implies low granularity on a row group buffer
                size. For configuring a row group size based on the number of records,
                set ``row_group_buffer_size`` to 1 and use ``record_batch_size`` to
                adjust the value.
            codec: The codec to use for block-level compression. Any string supported
                by the pyarrow specification is accepted.
            use_deprecated_int96_timestamps: Write nanosecond resolution timestamps to
                INT96 Parquet format. Defaults to False.
            file_name_suffix: Suffix for the files written.
            num_shards: The number of files (shards) used for output. If not set, the
                service will decide on the optimal number of shards.
                Constraining the number of shards is likely to reduce
                the performance of a pipeline.  Setting this value is not recommended
                unless you require a specific number of output files.
            shard_name_template: A template string containing placeholders for
                the shard number and shard count. When constructing a filename for a
                particular shard number, the upper-case letters 'S' and 'N' are
                replaced with the 0-padded shard number and shard count respectively.
                This argument can be '' in which case it behaves as if num_shards was
                set to 1 and only one file will be generated. The default pattern used
                is '-SSSSS-of-NNNNN' if None is passed as the shard_name_template.
            mime_type: The MIME type to use for the produced files, if the filesystem
                supports specifying MIME types.

        Returns:
            A WriteToParquet transform usable for writing.
        """
        super(WriteToParquet, self).__init__()
        self._sink = _create_parquet_sink(
            file_path_prefix,
            schema,
            codec,
            row_group_buffer_size,
            record_batch_size,
            use_deprecated_int96_timestamps,
            file_name_suffix,
            num_shards,
            shard_name_template,
            mime_type,
        )

    def expand(self, pcoll):
        return pcoll | Write(self._sink)

    def display_data(self):
        return {"sink_dd": self._sink}


def _create_parquet_sink(
    file_path_prefix,
    schema,
    codec,
    row_group_buffer_size,
    record_batch_size,
    use_deprecated_int96_timestamps,
    file_name_suffix,
    num_shards,
    shard_name_template,
    mime_type,
):
    return _ParquetSink(
        file_path_prefix,
        schema,
        codec,
        row_group_buffer_size,
        record_batch_size,
        use_deprecated_int96_timestamps,
        file_name_suffix,
        num_shards,
        shard_name_template,
        mime_type,
    )


class _ParquetSink(filebasedsink.FileBasedSink):
    """A sink for parquet files."""

    def __init__(
        self,
        file_path_prefix,
        schema,
        codec,
        row_group_buffer_size,
        record_batch_size,
        use_deprecated_int96_timestamps,
        file_name_suffix,
        num_shards,
        shard_name_template,
        mime_type,
    ):
        super(_ParquetSink, self).__init__(
            file_path_prefix,
            file_name_suffix=file_name_suffix,
            num_shards=num_shards,
            shard_name_template=shard_name_template,
            coder=None,
            mime_type=mime_type,
            # Compression happens at the block level using the supplied codec, and
            # not at the file level.
            compression_type=CompressionTypes.UNCOMPRESSED,
        )
        self._schema = schema
        self._codec = codec
        self._row_group_buffer_size = row_group_buffer_size
        self._use_deprecated_int96_timestamps = use_deprecated_int96_timestamps
        self._buffer = [[] for _ in range(len(schema.names))]
        self._buffer_size = record_batch_size
        self._record_batches = []
        self._record_batches_byte_size = 0
        self._file_handle = None

    def open(self, temp_path):
        self._file_handle = super(_ParquetSink, self).open(temp_path)
        return pq.ParquetWriter(
            self._file_handle,
            self._schema,
            compression=self._codec,
            use_deprecated_int96_timestamps=self._use_deprecated_int96_timestamps,
        )

    def write_record(self, writer, value):
        if len(self._buffer[0]) >= self._buffer_size:
            self._flush_buffer()

        if self._record_batches_byte_size >= self._row_group_buffer_size:
            self._write_batches(writer)

        # reorder the data in columnar format.
        for i, n in enumerate(self._schema.names):
            self._buffer[i].append(value[n])

    def close(self, writer):
        if len(self._buffer[0]) > 0:
            self._flush_buffer()
        if self._record_batches_byte_size > 0:
            self._write_batches(writer)

        writer.close()
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

    def display_data(self):
        res = super(_ParquetSink, self).display_data()
        res["codec"] = str(self._codec)
        res["schema"] = str(self._schema)
        res["row_group_buffer_size"] = str(self._row_group_buffer_size)
        return res

    def _write_batches(self, writer):
        table = pa.Table.from_batches(self._record_batches)
        self._record_batches = []
        self._record_batches_byte_size = 0
        writer.write_table(table)

    def _flush_buffer(self):
        arrays = [[] for _ in range(len(self._schema.names))]
        for x, y in enumerate(self._buffer):
            arrays[x] = pa.array(y, type=self._schema.types[x])
            self._buffer[x] = []
        rb = pa.RecordBatch.from_arrays(arrays, self._schema.names)
        self._record_batches.append(rb)
        size = 0
        for x in arrays:
            for b in x.buffers():
                if b is not None:  # only this line is different
                    size = size + b.size
        self._record_batches_byte_size = self._record_batches_byte_size + size
