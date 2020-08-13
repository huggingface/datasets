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
import logging
import os
import types
from contextlib import contextmanager
from typing import Any, Dict, Optional

import numpy as np
import pyarrow as pa
from filelock import FileLock, Timeout

from .arrow_dataset import Dataset
from .arrow_reader import ArrowReader
from .arrow_writer import ArrowWriter
from .info import MetricInfo
from .naming import camelcase_to_snakecase
from .utils import HF_METRICS_CACHE, Version, copyfunc
from .utils.download_manager import DownloadManager
from .utils.file_utils import DownloadConfig


logger = logging.getLogger(__file__)


@contextmanager
def temp_seed(seed: int):
    state = np.random.get_state()
    np.random.seed(seed)
    try:
        yield
    finally:
        np.random.set_state(state)


class Metric(object):
    def __init__(
        self,
        name: str = None,
        experiment_id: Optional[str] = None,
        process_id: int = 0,
        num_process: int = 1,
        data_dir: Optional[str] = None,
        in_memory: bool = False,
        hash: str = None,
        seed: Optional[int] = None,
        **kwargs,
    ):
        """ A Metrics is the base class and common API for all metrics.
            Args:
                process_id (``int``): specify the id of the node in a distributed settings between 0 and num_nodes-1
                    This can be used, to compute metrics on distributed setups
                    (in particular non-additive metrics like F1).
                data_dir (``str``): path to a directory in which temporary data will be stored.
                    This should be a shared file-system for distributed setups.
                hash (``str``): can be used to define a hash specific to the metrics computation script
                    This prevents the metric's data to be overridden when the metric loading script is modified.
                experiment_id (Optional ``str``): Should be used if you perform several concurrent experiments using
                    the same caching directory (will be indicated in the raise error)
                in_memory (``bool``): keep all predictions and references in memory. Not possible in distributed settings.
                seed (Optional ``int``): If specified, this will temporarily set numpy's random seed when :func:`nlp.Metric.compute` is run.
        """
        # Safety checks
        assert isinstance(process_id, int) and process_id >= 0, "'process_id' should be a number greater than 0"
        assert (
            isinstance(num_process, int) and num_process > process_id
        ), "'num_process' should be a number greater than process_id"
        assert (
            process_id == 0 or not in_memory
        ), "Using 'in_memory' is not possible in distributed setting (process_id > 0)."

        # Metric name
        self.name = camelcase_to_snakecase(self.__class__.__name__)
        # Configuration name
        self.config_name: str = name or "default"

        self.process_id = process_id
        self.num_process = num_process
        self.in_memory = in_memory
        self.experiment_id = experiment_id if experiment_id is not None else "cache"
        self.hash = hash
        self._version = "1.0.0"
        self._data_dir_root = os.path.expanduser(data_dir or HF_METRICS_CACHE)
        self.data_dir = self._build_data_dir()
        self.seed: int = seed or np.random.get_state()[1][0]

        # prepare info
        info = self._info()
        info.metric_name = self.name
        info.config_name = self.config_name
        info.version = self._version
        self.info = info

        # Update 'compute' and 'add' docstring
        # methods need to be copied otherwise it changes the docstrings of every instance
        self.compute = types.MethodType(copyfunc(self.compute), self)
        self.add_batch = types.MethodType(copyfunc(self.add_batch), self)
        self.add = types.MethodType(copyfunc(self.add), self)
        self.compute.__func__.__doc__ += self.info.inputs_description
        self.add_batch.__func__.__doc__ += self.info.inputs_description
        self.add.__func__.__doc__ += self.info.inputs_description

        self.arrow_schema = pa.schema(field for field in self.info.features.type)
        self.buf_writer = None
        self.writer = None
        self.writer_batch_size = None
        self.data = None

        # Check we can write on the cache file without competitors
        self.cache_file_name = self._get_cache_path(self.process_id)
        self.filelock = FileLock(self.cache_file_name + ".lock")
        try:
            self.filelock.acquire(timeout=1)
        except Timeout:
            raise ValueError(
                "Cannot acquire lock, caching file might be used by another process, "
                "you should setup a unique 'experiment_id' for this run."
            )

    def _relative_data_dir(self, with_version=True):
        """ Relative path of this metric in cache_dir:
            Will be:
                self.name/self.config_name/self.config.version/self.hash/
            If any of these element is missing or if ``with_version=False`` the corresponding subfolders are dropped.
        """
        builder_data_dir = os.path.join(self.name, self.config_name)
        if with_version:
            builder_data_dir = os.path.join(builder_data_dir, str(self._version))
        if self.hash:
            builder_data_dir = os.path.join(builder_data_dir, self.hash)
        return builder_data_dir

    def _build_data_dir(self):
        """ Return the directory for the current version.
        """
        builder_data_dir = os.path.join(self._data_dir_root, self._relative_data_dir(with_version=False))
        version_data_dir = os.path.join(self._data_dir_root, self._relative_data_dir(with_version=True))

        def _other_versions_on_disk():
            """Returns previous versions on disk."""
            if not os.path.exists(builder_data_dir):
                return []

            version_dirnames = []
            for dir_name in os.listdir(builder_data_dir):
                try:
                    version_dirnames.append((Version(dir_name), dir_name))
                except ValueError:  # Invalid version (ex: incomplete data dir)
                    pass
            version_dirnames.sort(reverse=True)
            return version_dirnames

        # Check and warn if other versions exist on disk
        version_dirs = _other_versions_on_disk()
        if version_dirs:
            other_version = version_dirs[0][0]
            if other_version != self._version:
                warn_msg = (
                    "Found a different version {other_version} of metric {name} in "
                    "data_dir {data_dir}. Using currently defined version "
                    "{cur_version}.".format(
                        other_version=str(other_version),
                        name=self.name,
                        data_dir=self._data_dir_root,
                        cur_version=str(self._version),
                    )
                )
                logger.warning(warn_msg)

        os.makedirs(version_data_dir, exist_ok=True)
        return version_data_dir

    def _get_cache_path(self, node_id):
        return os.path.join(self.data_dir, f"{self.experiment_id}-{self.name}-{node_id}.arrow")

    def finalize(self, timeout=120):
        """ Close all the writing process and load/gather the data
            from all the nodes if main node or all_process is True.
        """
        self.writer.finalize()
        self.writer = None
        self.buf_writer = None
        self.filelock.release()

        if self.process_id == 0:
            # Let's acquire a lock on each node files to be sure they are finished writing
            node_files = []
            locks = []
            for node_id in range(self.num_process):
                node_file = self._get_cache_path(node_id)
                filelock = FileLock(node_file + ".lock")
                filelock.acquire(timeout=timeout)
                node_files.append({"filename": node_file})
                locks.append(filelock)

            # Read the predictions and references
            reader = ArrowReader(path=self.data_dir, info=None)
            self.data = Dataset(**reader.read_files(node_files))

            # Release all of our locks
            for lock in locks:
                lock.release()

    def compute(self, predictions=None, references=None, timeout=120, **metrics_kwargs):
        """ Compute the metrics.
        """
        if predictions is not None:
            self.add_batch(predictions=predictions, references=references)
        self.finalize(timeout=timeout)

        self.data.set_format(type=self.info.format)

        predictions = self.data["predictions"]
        references = self.data["references"]
        with temp_seed(self.seed):
            output = self._compute(predictions=predictions, references=references, **metrics_kwargs)
        return output

    def add_batch(self, predictions=None, references=None, **kwargs):
        """ Add a batch of predictions and references for the metric's stack.
        """
        batch = {"predictions": predictions, "references": references}
        if self.writer is None:
            self._init_writer()
        self.writer.write_batch(batch)

    def add(self, prediction=None, reference=None, **kwargs):
        """ Add one prediction and reference for the metric's stack.
        """
        example = {"predictions": prediction, "references": reference}
        example = self.info.features.encode_example(example)
        if self.writer is None:
            self._init_writer()
        self.writer.write(example)

    def _init_writer(self):
        if self.in_memory:
            self.buf_writer = pa.BufferOutputStream()
            self.writer = ArrowWriter(
                schema=self.arrow_schema, stream=self.buf_writer, writer_batch_size=self.writer_batch_size
            )
        else:
            self.buf_writer = None
            self.writer = ArrowWriter(
                schema=self.arrow_schema, path=self.cache_file_name, writer_batch_size=self.writer_batch_size
            )

    def _info(self) -> MetricInfo:
        """Construct the MetricInfo object. See `MetricInfo` for details.

        Warning: This function is only called once and the result is cached for all
        following .info() calls.

        Returns:
            info: (MetricInfo) The metrics information
        """
        raise NotImplementedError

    def download_and_prepare(
        self,
        download_config: Optional[DownloadConfig] = None,
        dl_manager: Optional[DownloadManager] = None,
        **download_and_prepare_kwargs,
    ):
        """Downloads and prepares dataset for reading.

        Args:
            download_config (Optional ``nlp.DownloadConfig``: specific download configuration parameters.
            dl_manager (Optional ``nlp.DownloadManager``): specific Download Manger to use
        """
        if dl_manager is None:
            if download_config is None:
                download_config = DownloadConfig()
                download_config.cache_dir = os.path.join(self.data_dir, "downloads")
                download_config.force_download = False

            dl_manager = DownloadManager(
                dataset_name=self.name, download_config=download_config, data_dir=self.data_dir
            )

        self._download_and_prepare(dl_manager)

    def _download_and_prepare(self, dl_manager):
        """Downloads and prepares resources for the metric.

        This is the internal implementation to overwrite called when user calls
        `download_and_prepare`. It should download all required resources for the metric.

        Args:
            dl_manager: (DownloadManager) `DownloadManager` used to download and cache
                data..
        """
        return None

    def _compute(self, predictions=None, references=None, **kwargs) -> Dict[str, Any]:
        """ This method defines the common API for all the metrics in the library """
        raise NotImplementedError
