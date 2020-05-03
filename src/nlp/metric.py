# coding=utf-8
# Copyright 2020 The HuggingFace NLP Authors
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
""" Metrics base class."""
import os
import logging
from typing import Optional
from filelock import FileLock, Timeout

import pyarrow as pa

from .arrow_writer import ArrowWriter
from .arrow_reader import ArrowReader
from .utils import convert_tuples_in_lists


logger = logging.getLogger(__file__)


class Metric(object):
    name: str = 'unknown-metric'

    def __init__(self, node_id: int = 0, data_dir: Optional[str] = None, experiment_id: Optional[str] = None, in_memory=False, arrow_schema=None, **kwargs):
        """ A Metrics is the base class and common API for all metrics.
            Args:
                node_id (int): specify the id of the node in a distributed settings between 0 and num_nodes-1
                    This can be used, to compute metrics on distributed setups
                    (in particular non-additive metrics like F1).
                data_dir (str): path to a directory in which temporary data will be stored.
                    This should be a shared file-system for distributed setups.
                experiment_id (str): Should be used if you perform several concurrent experiments using
                    the same caching directory (will be indicated in the raise error)
                in_memory (bool): keep all predictions and references in memory. Not possible in distributed settings.
        """
        assert isinstance(node_id, int) and node_id >= 0, "'node_id' should a number between 0 and num_nodes-1"
        assert node_id == 0 or not in_memory, "Using 'in_memory' is not possible in distributed setting (node_id > 0)."
        self.node_id = node_id
        self.in_memory = in_memory
        self.experiment_id = experiment_id if experiment_id is not None else "cache"
        self.data_dir = data_dir

        self.arrow_schema = arrow_schema
        self.buf_writer = None
        self.writer = None
        self.writer_batch_size = None
        self.data = None

        # Check we can write on the cache file without competitors
        self.cache_file_name = os.path.join(self.data_dir, self._get_file_name(self.node_id))
        self.filelock = FileLock(self.cache_file_name)
        try:
            self.filelock.acquire(timeout=1)
        except Timeout:
            raise ValueError("Cannot acquire lock, caching file might be used by another process, "
                             "you should setup a unique 'experiment_id' for this run.")

    def _get_file_name(self, node_id):
        return f"{self.experiment_id}-{self.name}-{node_id}.arrow"

    def finalize(self, num_nodes, timeout=120):
        """ Close all the writing process and load/gather the data from all the nodes. """
        self.writer.finalize()
        self.filelock.release()

        # Let's acquire a lock on each node files to be sure they have finished writing
        node_files = []
        locks = []
        for node_id in range(num_nodes):
            node_file = self._get_file_name(node_id)
            filelock = FileLock(node_file)
            filelock.acquire(timeout=timeout)
            node_files.append(node_file)
            locks.append(filelock)

        # Read the predictions and references
        reader = ArrowReader(path=self.data_dir, info=None)
        self.data = reader.read_files(node_files)

        # Release all of our locks
        for lock in locks:
            lock.release()

    def compute(self, predictions=None, references=None, num_nodes=1, **kwargs):
        """ We add predictions and references to our stack. """
        if predictions is not None:
            self.add(predictions=predictions, references=references)
        if num_nodes-1 < self.node_id:
            raise ValueError(f"'num_node' should be the total number of nodes used in distributed setup and "
                             f"cannot be less than self.node_id + 1. Currently num_node={num_nodes} and self.node_id={self.node_id}")
        self.finalize(num_nodes)
        self._compute(self.data['predictions'], self.data['references'], **kwargs)

    def add(self, predictions=None, references=None, **kwargs):
        """ Add predictions and references for the metric """
        batch = {'predictions': predictions, 'references': references}
        if self.writer is None:
            if self.arrow_schema is None:
                batch = convert_tuples_in_lists(batch)
                self.arrow_schema = pa.Table.from_pydict(batch).schema
            if self.in_memory:
                self.buf_writer = pa.BufferOutputStream()
                self.writer = ArrowWriter(schema=self.arrow_schema, stream=self.buf_writer, writer_batch_size=self.writer_batch_size)
            else:
                self.buf_writer = None
                self.writer = ArrowWriter(schema=self.arrow_schema, path=self.cache_file_name, writer_batch_size=self.writer_batch_size)

        self.writer.write_batch(batch)

    def _compute(self, predictions=None, references=None, **kwargs):
        """ This method defines the common API for all the metrics in the library """
        raise NotImplementedError
