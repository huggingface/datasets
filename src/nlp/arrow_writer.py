# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors and the TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""To write records into Parquet files."""
import errno
import logging
import os
import socket
from typing import Any, Dict, List, Optional

import pyarrow as pa

from .utils.file_utils import HF_DATASETS_CACHE, hash_url_to_filename
from .utils.py_utils import map_all_sequences_to_lists


logger = logging.getLogger(__name__)

# Batch size constants. For more info, see:
# https://github.com/apache/arrow/blob/master/docs/source/cpp/arrays.rst#size-limitations-and-recommendations)
DEFAULT_MAX_BATCH_SIZE = 10_000  # hopefully it doesn't write too much at once (max is 2GB)


class ArrowWriter(object):
    """Shuffles and writes Examples to Arrow files.
    """

    def __init__(
        self,
        data_type: Optional[pa.DataType] = None,
        schema: Optional[pa.Schema] = None,
        path: Optional[str] = None,
        stream: Optional[pa.NativeFile] = None,
        writer_batch_size: Optional[int] = None,
        disable_nullable: bool = True,
    ):
        if path is None and stream is None:
            raise ValueError("At least one of path and stream must be provided.")

        if data_type is not None:
            self._type: pa.DataType = data_type
            self._schema: pa.Schema = pa.schema(field for field in self._type)
        elif schema is not None:
            self._schema: pa.Schema = schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)
        else:
            self._schema = None
            self._type = None

        if disable_nullable and self._schema is not None:
            self._schema = pa.schema(pa.field(field.name, field.type, nullable=False) for field in self._type)
            self._type = pa.struct(pa.field(field.name, field.type, nullable=False) for field in self._type)

        self._path = path
        if stream is None:
            self.stream = pa.OSFile(self._path, "wb")
        else:
            self.stream = stream

        self.writer_batch_size = writer_batch_size or DEFAULT_MAX_BATCH_SIZE

        self._num_examples = 0
        self._num_bytes = 0
        self.current_rows = []

        self._build_writer(schema=self._schema)

    def _build_writer(self, pa_table=None, schema=None):
        if schema is not None:
            self._schema: pa.Schema = schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)
            self.pa_writer = pa.RecordBatchStreamWriter(self.stream, schema)
        elif pa_table is not None:
            self._schema: pa.Schema = pa_table.schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)
            self.pa_writer = pa.RecordBatchStreamWriter(self.stream, self._schema)
        else:
            self.pa_writer = None

    @property
    def schema(self):
        return self._schema if self._schema is not None else []

    def _write_array_on_file(self, pa_array):
        """Write a PyArrow Array"""
        pa_batch = pa.RecordBatch.from_struct_array(pa_array)
        self._num_bytes += pa_array.nbytes
        self.pa_writer.write_batch(pa_batch)

    def write_on_file(self):
        """ Write stored examples
        """
        if self.current_rows:
            pa_array = pa.array(self.current_rows, type=self._type)
            first_example = pa.array(self.current_rows[0:1], type=self._type)[0]
            # Sanity check
            if pa_array[0] != first_example:
                # There was an Overflow in StructArray. Let's reduce the batch_size
                while pa_array[0] != first_example:
                    new_batch_size = self.writer_batch_size // 2
                    pa_array = pa.array(self.current_rows[:new_batch_size], type=self._type)
                logger.warning(
                    "Batch size is too big (>2GB). Reducing it from {} to {}".format(
                        self.writer_batch_size, new_batch_size
                    )
                )
                self.writer_batch_size = new_batch_size
                n_batches = len(self.current_rows) // new_batch_size
                n_batches += int(len(self.current_rows) % new_batch_size != 0)
                for i in range(n_batches):
                    pa_array = pa.array(
                        self.current_rows[i * new_batch_size : (i + 1) * new_batch_size], type=self._type,
                    )
                    self._write_array_on_file(pa_array)
            else:
                # All good
                self._write_array_on_file(pa_array)
            self.current_rows = []

    def write(self, example: Dict[str, Any], writer_batch_size: Optional[int] = None):
        """ Add a given Example to the write-pool which is written to file.

        Args:
            example: the Example to add.
        """
        example = map_all_sequences_to_lists(example)
        self.current_rows.append(example)
        self._num_examples += 1
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if self.pa_writer is None:
            self._build_writer(pa_table=pa.Table.from_pydict(example))
        if writer_batch_size is not None and len(self.current_rows) >= writer_batch_size:
            self.write_on_file()

    def write_batch(
        self, batch_examples: Dict[str, List[Any]], writer_batch_size: Optional[int] = None,
    ):
        """ Write a batch of Example to file.

        Args:
            example: the Example to add.
        """
        batch_examples = map_all_sequences_to_lists(batch_examples)
        if self.pa_writer is None:
            self._build_writer(pa_table=pa.Table.from_pydict(batch_examples))
        pa_table: pa.Table = pa.Table.from_pydict(batch_examples, schema=self._schema)
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        batches: List[pa.RecordBatch] = pa_table.to_batches(max_chunksize=writer_batch_size)
        self._num_bytes += sum(batch.nbytes for batch in batches)
        self._num_examples += pa_table.num_rows
        for batch in batches:
            self.pa_writer.write_batch(batch)

    def write_table(self, pa_table: pa.Table, writer_batch_size: Optional[int] = None):
        """ Write a batch of Example to file.

        Args:
            example: the Example to add.
        """
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if self.pa_writer is None:
            self._build_writer(pa_table=pa_table)
        batches: List[pa.RecordBatch] = pa_table.to_batches(max_chunksize=writer_batch_size)
        self._num_bytes += sum(batch.nbytes for batch in batches)
        self._num_examples += pa_table.num_rows
        for batch in batches:
            self.pa_writer.write_batch(batch)

    def finalize(self, close_stream=True):
        if self.pa_writer is not None:
            self.write_on_file()
            self.pa_writer.close()
        if close_stream:
            self.stream.close()
        logger.info(
            "Done writing %s examples in %s bytes %s.",
            self._num_examples,
            self._num_bytes,
            self._path if self._path else "",
        )
        return self._num_examples, self._num_bytes


class BeamWriter(object):
    """
    Shuffles and writes Examples to Arrow files.
    The Arrow files are converted from Parquet files that are the output of Apache Beam pipelines.
    """

    def __init__(
        self,
        data_type: Optional[pa.DataType] = None,
        schema: Optional[pa.Schema] = None,
        path: Optional[str] = None,
        namespace: Optional[str] = None,
        cache_dir: Optional[str] = None,
    ):
        if data_type is None and schema is None:
            raise ValueError("At least one of data_type and schema must be provided.")
        if path is None:
            raise ValueError("Path must be provided.")

        if data_type is not None:
            self._type: pa.DataType = data_type
            self._schema: pa.Schema = pa.schema(field for field in self._type)
        else:
            self._schema: pa.Schema = schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)

        self._path = path
        self._parquet_path = os.path.splitext(path)[0] + ".parquet"
        self._namespace = namespace or "default"
        self._num_examples = None
        self._cache_dir = cache_dir or HF_DATASETS_CACHE

    def write_from_pcollection(self, pcoll_examples):
        """Add the final steps of the beam pipeline: write to parquet files."""
        import apache_beam as beam
        from .utils.beam_utils import WriteToParquet

        def inc_num_examples(example):
            beam.metrics.Metrics.counter(self._namespace, "num_examples").inc()

        # count examples
        _ = pcoll_examples | "Count N. Examples" >> beam.Map(inc_num_examples)

        # save dataset
        return (
            pcoll_examples
            | "Get values" >> beam.Values()
            | "Save to parquet"
            >> WriteToParquet(self._parquet_path, self._schema, num_shards=1, shard_name_template="")
        )

    def finalize(self, metrics_query_result: dict):
        """
        Run after the pipeline has finished.
        It converts the resulting parquet files to arrow and it completes the info from the pipeline metrics.

        Args:
            metrics_query_result: `dict` obtained from pipeline_results.metrics().query(m_filter). Make sure
                that the filter keeps only the metrics for the considered split, under the namespace `split_name`.
        """
        import apache_beam as beam
        from .utils import beam_utils

        # Convert to arrow
        logger.info("Converting parquet file {} to arrow {}".format(self._parquet_path, self._path))
        try:  # stream conversion
            with beam.io.filesystems.FileSystems.open(self._parquet_path) as src:
                with beam.io.filesystems.FileSystems.create(self._path) as dest:
                    parquet_to_arrow(src, dest)
        except socket.error as e:  # broken pipe can happen if the connection is unstable, do local conversion instead
            if e.errno != errno.EPIPE:  # not a broken pipe
                raise e
            logger.warning("Broken Pipe during stream conversion from parquet to arrow. Using local convert instead")
            local_convert_dir = os.path.join(self._cache_dir, "beam_convert")
            os.makedirs(local_convert_dir, exist_ok=True)
            local_parquet_path = os.path.join(local_convert_dir, hash_url_to_filename(self._parquet_path) + ".parquet")
            local_arrow_path = os.path.splitext(local_parquet_path)[0] + ".arrow"
            beam_utils.download_remote_to_local(self._parquet_path, local_parquet_path)
            parquet_to_arrow(local_parquet_path, local_arrow_path)
            beam_utils.upload_local_to_remote(local_arrow_path, self._path)

        # Save metrics
        counters_dict = {metric.key.metric.name: metric.result for metric in metrics_query_result["counters"]}
        self._num_examples = counters_dict["num_examples"]
        output_file_metadata = beam.io.filesystems.FileSystems.match([self._path], limits=[1])[0].metadata_list[0]
        self._num_bytes = output_file_metadata.size_in_bytes
        return self._num_examples, self._num_bytes


def parquet_to_arrow(source, destination):
    """Convert parquet file to arrow file. Inputs can be str paths or file-like objects"""
    pf = pa.parquet.ParquetFile(source)
    stream = None if isinstance(destination, str) else destination
    writer = ArrowWriter(path=destination, stream=stream)
    for i in range(pf.num_row_groups):
        row_group_table = pf.read_row_group(i)
        writer.write_table(row_group_table)
    return destination
