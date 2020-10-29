# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors
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
import types
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pyarrow as pa
from filelock import BaseFileLock, FileLock, Timeout

from .arrow_dataset import Dataset
from .arrow_reader import ArrowReader
from .arrow_writer import ArrowWriter
from .features import Features
from .info import DatasetInfo, MetricInfo
from .naming import camelcase_to_snakecase
from .utils import HF_METRICS_CACHE, copyfunc, temp_seed
from .utils.download_manager import DownloadManager
from .utils.file_utils import DownloadConfig
from .utils.logging import get_logger


logger = get_logger(__file__)


class FileFreeLock(BaseFileLock):
    """Thread lock until a file **cannot** be locked"""

    def __init__(self, lock_file, *args, **kwargs):
        self.filelock = FileLock(lock_file)
        super().__init__(lock_file, *args, **kwargs)

    def _acquire(self):
        try:
            self.filelock.acquire(timeout=0.01, poll_intervall=0.02)  # Try to lock once
        except Timeout:
            # We couldn't acquire the lock, the file is locked!
            self._lock_file_fd = self.filelock.lock_file
        else:
            # We were able to acquire the lock, the file is not yet locked!
            self.filelock.release()
            self._lock_file_fd = None

    def _release(self):
        self._lock_file_fd = None


class MetricInfoMixin(object):
    """This base class exposes some attributes of MetricInfo
    at the base level of the Metric for easy access.
    """

    def __init__(self, info: MetricInfo):
        self._metric_info = info

    @property
    def info(self):
        """ :class:`datasets.MetricInfo` object containing all the metadata in the metric."""
        return self._metric_info

    @property
    def name(self) -> str:
        return self._metric_info.metric_name

    @property
    def experiment_id(self) -> Optional[str]:
        return self._metric_info.experiment_id

    @property
    def description(self) -> str:
        return self._metric_info.description

    @property
    def citation(self) -> str:
        return self._metric_info.citation

    @property
    def features(self) -> Features:
        return self._metric_info.features

    @property
    def inputs_description(self) -> str:
        return self._metric_info.inputs_description

    @property
    def homepage(self) -> Optional[str]:
        return self._metric_info.homepage

    @property
    def license(self) -> str:
        return self._metric_info.license

    @property
    def codebase_urls(self) -> Optional[List[str]]:
        return self._metric_info.codebase_urls

    @property
    def reference_urls(self) -> Optional[List[str]]:
        return self._metric_info.reference_urls

    @property
    def streamable(self) -> bool:
        return self._metric_info.streamable

    @property
    def format(self) -> Optional[str]:
        return self._metric_info.format


class Metric(MetricInfoMixin):
    """A Metrics is the base class and common API for all metrics.

    Args:
        config_name (``str``): This is used to define a hash specific to a metrics computation script and prevents the metric's data
            to be overridden when the metric loading script is modified.
        keep_in_memory (``bool``): keep all predictions and references in memory. Not possible in distributed settings.
        cache_dir (``str``): Path to a directory in which temporary prediction/references data will be stored.
            The data directory should be located on a shared file-system in distributed setups.
        num_process (``int``): specify the total number of nodes in a distributed settings.
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        process_id (``int``): specify the id of the current process in a distributed setup (between 0 and num_process-1)
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        seed (Optional ``int``): If specified, this will temporarily set numpy's random seed when :func:`datasets.Metric.compute` is run.
        experiment_id (``str``): A specific experiment id. This is used if several distributed evaluations share the same file system.
            This is useful to compute metrics in distributed setups (in particular non-additive metrics like F1).
        max_concurrent_cache_files (``int``): Max number of concurrent metrics cache files (default 10000).
        timeout (``Union[int, float]``): Timeout in second for distributed setting synchronization.
    """

    def __init__(
        self,
        config_name: Optional[str] = None,
        keep_in_memory: bool = False,
        cache_dir: Optional[str] = None,
        num_process: int = 1,
        process_id: int = 0,
        seed: Optional[int] = None,
        experiment_id: Optional[str] = None,
        max_concurrent_cache_files: int = 10000,
        timeout: Union[int, float] = 100,
        **kwargs,
    ):
        # prepare info
        self.config_name = config_name or "default"
        info = self._info()
        info.metric_name = camelcase_to_snakecase(self.__class__.__name__)
        info.config_name = self.config_name
        info.experiment_id = experiment_id or "default_experiment"
        MetricInfoMixin.__init__(self, info)  # For easy access on low level

        # Safety checks on num_process and process_id
        assert isinstance(process_id, int) and process_id >= 0, "'process_id' should be a number greater than 0"
        assert (
            isinstance(num_process, int) and num_process > process_id
        ), "'num_process' should be a number greater than process_id"
        assert (
            num_process == 1 or not keep_in_memory
        ), "Using 'keep_in_memory' is not possible in distributed setting (num_process > 1)."
        self.num_process = num_process
        self.process_id = process_id
        self.max_concurrent_cache_files = max_concurrent_cache_files

        self.keep_in_memory = keep_in_memory
        self._data_dir_root = os.path.expanduser(cache_dir or HF_METRICS_CACHE)
        self.data_dir = self._build_data_dir()
        self.seed: int = seed or np.random.get_state()[1][0]
        self.timeout: Union[int, float] = timeout

        # Update 'compute' and 'add' docstring
        # methods need to be copied otherwise it changes the docstrings of every instance
        self.compute = types.MethodType(copyfunc(self.compute), self)
        self.add_batch = types.MethodType(copyfunc(self.add_batch), self)
        self.add = types.MethodType(copyfunc(self.add), self)
        self.compute.__func__.__doc__ += self.info.inputs_description
        self.add_batch.__func__.__doc__ += self.info.inputs_description
        self.add.__func__.__doc__ += self.info.inputs_description

        # self.arrow_schema = pa.schema(field for field in self.info.features.type)
        self.buf_writer = None
        self.writer = None
        self.writer_batch_size = None
        self.data = None

        # This is the cache file we store our predictions/references in
        # Keep it None for now so we can (cloud)pickle the object
        self.cache_file_name = None
        self.filelock = None
        self.rendez_vous_lock = None

        # This is all the cache files on which we have a lock when we are in a distributed setting
        self.file_paths = None
        self.filelocks = None

    def __len__(self):
        """Return the number of examples (predictions or predictions/references pair)
        currently stored in the metric's cache.
        """
        return 0 if self.writer is None else len(self.writer)

    def __repr__(self):
        return (
            f'Metric(name: "{self.name}", features: {self.features}, '
            f'usage: """{self.inputs_description}""", '
            f"stored examples: {len(self)})"
        )

    def _build_data_dir(self):
        """Path of this metric in cache_dir:
        Will be:
            self._data_dir_root/self.name/self.config_name/self.hash (if not none)/
        If any of these element is missing or if ``with_version=False`` the corresponding subfolders are dropped.
        """
        builder_data_dir = self._data_dir_root
        builder_data_dir = os.path.join(builder_data_dir, self.name, self.config_name)
        os.makedirs(builder_data_dir, exist_ok=True)
        return builder_data_dir

    def _create_cache_file(self, timeout=1) -> Tuple[str, FileLock]:
        """ Create a new cache file. If the default cache file is used, we generated a new hash. """
        file_path = os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-{self.process_id}.arrow")
        filelock = None
        for i in range(self.max_concurrent_cache_files):
            filelock = FileLock(file_path + ".lock")
            try:
                filelock.acquire(timeout=timeout)
            except Timeout:
                # If we have reached the max number of attempts or we are not allow to find a free name (distributed setup)
                # We raise an error
                if self.num_process != 1:
                    raise ValueError(
                        f"Error in _create_cache_file: another metric instance is already using the local cache file at {file_path}. "
                        f"Please specify an experiment_id (currently: {self.experiment_id}) to avoid colision "
                        f"between distributed metric instances."
                    )
                if i == self.max_concurrent_cache_files - 1:
                    raise ValueError(
                        f"Cannot acquire lock, too many metric instance are operating concurrently on this file system."
                        f"You should set a larger value of max_concurrent_cache_files when creating the metric "
                        f"(current value is {self.max_concurrent_cache_files})."
                    )
                # In other cases (allow to find new file name + not yet at max num of attempts) we can try to sample a new hashing name.
                file_uuid = str(uuid.uuid4())
                file_path = os.path.join(
                    self.data_dir, f"{self.experiment_id}-{file_uuid}-{self.num_process}-{self.process_id}.arrow"
                )
            else:
                break

        return file_path, filelock

    def _get_all_cache_files(self) -> Tuple[List[str], List[FileLock]]:
        """Get a lock on all the cache files in a distributed setup.
        We wait for timeout second to let all the distributed node finish their tasks (default is 100 seconds).
        """
        if self.num_process == 1:
            file_paths = [self.cache_file_name]
        else:
            file_paths = [
                os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-{process_id}.arrow")
                for process_id in range(self.num_process)
            ]

        # Let's acquire a lock on each process files to be sure they are finished writing
        filelocks = []
        for process_id, file_path in enumerate(file_paths):
            filelock = FileLock(file_path + ".lock")
            try:
                filelock.acquire(timeout=self.timeout)
            except Timeout:
                raise ValueError(f"Cannot acquire lock on cached file {file_path} for process {process_id}.")
            else:
                filelocks.append(filelock)

        return file_paths, filelocks

    def _check_all_processes_locks(self):
        expected_lock_file_names = [
            os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-{process_id}.arrow.lock")
            for process_id in range(self.num_process)
        ]
        for expected_lock_file_name in expected_lock_file_names:
            nofilelock = FileFreeLock(expected_lock_file_name)
            try:
                nofilelock.acquire(timeout=self.timeout)
            except Timeout:
                raise ValueError(
                    f"Expected to find locked file {expected_lock_file_name} from process {self.process_id} but it doesn't exist."
                )
            else:
                nofilelock.release()

    def _check_rendez_vous(self):
        expected_lock_file_name = os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-0.arrow.lock")
        nofilelock = FileFreeLock(expected_lock_file_name)
        try:
            nofilelock.acquire(timeout=self.timeout)
        except Timeout:
            raise ValueError(
                f"Expected to find locked file {expected_lock_file_name} from process {self.process_id} but it doesn't exist."
            )
        else:
            nofilelock.release()
        lock_file_name = os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-rdv.lock")
        rendez_vous_lock = FileLock(lock_file_name)
        try:
            rendez_vous_lock.acquire(timeout=self.timeout)
        except Timeout:
            raise ValueError(f"Couldn't acquire lock on {lock_file_name} from process {self.process_id}.")
        else:
            rendez_vous_lock.release()

    def _finalize(self):
        """Close all the writing process and load/gather the data
        from all the nodes if main node or all_process is True.
        """
        if self.writer is not None:
            self.writer.finalize()
        self.writer = None
        if self.filelock is not None:
            self.filelock.release()

        if self.keep_in_memory:
            # Read the predictions and references
            reader = ArrowReader(path=self.data_dir, info=DatasetInfo(features=self.features))
            self.data = Dataset.from_buffer(self.buf_writer.getvalue())

        elif self.process_id == 0:
            # Let's acquire a lock on each node files to be sure they are finished writing
            file_paths, filelocks = self._get_all_cache_files()

            # Read the predictions and references
            try:
                reader = ArrowReader(path="", info=DatasetInfo(features=self.features))
                self.data = Dataset(**reader.read_files([{"filename": f} for f in file_paths]))
            except FileNotFoundError:
                raise ValueError(
                    "Error in finalize: another metric instance is already using the local cache file. "
                    "Please specify an experiment_id to avoid colision between distributed metric instances."
                )

            # Store file paths and locks and we will release/delete them after the computation.
            self.file_paths = file_paths
            self.filelocks = filelocks

    def compute(self, *args, **kwargs) -> Optional[dict]:
        """Compute the metrics.

        Args:
            We disallow the usage of positional arguments to prevent mistakes
            `predictions` (Optional list/array/tensor): predictions
            `references` (Optional list/array/tensor): references
            `**kwargs` (Optional other kwargs): will be forwared to the metrics :func:`_compute` method (see details in the docstring)

        Return:
            Dictionnary with the metrics if this metric is run on the main process (process_id == 0)
            None if the metric is not run on the main process (process_id != 0)
        """
        if args:
            raise ValueError("Please call `compute` using keyword arguments.")

        predictions = kwargs.pop("predictions", None)
        references = kwargs.pop("references", None)

        if predictions is not None:
            self.add_batch(predictions=predictions, references=references)
        self._finalize()

        self.cache_file_name = None
        self.filelock = None

        if self.process_id == 0:
            self.data.set_format(type=self.info.format)

            predictions = self.data["predictions"]
            references = self.data["references"]
            with temp_seed(self.seed):
                output = self._compute(predictions=predictions, references=references, **kwargs)

            if self.buf_writer is not None:
                self.buf_writer = None
                del self.data
                self.data = None
            else:
                # Release locks and delete all the cache files
                for filelock, file_path in zip(self.filelocks, self.file_paths):
                    logger.info(f"Removing {file_path}")
                    del self.data
                    self.data = None
                    del self.writer
                    self.writer = None
                    os.remove(file_path)
                    filelock.release()

            return output
        else:
            return None

    def add_batch(self, *, predictions=None, references=None):
        """
        Add a batch of predictions and references for the metric's stack.
        """
        batch = {"predictions": predictions, "references": references}
        batch = self.info.features.encode_batch(batch)
        if self.writer is None:
            self._init_writer()
        try:
            self.writer.write_batch(batch)
        except pa.ArrowInvalid:
            raise ValueError(
                f"Predictions and/or references don't match the expected format.\n"
                f"Expected format: {self.features},\n"
                f"Input predictions: {predictions},\n"
                f"Input references: {references}"
            )

    def add(self, *, prediction=None, reference=None):
        """Add one prediction and reference for the metric's stack."""
        example = {"predictions": prediction, "references": reference}
        example = self.info.features.encode_example(example)
        if self.writer is None:
            self._init_writer()
        try:
            self.writer.write(example)
        except pa.ArrowInvalid:
            raise ValueError(
                f"Prediction and/or reference don't match the expected format.\n"
                f"Expected format: {self.features},\n"
                f"Input predictions: {prediction},\n"
                f"Input references: {reference}"
            )

    def _init_writer(self, timeout=1):
        if self.num_process > 1:
            if self.process_id == 0:
                file_path = os.path.join(self.data_dir, f"{self.experiment_id}-{self.num_process}-rdv.lock")
                self.rendez_vous_lock = FileLock(file_path)
                try:
                    self.rendez_vous_lock.acquire(timeout=timeout)
                except TimeoutError:
                    raise ValueError(
                        f"Error in _init_writer: another metric instance is already using the local cache file at {file_path}. "
                        f"Please specify an experiment_id (currently: {self.experiment_id}) to avoid colision "
                        f"between distributed metric instances."
                    )

        if self.keep_in_memory:
            self.buf_writer = pa.BufferOutputStream()
            self.writer = ArrowWriter(
                features=self.info.features, stream=self.buf_writer, writer_batch_size=self.writer_batch_size
            )
        else:
            self.buf_writer = None

            # Get cache file name and lock it
            if self.cache_file_name is None or self.filelock is None:
                cache_file_name, filelock = self._create_cache_file()  # get ready
                self.cache_file_name = cache_file_name
                self.filelock = filelock

            self.writer = ArrowWriter(
                features=self.info.features, path=self.cache_file_name, writer_batch_size=self.writer_batch_size
            )
        # Setup rendez-vous here if
        if self.num_process > 1:
            if self.process_id == 0:
                self._check_all_processes_locks()  # wait for everyone to be ready
                self.rendez_vous_lock.release()  # let everyone go
            else:
                self._check_rendez_vous()  # wait for master to be ready and to let everyone go

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
            download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
            dl_manager (Optional ``datasets.DownloadManager``): specific Download Manger to use
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

    def _compute(self, *, predictions=None, references=None, **kwargs) -> Dict[str, Any]:
        """ This method defines the common API for all the metrics in the library """
        raise NotImplementedError

    def __del__(self):
        if self.filelock is not None:
            self.filelock.release()
        if self.rendez_vous_lock is not None:
            self.rendez_vous_lock.release()
        del self.writer
        del self.data
