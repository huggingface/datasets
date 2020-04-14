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
import collections
import itertools
import json
import os

from typing import Dict, List, Optional, Any

import logging

import pyarrow as pa

logger = logging.getLogger(__name__)

class ArrowWriter(object):
    """Shuffles and writes Examples to Arrow files.
    """

    def __init__(self,
                 data_type: Optional[pa.DataType] = None,
                 schema: Optional[pa.Schema] = None,
                 path: Optional[str] = None,
                 stream: Optional[pa.NativeFile] = None,
                 writer_batch_size: Optional[int] = None,
                 disable_nullable: bool = True):
        if data_type is None and schema is None:
            raise ValueError("At least one of data_type and schema must be provided.")
        if path is None and stream is None:
            raise ValueError("At least one of path and stream must be provided.")

        if data_type is not None:
            self._type: pa.DataType = data_type
            self._schema: pa.Schema = pa.schema(field for field in self._type)
        else:
            self._schema: pa.Schema = schema
            self._type: pa.DataType = pa.struct(field for field in self._schema)

        if disable_nullable:
            self._schema = pa.schema(pa.field(field.name, field.type, nullable=False) for field in self._type)
            self._type = pa.struct(pa.field(field.name, field.type, nullable=False) for field in self._type)

        self._path = path
        if stream is None:
            self.stream = pa.OSFile(self._path, 'wb')
        else:
            self.stream = stream

        self.writer = pa.RecordBatchStreamWriter(self.stream, self._schema)
        self.writer_batch_size = writer_batch_size

        self._num_examples = 0
        self._num_bytes = 0
        self.current_rows = []

    def write_on_file(self):
        """ Write stored examples
        """
        pa_array = pa.array(self.current_rows, type=self._type)
        pa_batch = pa.RecordBatch.from_struct_array(pa_array)
        self._num_bytes += pa_array.nbytes
        self.writer.write_batch(pa_batch)
        self.current_rows = []

    def write(self, example: Dict[str, Any], writer_batch_size: Optional[int] = None):
        """ Add a given Example to the write-pool which is written to file.

        Args:
            example: the Example to add.
        """
        self.current_rows.append(example)
        self._num_examples += 1
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        if writer_batch_size is not None and len(self.current_rows) >= writer_batch_size:
            self.write_on_file()

    def write_batch(self, batch_examples: Dict[str, List[Any]], writer_batch_size: Optional[int] = None):
        """ Write a batch of Example to file.

        Args:
            example: the Example to add.
        """
        pa_table: pa.Table = pa.Table.from_pydict(batch_examples, schema=self._schema)
        if writer_batch_size is None:
            writer_batch_size = self.writer_batch_size
        batches: List[pa.RecordBatch] = pa_table.to_batches(max_chunksize=writer_batch_size)
        self._num_bytes += sum(batch.nbytes for batch in batches)
        self._num_examples += pa_table.num_rows
        for batch in batches:
            self.writer.write_batch(batch)

    def finalize(self, close_stream=True):
        self.write_on_file()
        self.writer.close()
        if close_stream:
            self.stream.close()
        logger.info("Done writing %s examples in %s bytes %s.",
                    self._num_examples, self._num_bytes,
                    self._path if self._path else "")
        return self._num_examples, self._num_bytes


class BeamWriter(object):
    """Shuffles and writes Examples to Parquet files.
    """

    def __init__(self,
                 data_type: Optional[pa.DataType] = None,
                 schema: Optional[pa.Schema] = None,
                 path: Optional[str] = None,
                 stream: Optional[pa.NativeFile] = None,
                 writer_batch_size: Optional[int] = None):
        raise NotImplementedError
