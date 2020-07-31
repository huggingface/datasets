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
import json
import logging
import os
import socket
from dataclasses import asdict
from typing import Any, Dict, List, Optional

import pyarrow as pa
from tqdm.auto import tqdm

from .features import Features
from .info import DatasetInfo
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
        features: Optional[Features] = None,
        path: Optional[str] = None,
        stream: Optional[pa.NativeFile] = None,
        writer_batch_size: Optional[int] = None,
        disable_nullable: bool = True,
        update_features: bool = False,
        with_metadata: bool = True,
    ):
        if path is None and stream is None:
            raise ValueError("At least one of path and stream must be provided.")
        if features is not None:
            self._features = features
            self._schema = pa.schema(features.type)
            self._type: pa.DataType = pa.struct(field for field in self._schema)
        elif data_type is not None:
            self._type: pa.DataType = data_type
            self._schema: pa.Schema = pa.schema(field for field in self._type)
            self._features = Features.from_arrow_schema(self._schema)
        elif schema is not None:
            self._schema: pa.Schema = schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)
            self._features = Features.from_arrow_schema(self._schema)
        else:
            self._features = None
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
        self.update_features = update_features
        self.with_metadata = with_metadata

        self._num_examples = 0
        self._num_bytes = 0
        self.current_rows = []
        self.pa_writer: Optional[pa.RecordBatchStreamWriter] = None

    def _build_writer(self, inferred_schema: pa.Schema):
        inferred_features = Features.from_arrow_schema(inferred_schema)
        if self._features is not None:
            if self.update_features:
                fields = {field.name: field for field in self._features.type}
                for inferred_field in inferred_features.type:
                    name = inferred_field.name
                    if name in fields:
                        if inferred_field == fields[name]:
                            inferred_features[name] = self._features[name]
                self._features = inferred_features
                self._schema: pa.Schema = inferred_schema
                self._type: pa.DataType = pa.struct(field for field in self._schema)
        else:
            self._features = inferred_features
            self._schema: pa.Schema = inferred_schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)
        if self.with_metadata:
            self._schema = self._schema.with_metadata(self._build_metadata(DatasetInfo(features=self._features)))
        self.pa_writer = pa.RecordBatchStreamWriter(self.stream, self._schema)

    @property
    def schema(self):
        return self._schema if self._schema is not None else []

    def _build_metadata(self, info) -> Dict[str, str]:
        keys = ["features"]  # we can add support for more DatasetInfo keys in the future
        info_as_dict = asdict(info)
        return {"huggingface": json.dumps({key: info_as_dict[key] for key in keys})}

    def _write_array_on_file(self, pa_array):
        """Write a PyArrow Array"""
        pa_batch = pa.RecordBatch.from_struct_array(pa_array)
        self._num_bytes += pa_array.nbytes
        if self.pa_writer is None:
            pa_table = pa.Table.from_batches([pa_batch])
            self._build_writer(inferred_schema=pa_table.schema)
        self.pa_writer.write_batch(pa_batch)

    def write_on_file(self):
        """ Write stored examples
        """
        # infer type on first write
        type = None if self.update_features and self.pa_writer is None else self._type
        if self.current_rows:
            pa_array = pa.array(self.current_rows, type=type)
            first_example = pa.array(self.current_rows[0:1], type=type)[0]
            # Sanity check
            if pa_array[0] != first_example:
                # There was an Overflow in StructArray. Let's reduce the batch_size
                while pa_array[0] != first_example:
                    new_batch_size = self.writer_batch_size // 2
                    pa_array = pa.array(self.current_rows[:new_batch_size], type=type)
                logger.warning(
                    "Batch size is too big (>2GB). Reducing it from {} to {}".format(
                        self.writer_batch_size, new_batch_size
                    )
                )
                self.writer_batch_size = new_batch_size
                n_batches = len(self.current_rows) // new_batch_size
                n_batches += int(len(self.current_rows) % new_batch_size != 0)
                for i in range(n_batches):
                    pa_array = pa.array(self.current_rows[i * new_batch_size : (i + 1) * new_batch_size], type=type,)
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
            self._build_writer(inferred_schema=pa.Table.from_pydict(batch_examples).schema)
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
            self._build_writer(inferred_schema=pa_table.schema)
        batches: List[pa.RecordBatch] = pa_table.to_batches(max_chunksize=writer_batch_size)
        self._num_bytes += sum(batch.nbytes for batch in batches)
        self._num_examples += pa_table.num_rows
        for batch in batches:
            self.pa_writer.write_batch(batch)

    def finalize(self, close_stream=True):
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
        self._parquet_path = os.path.splitext(path)[0]  # remove extension
        self._namespace = namespace or "default"
        self._num_examples = None
        self._cache_dir = cache_dir or HF_DATASETS_CACHE

    def write_from_pcollection(self, pcoll_examples):
        """Add the final steps of the beam pipeline: write to parquet files."""
        import apache_beam as beam

        def inc_num_examples(example):
            beam.metrics.Metrics.counter(self._namespace, "num_examples").inc()

        # count examples
        _ = pcoll_examples | "Count N. Examples" >> beam.Map(inc_num_examples)

        # save dataset
        simplified_schema = pa.schema({field.name: pa.string() for field in self._schema})
        return (
            pcoll_examples
            | "Get values" >> beam.Values()
            | "simplify" >> beam.Map(lambda ex: {k: json.dumps(v) for k, v in ex.items()})
            | "Save to parquet"
            >> beam.io.parquetio.WriteToParquet(
                self._parquet_path, simplified_schema, shard_name_template="-SSSSS-of-NNNNN.parquet"
            )
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
        shards = [
            metadata.path
            for metadata in beam.io.filesystems.FileSystems.match([self._parquet_path + "*.parquet"])[0].metadata_list
        ]
        try:  # stream conversion
            sources = [beam.io.filesystems.FileSystems.open(shard) for shard in shards]
            with beam.io.filesystems.FileSystems.create(self._path) as dest:
                parquet_to_arrow(sources, dest)
        except socket.error as e:  # broken pipe can happen if the connection is unstable, do local conversion instead
            if e.errno != errno.EPIPE:  # not a broken pipe
                raise e
            logger.warning("Broken Pipe during stream conversion from parquet to arrow. Using local convert instead")
            local_convert_dir = os.path.join(self._cache_dir, "beam_convert")
            os.makedirs(local_convert_dir, exist_ok=True)
            local_arrow_path = os.path.join(local_convert_dir, hash_url_to_filename(self._parquet_path) + ".arrow")
            local_shards = []
            for shard in shards:
                local_parquet_path = os.path.join(local_convert_dir, hash_url_to_filename(shard) + ".parquet")
                local_shards.append(local_parquet_path)
                beam_utils.download_remote_to_local(shard, local_parquet_path)
            parquet_to_arrow(local_shards, local_arrow_path)
            beam_utils.upload_local_to_remote(local_arrow_path, self._path)

        # Save metrics
        counters_dict = {metric.key.metric.name: metric.result for metric in metrics_query_result["counters"]}
        self._num_examples = counters_dict["num_examples"]
        output_file_metadata = beam.io.filesystems.FileSystems.match([self._path], limits=[1])[0].metadata_list[0]
        self._num_bytes = output_file_metadata.size_in_bytes
        return self._num_examples, self._num_bytes


def parquet_to_arrow(sources, destination):
    """Convert parquet files to arrow file. Inputs can be str paths or file-like objects"""
    stream = None if isinstance(destination, str) else destination
    writer = ArrowWriter(path=destination, stream=stream)
    for source in tqdm(sources, unit="sources"):
        pf = pa.parquet.ParquetFile(source)
        for i in tqdm(range(pf.num_row_groups), unit="row_groups", leave=False):
            df = pf.read_row_group(i).to_pandas()
            for col in df.columns:
                df[col] = df[col].apply(json.loads)
            reconstructed_table = pa.Table.from_pandas(df)
            writer.write_table(reconstructed_table)
    return destination
