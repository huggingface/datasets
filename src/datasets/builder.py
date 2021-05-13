# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the TensorFlow Datasets Authors.
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
"""DatasetBuilder base class."""

import abc
import contextlib
import copy
import inspect
import os
import shutil
import urllib
from dataclasses import dataclass
from functools import partial
from typing import Dict, List, Optional, Tuple, Union

from datasets.features import Features
from datasets.utils.mock_download_manager import MockDownloadManager

from . import config, utils
from .arrow_dataset import Dataset
from .arrow_reader import HF_GCP_BASE_URL, ArrowReader, DatasetNotOnHfGcs, MissingFilesOnHfGcs, ReadInstruction
from .arrow_writer import ArrowWriter, BeamWriter
from .dataset_dict import DatasetDict
from .fingerprint import Hasher
from .info import DatasetInfo, DatasetInfosDict, PostProcessedInfo
from .naming import camelcase_to_snakecase, filename_prefix_for_split
from .splits import Split, SplitDict, SplitGenerator
from .utils.download_manager import DownloadManager, GenerateMode
from .utils.file_utils import DownloadConfig, is_remote_url
from .utils.filelock import FileLock
from .utils.info_utils import get_size_checksum_dict, verify_checksums, verify_splits
from .utils.logging import WARNING, get_logger


logger = get_logger(__name__)


class InvalidConfigName(ValueError):
    pass


@dataclass
class BuilderConfig:
    """Base class for :class:`DatasetBuilder` data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    :class:`BuilderConfig` and add their own properties.

    Attributes:
        name (:obj:`str`, default ``"default"``):
        version (:class:`Version` or :obj:`str`, optional):
        data_dir (:obj:`str`, optional):
        data_files (:obj:`str` or :obj:`dict` or :obj:`list` or :obj:`tuple`, optional):
        description (:obj:`str`, optional):
    """

    name: str = "default"
    version: Optional[Union[str, utils.Version]] = "0.0.0"
    data_dir: Optional[str] = None
    data_files: Optional[Union[str, Dict, List, Tuple]] = None
    description: Optional[str] = None

    def __post_init__(self):
        # The config name is used to name the cache directory.
        invalid_windows_characters = r"<>:/\|?*"
        for invalid_char in invalid_windows_characters:
            if invalid_char in self.name:
                raise InvalidConfigName(
                    (
                        "Bad characters from black list '{}' found in '{}'. "
                        "They could create issues when creating a directory "
                        "for this config on Windows filesystem."
                    ).format(invalid_windows_characters, self.name)
                )

    def __eq__(self, o):
        # we need to override the default dataclass __eq__ since it doesn't check for
        # other attributes that the ones of the signature.
        if set(self.__dict__.keys()) != set(o.__dict__.keys()):
            return False
        return all((k, getattr(self, k)) == (k, getattr(o, k)) for k in self.__dict__.keys())

    def create_config_id(self, config_kwargs: dict, custom_features: Optional[Features] = None) -> str:
        """
        The config id is used to build the cache directory.
        By default it is equal to the config name.
        However the name of a config is not sufficent to have a unique identifier for the dataset being generated since
        it doesn't take into account:
        - the config kwargs that can be used to overwrite attributes
        - the custom features used to write the dataset
        - the data_files for json/text/csv/pandas datasets
        Therefore the config id is just the config name with an optional suffix based on these.
        """
        # Possibly add a suffix to the name to handle custom features/data_files/config_kwargs
        suffix: Optional[str] = None
        config_kwargs_to_add_to_suffix = config_kwargs.copy()
        # name and version are already used to build the cache directory
        config_kwargs_to_add_to_suffix.pop("name", None)
        config_kwargs_to_add_to_suffix.pop("version", None)
        # data files are handled differently
        config_kwargs_to_add_to_suffix.pop("data_files", None)
        # data dir handling (when specified it points to the manually downloaded data):
        # it was previously ignored before the introduction of config id because we didn't want
        # to change the config name. Now it's fine to take it into account for the config id.
        # config_kwargs_to_add_to_suffix.pop("data_dir", None)
        if config_kwargs_to_add_to_suffix:
            # we don't care about the order of the kwargs
            config_kwargs_to_add_to_suffix = {
                k: config_kwargs_to_add_to_suffix[k] for k in sorted(config_kwargs_to_add_to_suffix)
            }
            if all(isinstance(v, (str, bool, int, float)) for v in config_kwargs_to_add_to_suffix.values()):
                suffix = ",".join(
                    str(k) + "=" + urllib.parse.quote_plus(str(v)) for k, v in config_kwargs_to_add_to_suffix.items()
                )
                if len(suffix) > 32:  # hash if too long
                    suffix = Hasher.hash(config_kwargs_to_add_to_suffix)
            else:
                suffix = Hasher.hash(config_kwargs_to_add_to_suffix)

        if self.data_files is not None:
            m = Hasher()
            if suffix:
                m.update(suffix)
            if isinstance(self.data_files, str):
                data_files = {"train": [self.data_files]}
            elif isinstance(self.data_files, (tuple, list)):
                data_files = {"train": self.data_files}
            elif isinstance(self.data_files, dict):
                data_files = {
                    str(key): files if isinstance(files, (tuple, list)) else [files]
                    for key, files in self.data_files.items()
                }
            else:
                raise ValueError("Please provide a valid `data_files` in `DatasetBuilder`")
            for key in sorted(data_files.keys()):
                m.update(key)
                for data_file in data_files[key]:
                    m.update(os.path.abspath(data_file))
                    m.update(str(os.path.getmtime(data_file)))
            suffix = m.hexdigest()

        if custom_features is not None:
            m = Hasher()
            if suffix:
                m.update(suffix)
            m.update(custom_features)
            suffix = m.hexdigest()

        if suffix:
            config_id = self.name + "-" + suffix
            if len(config_id) > config.MAX_DATASET_CONFIG_ID_READABLE_LENGTH:
                config_id = self.name + "-" + Hasher.hash(suffix)
            return config_id
        else:
            return self.name


class DatasetBuilder:
    """Abstract base class for all datasets.

    `DatasetBuilder` has 3 key methods:

        - :meth:`datasets.DatasetBuilder.info`: Documents the dataset, including feature
          names, types, and shapes, version, splits, citation, etc.
        - :meth:`datasets.DatasetBuilder.download_and_prepare`: Downloads the source data
          and writes it to disk.
        - :meth:`datasets.DatasetBuilder.as_dataset`: Generates a `Dataset`.

    **Configuration**: Some `DatasetBuilder`s expose multiple variants of the
    dataset by defining a `datasets.BuilderConfig` subclass and accepting a
    config object (or name) on construction. Configurable datasets expose a
    pre-defined set of configurations in :meth:`datasets.DatasetBuilder.builder_configs`.
    """

    # Default version.
    VERSION = utils.Version("0.0.0")

    # Class for the builder config.
    BUILDER_CONFIG_CLASS = BuilderConfig

    # Named configurations that modify the data generated by download_and_prepare.
    BUILDER_CONFIGS = []

    # Optional default config name to be used used when name is None
    DEFAULT_CONFIG_NAME = None

    def __init__(
        self,
        cache_dir: Optional[str] = None,
        name: Optional[str] = None,
        hash: Optional[str] = None,
        features: Optional[Features] = None,
        **config_kwargs,
    ):
        """Constructs a DatasetBuilder.

        Callers must pass arguments as keyword arguments.

        Args:
            cache_dir: `str`, directory to read/write data. Defaults to "~/datasets".
            name: `str` name, optional configuration for the dataset that affects the data generated on disk. Different
                `builder_config`s will have their own subdirectories and versions.
                If not provided, uses the first configuration in self.BUILDER_CONFIGS
            hash: a hash specific to the dataset code. Used to update the caching directory when the dataset loading
                script code is udpated (to avoid reusing old data).
                The typical caching directory (defined in ``self._relative_data_dir``) is: ``name/version/hash/``
            features: `Features`, optional features that will be used to read/write the dataset
                It can be used to changed the :obj:`datasets.Features` description of a dataset for example.
            config_kwargs: will override the defaults kwargs in config

        """
        # DatasetBuilder name
        self.name: str = camelcase_to_snakecase(self.__class__.__name__)
        self.hash: Optional[str] = hash

        # Prepare config: DatasetConfig contains name, version and description but can be extended by each dataset
        config_kwargs = {key: value for key, value in config_kwargs.items() if value is not None}
        if "features" in inspect.signature(self.BUILDER_CONFIG_CLASS.__init__).parameters and features is not None:
            config_kwargs["features"] = features
        self.config, self.config_id = self._create_builder_config(
            name,
            custom_features=features,
            **config_kwargs,
        )

        # prepare info: DatasetInfo are a standardized dataclass across all datasets
        # Prefill datasetinfo
        info = self.get_exported_dataset_info()
        info.update(self._info())
        info.builder_name = self.name
        info.config_name = self.config.name
        info.version = self.config.version
        self.info = info
        # update info with user specified infos
        if features is not None:
            self.info.features = features

        # prepare data dirs
        self._cache_dir_root = os.path.expanduser(cache_dir or config.HF_DATASETS_CACHE)
        self._cache_dir = self._build_cache_dir()
        if not is_remote_url(self._cache_dir_root):
            os.makedirs(self._cache_dir_root, exist_ok=True)
        lock_path = os.path.join(self._cache_dir_root, self._cache_dir.replace(os.sep, "_") + ".lock")
        with FileLock(lock_path):
            if os.path.exists(self._cache_dir):  # check if data exist
                if len(os.listdir(self._cache_dir)) > 0:
                    logger.info("Overwrite dataset info from restored data version.")
                    self.info = DatasetInfo.from_directory(self._cache_dir)
                else:  # dir exists but no data, remove the empty dir as data aren't available anymore
                    logger.warning(
                        "Old caching folder {} for dataset {} exists but not data were found. Removing it. ".format(
                            self._cache_dir, self.name
                        )
                    )
                    os.rmdir(self._cache_dir)

        # Set download manager
        self.dl_manager = None

    # Must be set for datasets that use 'data_dir' functionality - the ones
    # that require users to do additional steps to download the data
    # (this is usually due to some external regulations / rules).
    # This field should contain a string with user instructions, including
    # the list of files that should be present. It will be
    # displayed in the dataset documentation.
    @property
    def manual_download_instructions(self) -> Optional[str]:
        return None

    @classmethod
    def get_all_exported_dataset_infos(cls) -> dict:
        """Empty dict if doesn't exist"""
        dset_infos_file_path = os.path.join(cls.get_imported_module_dir(), config.DATASETDICT_INFOS_FILENAME)
        if os.path.exists(dset_infos_file_path):
            return DatasetInfosDict.from_directory(cls.get_imported_module_dir())
        return {}

    def get_exported_dataset_info(self) -> DatasetInfo:
        """Empty DatasetInfo if doesn't exist"""
        return self.get_all_exported_dataset_infos().get(self.config.name, DatasetInfo())

    def _create_builder_config(self, name=None, custom_features=None, **config_kwargs) -> Tuple[BuilderConfig, str]:
        """Create and validate BuilderConfig object as well as a unique config id for this config.
        Raises ValueError if there are multiple builder configs and name and DEFAULT_CONFIG_NAME are None.
        config_kwargs override the defaults kwargs in config
        """
        builder_config = None

        # try default config
        if name is None and self.BUILDER_CONFIGS and not config_kwargs:
            if self.DEFAULT_CONFIG_NAME is not None:
                builder_config = self.builder_configs.get(self.DEFAULT_CONFIG_NAME)
                logger.warning("No config specified, defaulting to: %s/%s", self.name, builder_config.name)
            else:
                if len(self.BUILDER_CONFIGS) > 1:
                    example_of_usage = "load_dataset('{}', '{}')".format(self.name, self.BUILDER_CONFIGS[0].name)
                    raise ValueError(
                        "Config name is missing."
                        "\nPlease pick one among the available configs: %s" % list(self.builder_configs.keys())
                        + "\nExample of usage:\n\t`{}`".format(example_of_usage)
                    )
                builder_config = self.BUILDER_CONFIGS[0]
                logger.info("No config specified, defaulting to first: %s/%s", self.name, builder_config.name)

        # try get config by name
        if isinstance(name, str):
            builder_config = self.builder_configs.get(name)
            if builder_config is None and self.BUILDER_CONFIGS:
                raise ValueError(
                    "BuilderConfig %s not found. Available: %s" % (name, list(self.builder_configs.keys()))
                )

        # if not using an existing config, then create a new config on the fly with config_kwargs
        if not builder_config:
            if name is not None:
                config_kwargs["name"] = name
            if "version" not in config_kwargs and hasattr(self, "VERSION") and self.VERSION:
                config_kwargs["version"] = self.VERSION
            builder_config = self.BUILDER_CONFIG_CLASS(**config_kwargs)

        # otherwise use the config_kwargs to overwrite the attributes
        else:
            builder_config = copy.deepcopy(builder_config)
            for key, value in config_kwargs.items():
                if value is not None:
                    if not hasattr(builder_config, key):
                        raise ValueError(f"BuilderConfig {builder_config} doesn't have a '{key}' key.")
                    setattr(builder_config, key, value)

        if not builder_config.name:
            raise ValueError("BuilderConfig must have a name, got %s" % builder_config.name)

        # compute the config id that is going to be used for caching
        config_id = builder_config.create_config_id(config_kwargs, custom_features=custom_features)
        is_custom = config_id not in self.builder_configs
        if is_custom:
            logger.warning("Using custom data configuration %s", config_id)
        else:
            if builder_config != self.builder_configs[builder_config.name]:
                raise ValueError(
                    "Cannot name a custom BuilderConfig the same as an available "
                    "BuilderConfig. Change the name. Available BuilderConfigs: %s"
                    % (list(self.builder_configs.keys()))
                )
            if not builder_config.version:
                raise ValueError("BuilderConfig %s must have a version" % builder_config.name)
            # if not builder_config.description:
            #     raise ValueError("BuilderConfig %s must have a description" % builder_config.name)

        return builder_config, config_id

    @utils.classproperty
    @classmethod
    @utils.memoize()
    def builder_configs(cls):
        """Pre-defined list of configurations for this builder class."""
        config_dict = {config.name: config for config in cls.BUILDER_CONFIGS}
        if len(config_dict) != len(cls.BUILDER_CONFIGS):
            names = [config.name for config in cls.BUILDER_CONFIGS]
            raise ValueError("Names in BUILDER_CONFIGS must not be duplicated. Got %s" % names)
        return config_dict

    @property
    def cache_dir(self):
        return self._cache_dir

    def _relative_data_dir(self, with_version=True, with_hash=True):
        """Relative path of this dataset in cache_dir:
        Will be:
            self.name/self.config.version/self.hash/
        If any of these element is missing or if ``with_version=False`` the corresponding subfolders are dropped.
        """
        builder_data_dir = self.name
        builder_config = self.config
        hash = self.hash
        if builder_config:
            # use the enriched name instead of the name to make it unique
            builder_data_dir = os.path.join(builder_data_dir, self.config_id)
        if with_version:
            builder_data_dir = os.path.join(builder_data_dir, str(self.config.version))
        if with_hash and hash and isinstance(hash, str):
            builder_data_dir = os.path.join(builder_data_dir, hash)
        return builder_data_dir

    def _build_cache_dir(self):
        """Return the data directory for the current version."""
        builder_data_dir = os.path.join(self._cache_dir_root, self._relative_data_dir(with_version=False))
        version_data_dir = os.path.join(self._cache_dir_root, self._relative_data_dir(with_version=True))

        def _other_versions_on_disk():
            """Returns previous versions on disk."""
            if not os.path.exists(builder_data_dir):
                return []

            version_dirnames = []
            for dir_name in os.listdir(builder_data_dir):
                try:
                    version_dirnames.append((utils.Version(dir_name), dir_name))
                except ValueError:  # Invalid version (ex: incomplete data dir)
                    pass
            version_dirnames.sort(reverse=True)
            return version_dirnames

        # Check and warn if other versions exist on disk
        version_dirs = _other_versions_on_disk()
        if version_dirs:
            other_version = version_dirs[0][0]
            if other_version != self.config.version:
                warn_msg = (
                    "Found a different version {other_version} of dataset {name} in "
                    "cache_dir {cache_dir}. Using currently defined version "
                    "{cur_version}.".format(
                        other_version=str(other_version),
                        name=self.name,
                        cache_dir=self._cache_dir_root,
                        cur_version=str(self.config.version),
                    )
                )
                logger.warning(warn_msg)

        return version_data_dir

    @abc.abstractmethod
    def _info(self) -> DatasetInfo:
        """Construct the DatasetInfo object. See `DatasetInfo` for details.

        Warning: This function is only called once and the result is cached for all
        following .info() calls.

        Returns:
            info: (DatasetInfo) The dataset information
        """
        raise NotImplementedError

    @classmethod
    def get_imported_module_dir(cls):
        """Return the path of the module of this class or subclass."""
        return os.path.dirname(inspect.getfile(inspect.getmodule(cls)))

    def download_and_prepare(
        self,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[GenerateMode] = None,
        ignore_verifications: bool = False,
        try_from_hf_gcs: bool = True,
        dl_manager: Optional[DownloadManager] = None,
        base_path: Optional[str] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
        **download_and_prepare_kwargs,
    ):
        """Downloads and prepares dataset for reading.

        Args:
            download_config (Optional ``datasets.DownloadConfig``: specific download configuration parameters.
            download_mode (Optional `datasets.GenerateMode`): select the download/generate mode - Default to REUSE_DATASET_IF_EXISTS
            ignore_verifications (bool): Ignore the verifications of the downloaded/processed dataset information (checksums/size/splits/...)
            save_infos (bool): Save the dataset information (checksums/size/splits/...)
            try_from_hf_gcs (bool): If True, it will try to download the already prepared dataset from the Hf google cloud storage
            dl_manager (Optional ``datasets.DownloadManager``): specific Download Manger to use
            base_path: ( Optional ``str``): base path for relative paths that are used to download files. This can be a remote url.
            use_auth_token (Optional ``Union[str, bool]``): Optional string or boolean to use as Bearer token for remote files on the Datasets Hub.
                If True, will get token from ~/.huggingface.

        """
        download_mode = GenerateMode(download_mode or GenerateMode.REUSE_DATASET_IF_EXISTS)
        verify_infos = not ignore_verifications

        if dl_manager is None:
            if download_config is None:
                download_config = DownloadConfig(
                    cache_dir=os.path.join(self._cache_dir_root, "downloads"),
                    force_download=bool(download_mode == GenerateMode.FORCE_REDOWNLOAD),
                    use_etag=False,
                    use_auth_token=use_auth_token,
                )  # We don't use etag for data files to speed up the process

            dl_manager = DownloadManager(
                dataset_name=self.name,
                download_config=download_config,
                data_dir=self.config.data_dir,
                base_path=base_path,
            )
        elif isinstance(dl_manager, MockDownloadManager):
            try_from_hf_gcs = False
        self.dl_manager = dl_manager

        # Prevent parallel disk operations
        lock_path = os.path.join(self._cache_dir_root, self._cache_dir.replace(os.sep, "_") + ".lock")
        with FileLock(lock_path):
            data_exists = os.path.exists(self._cache_dir)
            if data_exists and download_mode == GenerateMode.REUSE_DATASET_IF_EXISTS:
                logger.warning("Reusing dataset %s (%s)", self.name, self._cache_dir)
                # We need to update the info in case some splits were added in the meantime
                # for example when calling load_dataset from multiple workers.
                self.info = self._load_info()
                self.download_post_processing_resources(dl_manager)
                return
            logger.info("Generating dataset %s (%s)", self.name, self._cache_dir)
            if not is_remote_url(self._cache_dir_root):  # if cache dir is local, check for available space
                if not utils.has_sufficient_disk_space(self.info.size_in_bytes or 0, directory=self._cache_dir_root):
                    raise IOError(
                        "Not enough disk space. Needed: {} (download: {}, generated: {}, post-processed: {})".format(
                            utils.size_str(self.info.size_in_bytes or 0),
                            utils.size_str(self.info.download_size or 0),
                            utils.size_str(self.info.dataset_size or 0),
                            utils.size_str(self.info.post_processing_size or 0),
                        )
                    )

            @contextlib.contextmanager
            def incomplete_dir(dirname):
                """Create temporary dir for dirname and rename on exit."""
                if is_remote_url(dirname):
                    yield dirname
                else:
                    tmp_dir = dirname + ".incomplete"
                    os.makedirs(tmp_dir, exist_ok=True)
                    try:
                        yield tmp_dir
                        if os.path.isdir(dirname):
                            shutil.rmtree(dirname)
                        os.rename(tmp_dir, dirname)
                    finally:
                        if os.path.exists(tmp_dir):
                            shutil.rmtree(tmp_dir)

            # Print is intentional: we want this to always go to stdout so user has
            # information needed to cancel download/preparation if needed.
            # This comes right before the progress bar.
            print(
                f"Downloading and preparing dataset {self.info.builder_name}/{self.info.config_name} "
                f"(download: {utils.size_str(self.info.download_size)}, generated: {utils.size_str(self.info.dataset_size)}, "
                f"post-processed: {utils.size_str(self.info.post_processing_size)}, "
                f"total: {utils.size_str(self.info.size_in_bytes)}) to {self._cache_dir}..."
            )

            if self.manual_download_instructions is not None:
                assert (
                    dl_manager.manual_dir is not None
                ), "The dataset {} with config {} requires manual data. \n Please follow the manual download instructions: {}. \n Manual data can be loaded with `datasets.load_dataset({}, data_dir='<path/to/manual/data>')".format(
                    self.name, self.config.name, self.manual_download_instructions, self.name
                )

            # Create a tmp dir and rename to self._cache_dir on successful exit.
            with incomplete_dir(self._cache_dir) as tmp_data_dir:
                # Temporarily assign _cache_dir to tmp_data_dir to avoid having to forward
                # it to every sub function.
                with utils.temporary_assignment(self, "_cache_dir", tmp_data_dir):
                    # Try to download the already prepared dataset files
                    downloaded_from_gcs = False
                    if try_from_hf_gcs:
                        try:
                            self._download_prepared_from_hf_gcs(dl_manager._download_config)
                            downloaded_from_gcs = True
                        except (DatasetNotOnHfGcs, MissingFilesOnHfGcs):
                            logger.info("Dataset not on Hf google storage. Downloading and preparing it from source")
                        except ConnectionError:
                            logger.warning("HF google storage unreachable. Downloading and preparing it from source")
                    if not downloaded_from_gcs:
                        self._download_and_prepare(
                            dl_manager=dl_manager, verify_infos=verify_infos, **download_and_prepare_kwargs
                        )
                    # Sync info
                    self.info.dataset_size = sum(split.num_bytes for split in self.info.splits.values())
                    self.info.download_checksums = dl_manager.get_recorded_sizes_checksums()
                    self.info.size_in_bytes = self.info.dataset_size + self.info.download_size
                    # Save info
                    self._save_info()

            # Download post processing resources
            self.download_post_processing_resources(dl_manager)

            print(
                f"Dataset {self.name} downloaded and prepared to {self._cache_dir}. "
                f"Subsequent calls will reuse this data."
            )

    def _download_prepared_from_hf_gcs(self, download_config: DownloadConfig):
        relative_data_dir = self._relative_data_dir(with_version=True, with_hash=False)
        reader = ArrowReader(self._cache_dir, self.info)
        # use reader instructions to download the right files
        reader.download_from_hf_gcs(download_config, relative_data_dir)
        downloaded_info = DatasetInfo.from_directory(self._cache_dir)
        self.info.update(downloaded_info)
        # download post processing resources
        remote_cache_dir = HF_GCP_BASE_URL + "/" + relative_data_dir.replace(os.sep, "/")
        for split in self.info.splits:
            for resource_file_name in self._post_processing_resources(split).values():
                if os.sep in resource_file_name:
                    raise ValueError("Resources shouldn't be in a sub-directory: {}".format(resource_file_name))
                try:
                    resource_path = utils.cached_path(remote_cache_dir + "/" + resource_file_name)
                    shutil.move(resource_path, os.path.join(self._cache_dir, resource_file_name))
                except ConnectionError:
                    logger.info(
                        "Couldn't download resourse file {} from Hf google storage.".format(resource_file_name)
                    )
        logger.info("Dataset downloaded from Hf google storage.")

    def _download_and_prepare(self, dl_manager, verify_infos, **prepare_split_kwargs):
        """Downloads and prepares dataset for reading.

        This is the internal implementation to overwrite called when user calls
        `download_and_prepare`. It should download all required data and generate
        the pre-processed datasets files.

        Args:
            dl_manager: (DownloadManager) `DownloadManager` used to download and cache
                data.
            verify_infos: bool, if False, do not perform checksums and size tests.
            prepare_split_kwargs: Additional options.
        """
        # Generating data for all splits
        split_dict = SplitDict(dataset_name=self.name)
        split_generators_kwargs = self._make_split_generators_kwargs(prepare_split_kwargs)
        split_generators = self._split_generators(dl_manager, **split_generators_kwargs)

        # Checksums verification
        if verify_infos:
            verify_checksums(
                self.info.download_checksums, dl_manager.get_recorded_sizes_checksums(), "dataset source files"
            )

        # Build splits
        for split_generator in split_generators:
            if str(split_generator.split_info.name).lower() == "all":
                raise ValueError(
                    "`all` is a special split keyword corresponding to the "
                    "union of all splits, so cannot be used as key in "
                    "._split_generator()."
                )

            logger.info("Generating split %s", split_generator.split_info.name)
            split_dict.add(split_generator.split_info)

            try:
                # Prepare split will record examples associated to the split
                self._prepare_split(split_generator, **prepare_split_kwargs)
            except OSError as e:
                raise OSError(
                    "Cannot find data file. "
                    + (self.manual_download_instructions or "")
                    + "\nOriginal error:\n"
                    + str(e)
                )

        if verify_infos:
            verify_splits(self.info.splits, split_dict)

        # Update the info object with the splits.
        self.info.splits = split_dict
        self.info.download_size = dl_manager.downloaded_size

    def download_post_processing_resources(self, dl_manager):
        for split in self.info.splits:
            for resource_name, resource_file_name in self._post_processing_resources(split).items():
                if os.sep in resource_file_name:
                    raise ValueError("Resources shouldn't be in a sub-directory: {}".format(resource_file_name))
                resource_path = os.path.join(self._cache_dir, resource_file_name)
                if not os.path.exists(resource_path):
                    downloaded_resource_path = self._download_post_processing_resources(
                        split, resource_name, dl_manager
                    )
                    if downloaded_resource_path:
                        logger.info(
                            "Downloaded post-processing resource {} as {}".format(resource_name, resource_file_name)
                        )
                        shutil.move(downloaded_resource_path, resource_path)

    def _load_info(self) -> DatasetInfo:
        return DatasetInfo.from_directory(self._cache_dir)

    def _save_info(self):
        lock_path = os.path.join(self._cache_dir_root, self._cache_dir.replace(os.sep, "_") + ".lock")
        with FileLock(lock_path):
            self.info.write_to_directory(self._cache_dir)

    def _save_infos(self):
        lock_path = os.path.join(self._cache_dir_root, self._cache_dir.replace(os.sep, "_") + ".lock")
        with FileLock(lock_path):
            DatasetInfosDict(**{self.config.name: self.info}).write_to_directory(self.get_imported_module_dir())

    def _make_split_generators_kwargs(self, prepare_split_kwargs):
        """Get kwargs for `self._split_generators()` from `prepare_split_kwargs`."""
        del prepare_split_kwargs
        return {}

    def as_dataset(
        self, split: Optional[Split] = None, run_post_process=True, ignore_verifications=False, in_memory=False
    ) -> Union[Dataset, DatasetDict]:
        """Return a Dataset for the specified split.

        Args:
            split (`datasets.Split`): Which subset of the data to return.
            run_post_process (bool, default=True): Whether to run post-processing dataset transforms and/or add
                indexes.
            ignore_verifications (bool, default=False): Whether to ignore the verifications of the
                downloaded/processed dataset information (checksums/size/splits/...).
            in_memory (bool, default=False): Whether to copy the data in-memory.

        Returns:
            datasets.Dataset
        """
        if not os.path.exists(self._cache_dir):
            raise AssertionError(
                (
                    "Dataset %s: could not find data in %s. Please make sure to call "
                    "builder.download_and_prepare(), or pass download=True to "
                    "datasets.load_dataset() before trying to access the Dataset object."
                )
                % (self.name, self._cache_dir_root)
            )

        logger.info(
            "Constructing Dataset for split %s, from %s", split or ", ".join(self.info.splits), self._cache_dir
        )

        # By default, return all splits
        if split is None:
            split = {s: s for s in self.info.splits}

        # Create a dataset for each of the given splits
        datasets = utils.map_nested(
            partial(
                self._build_single_dataset,
                run_post_process=run_post_process,
                ignore_verifications=ignore_verifications,
                in_memory=in_memory,
            ),
            split,
            map_tuple=True,
        )
        if isinstance(datasets, dict):
            datasets = DatasetDict(datasets)
        return datasets

    def _build_single_dataset(
        self,
        split: Union[str, ReadInstruction, Split],
        run_post_process: bool,
        ignore_verifications: bool,
        in_memory: bool = False,
    ):
        """as_dataset for a single split."""
        verify_infos = not ignore_verifications
        if isinstance(split, str):
            split = Split(split)

        # Build base dataset
        ds = self._as_dataset(
            split=split,
            in_memory=in_memory,
        )
        if run_post_process:
            for resource_file_name in self._post_processing_resources(split).values():
                if os.sep in resource_file_name:
                    raise ValueError("Resources shouldn't be in a sub-directory: {}".format(resource_file_name))
            resources_paths = {
                resource_name: os.path.join(self._cache_dir, resource_file_name)
                for resource_name, resource_file_name in self._post_processing_resources(split).items()
            }
            post_processed = self._post_process(ds, resources_paths)
            if post_processed is not None:
                ds = post_processed
                recorded_checksums = {}
                for resource_name, resource_path in resources_paths.items():
                    size_checksum = get_size_checksum_dict(resource_path)
                    recorded_checksums[resource_name] = size_checksum
                if verify_infos:
                    if self.info.post_processed is None or self.info.post_processed.resources_checksums is None:
                        expected_checksums = None
                    else:
                        expected_checksums = self.info.post_processed.resources_checksums.get(split)
                    verify_checksums(expected_checksums, recorded_checksums, "post processing resources")
                if self.info.post_processed is None:
                    self.info.post_processed = PostProcessedInfo()
                if self.info.post_processed.resources_checksums is None:
                    self.info.post_processed.resources_checksums = {}
                self.info.post_processed.resources_checksums[str(split)] = recorded_checksums
                self.info.post_processing_size = sum(
                    checksums_dict["num_bytes"]
                    for split_checksums_dicts in self.info.post_processed.resources_checksums.values()
                    for checksums_dict in split_checksums_dicts.values()
                )
                if self.info.dataset_size is not None and self.info.download_size is not None:
                    self.info.size_in_bytes = (
                        self.info.dataset_size + self.info.download_size + self.info.post_processing_size
                    )
                self._save_info()
                ds._info.post_processed = self.info.post_processed
                ds._info.post_processing_size = self.info.post_processing_size
                ds._info.size_in_bytes = self.info.size_in_bytes
                if self.info.post_processed.features is not None:
                    if self.info.post_processed.features.type != ds.features.type:
                        raise ValueError(
                            "Post-processed features info don't match the dataset:\nGot\n{}\nbut expected something like\n{}".format(
                                self.info.post_processed.features, ds.features
                            )
                        )
                    else:
                        ds.info.features = self.info.post_processed.features

        return ds

    def _as_dataset(self, split: Union[ReadInstruction, Split] = Split.TRAIN, in_memory: bool = False) -> Dataset:
        """Constructs a `Dataset`.

        This is the internal implementation to overwrite called when user calls
        `as_dataset`. It should read the pre-processed datasets files and generate
        the `Dataset` object.

        Args:
            split: `datasets.Split` which subset of the data to read.
            in_memory (bool, default False): Whether to copy the data in-memory.

        Returns:
            `Dataset`
        """

        dataset_kwargs = ArrowReader(self._cache_dir, self.info).read(
            name=self.name,
            instructions=split,
            split_infos=self.info.splits.values(),
            in_memory=in_memory,
        )
        return Dataset(**dataset_kwargs)

    def _post_process(self, dataset: Dataset, resources_paths: Dict[str, str]) -> Optional[Dataset]:
        """Run dataset transforms or add indexes"""
        return None

    def _post_processing_resources(self, split: str) -> Dict[str, str]:
        """Mapping resource_name -> resource_file_name"""
        return {}

    def _download_post_processing_resources(
        self, split: str, resource_name: str, dl_manager: DownloadManager
    ) -> Optional[str]:
        """Download the resource using the download manager and return the downloaded path"""

    @abc.abstractmethod
    def _split_generators(self, dl_manager: DownloadManager):
        """Specify feature dictionary generators and dataset splits.

        This function returns a list of `SplitGenerator`s defining how to generate
        data and what splits to use.

        Example:

            return[
                    datasets.SplitGenerator(
                            name=datasets.Split.TRAIN,
                            gen_kwargs={'file': 'train_data.zip'},
                    ),
                    datasets.SplitGenerator(
                            name=datasets.Split.TEST,
                            gen_kwargs={'file': 'test_data.zip'},
                    ),
            ]

        The above code will first call `_generate_examples(file='train_data.zip')`
        to write the train data, then `_generate_examples(file='test_data.zip')` to
        write the test data.

        Datasets are typically split into different subsets to be used at various
        stages of training and evaluation.

        Note that for datasets without a `VALIDATION` split, you can use a
        fraction of the `TRAIN` data for evaluation as you iterate on your model
        so as not to overfit to the `TEST` data.

        For downloads and extractions, use the given `download_manager`.
        Note that the `DownloadManager` caches downloads, so it is fine to have each
        generator attempt to download the source data.

        A good practice is to download all data in this function, and then
        distribute the relevant parts to each split with the `gen_kwargs` argument

        Args:
            dl_manager: (DownloadManager) Download manager to download the data

        Returns:
            `list<SplitGenerator>`.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def _prepare_split(self, split_generator: SplitGenerator, **kwargs):
        """Generate the examples and record them on disk.

        Args:
            split_generator: `SplitGenerator`, Split generator to process
            **kwargs: Additional kwargs forwarded from _download_and_prepare (ex:
                beam pipeline)
        """
        raise NotImplementedError()


class GeneratorBasedBuilder(DatasetBuilder):
    """Base class for datasets with data generation based on dict generators.

    `GeneratorBasedBuilder` is a convenience class that abstracts away much
    of the data writing and reading of `DatasetBuilder`. It expects subclasses to
    implement generators of feature dictionaries across the dataset splits
    (`_split_generators`). See the method docstrings for details.
    """

    # GeneratorBasedBuilder should have dummy data for tests by default
    test_dummy_data = True

    # Default batch size used by the ArrowWriter
    # It defines the number of samples that are kept in memory before writing them
    # and also the length of the arrow chunks
    # None means that the ArrowWriter will use its default value
    DEFAULT_WRITER_BATCH_SIZE = None

    def __init__(self, *args, writer_batch_size=None, **kwargs):
        super(GeneratorBasedBuilder, self).__init__(*args, **kwargs)
        # Batch size used by the ArrowWriter
        # It defines the number of samples that are kept in memory before writing them
        # and also the length of the arrow chunks
        # None means that the ArrowWriter will use its default value
        self._writer_batch_size = writer_batch_size or self.DEFAULT_WRITER_BATCH_SIZE

    @abc.abstractmethod
    def _generate_examples(self, **kwargs):
        """Default function generating examples for each `SplitGenerator`.

        This function preprocess the examples from the raw data to the preprocessed
        dataset files.
        This function is called once for each `SplitGenerator` defined in
        `_split_generators`. The examples yielded here will be written on
        disk.

        Args:
            **kwargs: `dict`, Arguments forwarded from the SplitGenerator.gen_kwargs

        Yields:
            key: `str` or `int`, a unique deterministic example identification key.
                * Unique: An error will be raised if two examples are yield with the
                    same key.
                * Deterministic: When generating the dataset twice, the same example
                    should have the same key.
                Good keys can be the image id, or line number if examples are extracted
                from a text file.
                The key will be hashed and sorted to shuffle examples deterministically,
                such as generating the dataset multiple times keep examples in the
                same order.
            example: `dict<str feature_name, feature_value>`, a feature dictionary
                ready to be encoded and written to disk. The example will be
                encoded with `self.info.features.encode_example({...})`.
        """
        raise NotImplementedError()

    def _prepare_split(self, split_generator):
        split_info = split_generator.split_info

        fname = "{}-{}.arrow".format(self.name, split_generator.name)
        fpath = os.path.join(self._cache_dir, fname)

        generator = self._generate_examples(**split_generator.gen_kwargs)
        not_verbose = bool(logger.getEffectiveLevel() > WARNING)

        with ArrowWriter(
            features=self.info.features,
            path=fpath,
            writer_batch_size=self._writer_batch_size,
            hash_salt=split_info.name,
            check_duplicates=True,
        ) as writer:
            try:
                for key, record in utils.tqdm(
                    generator, unit=" examples", total=split_info.num_examples, leave=False, disable=not_verbose
                ):
                    example = self.info.features.encode_example(record)
                    writer.write(example, key)
            finally:
                num_examples, num_bytes = writer.finalize()

        split_generator.split_info.num_examples = num_examples
        split_generator.split_info.num_bytes = num_bytes


class ArrowBasedBuilder(DatasetBuilder):
    """Base class for datasets with data generation based on Arrow loading functions (CSV/JSON/Parquet)."""

    # ArrowBasedBuilder should have dummy data for tests by default
    test_dummy_data = True

    @abc.abstractmethod
    def _generate_examples(self, **kwargs):
        """Default function generating examples for each `SplitGenerator`.

        This function preprocess the examples from the raw data to the preprocessed
        dataset files.
        This function is called once for each `SplitGenerator` defined in
        `_split_generators`. The examples yielded here will be written on
        disk.

        Args:
            **kwargs: `dict`, Arguments forwarded from the SplitGenerator.gen_kwargs

        Yields:
            key: `str` or `int`, a unique deterministic example identification key.
                * Unique: An error will be raised if two examples are yield with the
                    same key.
                * Deterministic: When generating the dataset twice, the same example
                    should have the same key.
                Good keys can be the image id, or line number if examples are extracted
                from a text file.
                The key will be hashed and sorted to shuffle examples deterministically,
                such as generating the dataset multiple times keep examples in the
                same order.
            example: `dict<str feature_name, feature_value>`, a feature dictionary
                ready to be encoded and written to disk. The example will be
                encoded with `self.info.features.encode_example({...})`.
        """
        raise NotImplementedError()

    def _prepare_split(self, split_generator):
        fname = "{}-{}.arrow".format(self.name, split_generator.name)
        fpath = os.path.join(self._cache_dir, fname)

        generator = self._generate_tables(**split_generator.gen_kwargs)
        not_verbose = bool(logger.getEffectiveLevel() > WARNING)
        with ArrowWriter(features=self.info.features, path=fpath) as writer:
            for key, table in utils.tqdm(generator, unit=" tables", leave=False, disable=not_verbose):
                writer.write_table(table)
            num_examples, num_bytes = writer.finalize()

        split_generator.split_info.num_examples = num_examples
        split_generator.split_info.num_bytes = num_bytes
        if self.info.features is None:
            self.info.features = writer._features


class MissingBeamOptions(ValueError):
    pass


class BeamBasedBuilder(DatasetBuilder):
    """Beam based Builder."""

    # BeamBasedBuilder does not have dummy data for tests yet
    test_dummy_data = False

    def __init__(self, *args, **kwargs):
        self._beam_runner = kwargs.pop("beam_runner", None)
        self._beam_options = kwargs.pop("beam_options", None)
        super(BeamBasedBuilder, self).__init__(*args, **kwargs)
        self._beam_writers = {}  # {split: beam_writer} mapping.

    def _make_split_generators_kwargs(self, prepare_split_kwargs):
        # Pass `pipeline` into `_split_generators()` from `prepare_split_kwargs` if
        # it's in the call signature of `_split_generators()`.
        # This allows for global preprocessing in beam.
        split_generators_kwargs = {}
        split_generators_arg_names = inspect.signature(self._split_generators).parameters.keys()
        if "pipeline" in split_generators_arg_names:
            split_generators_kwargs["pipeline"] = prepare_split_kwargs["pipeline"]
        return split_generators_kwargs

    @abc.abstractmethod
    def _build_pcollection(self, pipeline, **kwargs):
        """Build the beam pipeline examples for each `SplitGenerator`.

        This function extracts examples from the raw data with parallel transforms
        in a Beam pipeline. It is called once for each `SplitGenerator` defined in
        `_split_generators`. The examples from the PCollection will be
        encoded and written to disk.

        Warning: When running in a distributed setup, make sure that the data
        which will be read (download_dir, manual_dir,...) and written (cache_dir)
        can be accessed by the workers jobs. The data should be located in a
        shared filesystem, like GCS.

        Example:

        ```
        def _build_pcollection(pipeline, extracted_dir):
            return (
                    pipeline
                    | beam.Create(gfile.io.listdir(extracted_dir))
                    | beam.Map(_process_file)
            )
        ```

        Args:
            pipeline: `beam.Pipeline`, root Beam pipeline
            **kwargs: Arguments forwarded from the SplitGenerator.gen_kwargs

        Returns:
            pcollection: `PCollection`, an Apache Beam PCollection containing the
                example to send to `self.info.features.encode_example(...)`.
        """
        raise NotImplementedError()

    def _download_and_prepare(self, dl_manager, verify_infos):
        # Create the Beam pipeline and forward it to _prepare_split
        import apache_beam as beam

        import datasets.utils.beam_utils as beam_utils

        beam_runner = self._beam_runner
        beam_options = self._beam_options

        if not beam_runner and not beam_options:
            usage_example = f"load_dataset('{self.name}', '{self.config.name}', beam_runner='DirectRunner')"
            raise MissingBeamOptions(
                "Trying to generate a dataset using Apache Beam, yet no Beam Runner "
                "or PipelineOptions() has been provided in `load_dataset` or in the "
                "builder arguments. For big datasets it has to run on large-scale data "
                "processing tools like Dataflow, Spark, etc. More information about "
                "Apache Beam runners at "
                "https://beam.apache.org/documentation/runners/capability-matrix/"
                "\nIf you really want to run it locally because you feel like the "
                "Dataset is small enough, you can use the local beam runner called "
                "`DirectRunner` (you may run out of memory). \nExample of usage: "
                "\n\t`{}`".format(usage_example)
            )

        beam_options = beam_options or beam.options.pipeline_options.PipelineOptions()
        # Beam type checking assumes transforms multiple outputs are of same type,
        # which is not our case. Plus it doesn't handle correctly all types, so we
        # are better without it.
        beam_options.view_as(beam.options.pipeline_options.TypeOptions).pipeline_type_check = False
        # Use a single pipeline for all splits
        pipeline = beam_utils.BeamPipeline(
            runner=beam_runner,
            options=beam_options,
        )
        super(BeamBasedBuilder, self)._download_and_prepare(
            dl_manager,
            verify_infos=False,
            pipeline=pipeline,
        )  # TODO handle verify_infos in beam datasets
        # Run pipeline
        pipeline_results = pipeline.run()
        pipeline_results.wait_until_finish()
        metrics = pipeline_results.metrics()
        # Update `info.splits`.
        split_dict = self.info.splits
        for split_name, beam_writer in self._beam_writers.items():
            m_filter = beam.metrics.MetricsFilter().with_namespace(namespace=split_name)
            num_examples, num_bytes = beam_writer.finalize(metrics.query(m_filter))
            split_info = split_dict[split_name]
            split_info.num_examples = num_examples
            split_info.num_bytes = num_bytes

    def _save_info(self):
        if os.path.exists(self._cache_dir):
            super()._save_info()
        else:
            import apache_beam as beam

            fs = beam.io.filesystems.FileSystems
            with fs.create(os.path.join(self._cache_dir, config.DATASET_INFO_FILENAME)) as f:
                self.info._dump_info(f)
            with fs.create(os.path.join(self._cache_dir, config.LICENSE_FILENAME)) as f:
                self.info._dump_license(f)

    def _prepare_split(self, split_generator, pipeline):
        import apache_beam as beam

        split_name = split_generator.split_info.name
        output_prefix = filename_prefix_for_split(self.name, split_name)
        output_prefix = os.path.join(self._cache_dir, output_prefix)

        # To write examples to disk:
        fname = "{}-{}.arrow".format(self.name, split_name)
        fpath = os.path.join(self._cache_dir, fname)
        beam_writer = BeamWriter(
            features=self.info.features, path=fpath, namespace=split_name, cache_dir=self._cache_dir
        )
        self._beam_writers[split_name] = beam_writer

        encode_example = self.info.features.encode_example

        # Note: We need to wrap the pipeline in a PTransform to avoid re-using the
        # same label names for each split
        @beam.ptransform_fn
        def _build_pcollection(pipeline):
            """PTransformation which build a single split."""
            # Encode the PCollection
            pcoll_examples = self._build_pcollection(pipeline, **split_generator.gen_kwargs)
            pcoll_examples |= "Encode" >> beam.Map(lambda key_ex: (key_ex[0], encode_example(key_ex[1])))
            return beam_writer.write_from_pcollection(pcoll_examples)

        # Add the PCollection to the pipeline
        _ = pipeline | split_name >> _build_pcollection()  # pylint: disable=no-value-for-parameter
