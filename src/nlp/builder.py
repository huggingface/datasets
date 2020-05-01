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
"""DatasetBuilder base class."""

import abc
import contextlib
import functools
import inspect
import itertools
import logging
import os
import shutil
from dataclasses import dataclass, field

from . import splits as splits_lib
from . import utils
from .arrow_reader import ArrowReader
from .arrow_writer import ArrowWriter, BeamWriter
from .info import DatasetInfo
from .lazy_imports_lib import lazy_imports
from .naming import filename_prefix_for_split
from .utils import Version
from .utils.download_manager import DownloadConfig, DownloadManager, GenerateMode
from .utils.file_utils import HF_DATASETS_CACHE


logger = logging.getLogger(__name__)

FORCE_REDOWNLOAD = GenerateMode.FORCE_REDOWNLOAD
REUSE_CACHE_IF_EXISTS = GenerateMode.REUSE_CACHE_IF_EXISTS
REUSE_DATASET_IF_EXISTS = GenerateMode.REUSE_DATASET_IF_EXISTS


@dataclass
class BuilderConfig:
    """Base class for `DatasetBuilder` data configuration.

    DatasetBuilder subclasses with data configuration options should subclass
    `BuilderConfig` and add their own properties.
    """

    name: str
    version: Version
    supported_versions: list = field(default_factory=list)
    description: str = ""


class DatasetBuilder:
    """Abstract base class for all datasets.

    `DatasetBuilder` has 3 key methods:

        * `nlp.DatasetBuilder.info`: documents the dataset, including feature
            names, types, and shapes, version, splits, citation, etc.
        * `nlp.DatasetBuilder.download_and_prepare`: downloads the source data
            and writes it to disk.
        * `nlp.DatasetBuilder.as_dataset`: generate an `Dataset`.

    **Configuration**: Some `DatasetBuilder`s expose multiple variants of the
    dataset by defining a `nlp.BuilderConfig` subclass and accepting a
    config object (or name) on construction. Configurable datasets expose a
    pre-defined set of configurations in `nlp.DatasetBuilder.builder_configs`.

    Typical `DatasetBuilder` usage:

    ```python
    mnist_builder = nlp.builder("mnist")
    mnist_info = mnist_builder.info
    mnist_builder.download_and_prepare()
    datasets = mnist_builder.as_dataset()

    train_dataset, test_dataset = datasets["train"], datasets["test"]
    assert isinstance(train_dataset, Dataset`)

    # And then the rest of your input pipeline
    train_dataset = train_dataset.repeat().shuffle(1024).batch(128)
    train_dataset = train_dataset.prefetch(2)
    features = tf.compat.v1.data.make_one_shot_iterator(train_dataset).get_next()
    image, label = features['image'], features['label']
    ```
    """

    # Name of the dataset, filled by metaclass based on class name.
    name = None

    # Semantic version of the dataset (ex: nlp.Version('1.2.0'))
    VERSION = None

    # List dataset versions which can be loaded using current code.
    # Data can only be prepared with canonical VERSION or above.
    SUPPORTED_VERSIONS = []

    # Named configurations that modify the data generated by download_and_prepare.
    BUILDER_CONFIGS = []

    # Must be set for datasets that use 'manual_dir' functionality - the ones
    # that require users to do additional steps to download the data
    # (this is usually due to some external regulations / rules).
    #
    # This field should contain a string with user instructions, including
    # the list of files that should be present. It will be
    # displayed in the dataset documentation.
    MANUAL_DOWNLOAD_INSTRUCTIONS = None

    def __init__(self, data_dir=None, config=None, version=None):
        """Constructs a DatasetBuilder.

        Callers must pass arguments as keyword arguments.

        Args:
            data_dir: `str`, directory to read/write data. Defaults to
                "~/nlp".
            config: `nlp.BuilderConfig` or `str` name, optional configuration
                for the dataset that affects the data generated on disk. Different
                `builder_config`s will have their own subdirectories and versions.
            version: `str`. Optional version at which to load the dataset. An error is
                raised if specified version cannot be satisfied. Eg: '1.2.3', '1.2.*'.
                The special value "experimental_latest" will use the highest version,
                even if not default. This is not recommended unless you know what you
                are doing, as the version could be broken.
        """
        # For pickling:
        self._original_state = dict(data_dir=data_dir, config=config, version=version)
        # To do the work:
        self._builder_config = self._create_builder_config(config)
        # Extract code version (VERSION or config)
        if not self._builder_config and not self.VERSION:
            raise AssertionError(
                "DatasetBuilder {} does not have a defined version. Please add a "
                "`VERSION = nlp.Version('x.y.z')` to the class.".format(self.name)
            )

        # Prepare version: TODO: can still be cleaned up
        self.canonical_version = self._builder_config.version if self._builder_config else self.VERSION
        self.supported_versions = (
            self._builder_config.supported_versions if self._builder_config else self.SUPPORTED_VERSIONS
        )
        self.versions = [
            utils.Version(v) if isinstance(v, str) else v for v in [self.canonical_version] + self.supported_versions
        ]
        if version == "experimental_latest":
            self._version = max(self.versions)
        else:
            for vers in self.versions:
                if version is None or version.match(vers):
                    self._version = vers
                    break

        # prepare info
        info = self._info()
        info.name = self.name
        info.version = self._version
        info.splits.dataset_name = self.name
        self.info = info

        # prepare data dirs
        self._data_dir_root = os.path.expanduser(data_dir or HF_DATASETS_CACHE)
        self._data_dir = self._build_data_dir()
        if os.path.exists(self._data_dir):
            logger.info("Overwrite dataset info from restored data version.")
            self.info = DatasetInfo.from_directory(self._data_dir)

    def __getstate__(self):
        return self._original_state

    def __setstate__(self, state):
        self.__init__(**state)

    @property
    def builder_config(self):
        """`nlp.BuilderConfig` for this builder."""
        return self._builder_config

    def _create_builder_config(self, builder_config):
        """Create and validate BuilderConfig object."""
        if builder_config is None and self.BUILDER_CONFIGS:
            builder_config = self.BUILDER_CONFIGS[0]
            logger.info("No config specified, defaulting to first: %s/%s", self.name, builder_config.name)
        if not builder_config:
            return None
        if isinstance(builder_config, str):
            name = builder_config
            builder_config = self.builder_configs.get(name)
            if builder_config is None:
                raise ValueError(
                    "BuilderConfig %s not found. Available: %s" % (name, list(self.builder_configs.keys()))
                )
        name = builder_config.name
        if not name:
            raise ValueError("BuilderConfig must have a name, got %s" % name)
        is_custom = name not in self.builder_configs
        if is_custom:
            logger.warning("Using custom data configuration %s", name)
        else:
            if builder_config is not self.builder_configs[name]:
                raise ValueError(
                    "Cannot name a custom BuilderConfig the same as an available "
                    "BuilderConfig. Change the name. Available BuilderConfigs: %s"
                    % (list(self.builder_configs.keys()))
                )
            if not builder_config.version:
                raise ValueError("BuilderConfig %s must have a version" % name)
            if not builder_config.description:
                raise ValueError("BuilderConfig %s must have a description" % name)
        return builder_config

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
    def version(self):
        return self._version

    @property
    def data_dir(self):
        return self._data_dir

    def _relative_data_dir(self, with_version=True):
        """Relative path of this dataset in data_dir."""
        builder_data_dir = self.name
        builder_config = self._builder_config
        if builder_config:
            builder_data_dir = os.path.join(builder_data_dir, builder_config.name)
        if not with_version:
            return builder_data_dir

        version = self._version
        version_data_dir = os.path.join(builder_data_dir, str(version))
        return version_data_dir

    def _build_data_dir(self):
        """Return the data directory for the current version."""
        builder_data_dir = os.path.join(self._data_dir_root, self._relative_data_dir(with_version=False))
        version_data_dir = os.path.join(self._data_dir_root, self._relative_data_dir(with_version=True))

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
            if other_version != self._version:
                warn_msg = (
                    "Found a different version {other_version} of dataset {name} in "
                    "data_dir {data_dir}. Using currently defined version "
                    "{cur_version}.".format(
                        other_version=str(other_version),
                        name=self.name,
                        data_dir=self._data_dir_root,
                        cur_version=str(self._version),
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

    def download_and_prepare(self, download_dir=None, download_config=None):
        """Downloads and prepares dataset for reading.

        Args:
            download_dir: `str`, directory where downloaded files are stored.
            download_config: `nlp.DownloadConfig`, further configuration for
                downloading and preparing dataset.

        Raises:
            IOError: if there is not enough disk space available.
        """

        download_config = download_config or DownloadConfig()
        data_exists = os.path.exists(self._data_dir)
        if data_exists and download_config.download_mode == REUSE_DATASET_IF_EXISTS:
            logger.info("Reusing dataset %s (%s)", self.name, self._data_dir)
            return

        # Currently it's not possible to overwrite the data because it would
        # conflict with versioning: If the last version has already been generated,
        # it will always be reloaded and data_dir will be set at construction.
        if data_exists:
            raise ValueError(
                "Trying to overwrite an existing dataset {} at {}. A dataset with "
                "the same version {} already exists. If the dataset has changed, "
                "please update the version number.".format(self.name, self._data_dir, self.version)
            )

        logger.info("Generating dataset %s (%s)", self.name, self._data_dir)
        if not utils.has_sufficient_disk_space(
            self.info.dataset_size + self.info.download_size, directory=self._data_dir_root
        ):
            raise IOError(
                "Not enough disk space. Needed: {} (download: {}, generated: {})".format(
                    utils.size_str(self.info.dataset_size + self.info.download_size),
                    utils.size_str(self.info.download_size),
                    utils.size_str(self.info.dataset_size),
                )
            )

        # Print is intentional: we want this to always go to stdout so user has
        # information needed to cancel download/preparation if needed.
        # This comes right before the progress bar.
        print(
            "Downloading and preparing dataset {} (download: {}, generated: {}, "
            "total: {}) to {}...".format(
                self.info.name,
                utils.size_str(self.info.download_size),
                utils.size_str(self.info.dataset_size),
                utils.size_str(self.info.download_size + self.info.dataset_size),
                self._data_dir,
            )
        )

        dl_manager = self._make_download_manager(download_dir=download_dir, download_config=download_config)

        @contextlib.contextmanager
        def incomplete_dir(dirname):
            """Create temporary dir for dirname and rename on exit."""
            tmp_dir = dirname + ".incomplete"
            os.makedirs(tmp_dir)
            try:
                yield tmp_dir
                os.rename(tmp_dir, dirname)
            finally:
                if os.path.exists(tmp_dir):
                    shutil.rmtree(tmp_dir)

        # Create a tmp dir and rename to self._data_dir on successful exit.
        with incomplete_dir(self._data_dir) as tmp_data_dir:
            # Temporarily assign _data_dir to tmp_data_dir to avoid having to forward
            # it to every sub function.
            with utils.temporary_assignment(self, "_data_dir", tmp_data_dir):
                self._download_and_prepare(dl_manager=dl_manager, download_config=download_config)

                # NOTE: If modifying the lines below to put additional information in
                # DatasetInfo, you'll likely also want to update
                # DatasetInfo.from_directory to possibly restore these attributes
                # when reading from package data.

                # splits = list(self.info.splits.values())
                # statistics_already_computed = bool(
                #         splits and splits[0].num_examples)
                # # Update DatasetInfo metadata by computing statistics from the data.
                # if (download_config.compute_stats == download.ComputeStatsMode.SKIP or
                #         download_config.compute_stats == download.ComputeStatsMode.AUTO
                #         and statistics_already_computed
                #         ):
                #     logger.info(
                #             "Skipping computing stats for mode %s.",
                #             download_config.compute_stats)
                # else:  # Mode is forced or stats do not exists yet
                #     logger.info("No statistics computed for now.")
                # self.info.compute_dynamic_properties()
                self.info.download_size = dl_manager.downloaded_size
                # Write DatasetInfo to disk, even if we haven't computed statistics.
                self.info.write_to_directory(self._data_dir)

        msg = (
            "Dataset {name} downloaded and prepared to {data_dir}. " "Subsequent calls will reuse this data."
        ).format(name=self.name, data_dir=self._data_dir,)
        print(msg)

    def _download_and_prepare(self, dl_manager, **prepare_split_kwargs):
        """Downloads and prepares dataset for reading.

        This is the internal implementation to overwrite called when user calls
        `download_and_prepare`. It should download all required data and generate
        the pre-processed datasets files.

        Args:
            dl_manager: (DownloadManager) `DownloadManager` used to download and cache
                data.
            download_config: `DownloadConfig`, Additional options.
        """
        os.makedirs(self._data_dir, exist_ok=True)

        # Generating data for all splits
        split_dict = splits_lib.SplitDict(dataset_name=self.name)
        split_generators_kwargs = self._make_split_generators_kwargs(prepare_split_kwargs)
        for split_generator in self._split_generators(dl_manager, **split_generators_kwargs):
            if str(split_generator.split_info.name).lower() == "all":
                raise ValueError(
                    "`all` is a special split keyword corresponding to the "
                    "union of all splits, so cannot be used as key in "
                    "._split_generator()."
                )

            logger.info("Generating split %s", split_generator.split_info.name)
            split_dict.add(split_generator.split_info)

            # Prepare split will record examples associated to the split
            self._prepare_split(split_generator, **prepare_split_kwargs)

        # Update the info object with the splits.
        self.info.update_splits_if_different(split_dict)

    def _make_download_manager(self, download_dir, download_config):
        """Creates a new download manager object."""
        download_dir = download_dir or os.path.join(self._data_dir_root, "downloads")

        # Use manual_dir only if MANUAL_DOWNLOAD_INSTRUCTIONS are set.
        if self.MANUAL_DOWNLOAD_INSTRUCTIONS:
            manual_dir = download_config.manual_dir or os.path.join(download_dir, "manual")
            manual_dir = os.path.join(manual_dir, self.name)
        else:
            manual_dir = None

        return DownloadManager(
            dataset_name=self.name,
            download_dir=download_dir,
            manual_dir=manual_dir,
            manual_dir_instructions=self.MANUAL_DOWNLOAD_INSTRUCTIONS,
            force_download=(download_config.download_mode == FORCE_REDOWNLOAD),
            register_checksums=download_config.register_checksums,
        )

    def _make_split_generators_kwargs(self, prepare_split_kwargs):
        """Get kwargs for `self._split_generators()` from `prepare_split_kwargs`."""
        del prepare_split_kwargs
        return {}

    def as_dataset(self, split=None, batch_size=None, as_supervised=False):
        logger.info("Constructing Dataset for split %s, from %s", split, self._data_dir)
        if not os.path.exists(self._data_dir):
            raise AssertionError(
                (
                    "Dataset %s: could not find data in %s. Please make sure to call "
                    "builder.download_and_prepare(), or pass download=True to "
                    "nlp.load() before trying to access the Dataset object."
                )
                % (self.name, self._data_dir_root)
            )

        # By default, return all splits
        if split is None:
            split = {s: s for s in self.info.splits}

        # Create a dataset for each of the given splits
        build_single_dataset = functools.partial(
            self._build_single_dataset, batch_size=batch_size, as_supervised=as_supervised,
        )
        datasets = utils.map_nested(build_single_dataset, split, map_tuple=True)
        return datasets

    def _build_single_dataset(self, split, batch_size, as_supervised):
        """as_dataset for a single split."""
        if isinstance(split, str):
            split = splits_lib.Split(split)

        # Build base dataset
        ds = self._as_dataset(split=split,)
        return ds

    def _as_dataset(self, split=splits_lib.Split.TRAIN):
        """Constructs a `Dataset`.

        This is the internal implementation to overwrite called when user calls
        `as_dataset`. It should read the pre-processed datasets files and generate
        the `Dataset` object.

        Args:
            split: `nlp.Split` which subset of the data to read.

        Returns:
            `Dataset`
        """

        ds = ArrowReader(self._data_dir, self.info).read(
            name=self.name, instructions=split, split_infos=self.info.splits.values(),
        )
        return ds

    @abc.abstractmethod
    def _split_generators(self, dl_manager):
        """Specify feature dictionary generators and dataset splits.

        This function returns a list of `SplitGenerator`s defining how to generate
        data and what splits to use.

        Example:

            return[
                    nlp.SplitGenerator(
                            name=nlp.Split.TRAIN,
                            gen_kwargs={'file': 'train_data.zip'},
                    ),
                    nlp.SplitGenerator(
                            name=nlp.Split.TEST,
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
    def _prepare_split(self, split_generator, **kwargs):
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

    def _download_and_prepare(self, dl_manager, download_config):
        # Extract max_examples_per_split and forward it to _prepare_split
        super(GeneratorBasedBuilder, self)._download_and_prepare(
            dl_manager=dl_manager, max_examples_per_split=download_config.max_examples_per_split,
        )

    def _prepare_split(self, split_generator, max_examples_per_split):
        generator = self._generate_examples(**split_generator.gen_kwargs)
        split_info = split_generator.split_info
        if max_examples_per_split is not None:
            logger.warning("Splits capped at %s examples max.", max_examples_per_split)
            generator = itertools.islice(generator, max_examples_per_split)
        fname = "{}-{}.arrow".format(self.name, split_generator.name)
        fpath = os.path.join(self._data_dir, fname)
        examples_type = self.info.features.type
        writer = ArrowWriter(data_type=examples_type, path=fpath)
        for key, record in utils.tqdm(generator, unit=" examples", total=split_info.num_examples, leave=False):
            example = self.info.features.encode_example(record)
            writer.write(example)
        num_examples, num_bytes = writer.finalize()
        assert num_examples == num_examples, f"Expected to write {split_info.num_examples} but wrote {num_examples}"
        split_generator.split_info.num_examples = num_examples
        split_generator.split_info.num_bytes = num_bytes


class BeamBasedBuilder(DatasetBuilder):
    """Beam based Builder."""

    def __init__(self, *args, **kwargs):
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
        which will be read (download_dir, manual_dir,...) and written (data_dir)
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

    def _download_and_prepare(self, dl_manager, download_config):
        # Create the Beam pipeline and forward it to _prepare_split
        beam = lazy_imports.apache_beam

        if not download_config.beam_runner and not download_config.beam_options:
            raise ValueError(
                "Trying to generate a dataset using Apache Beam, yet no Beam Runner "
                "or PipelineOptions() has been provided. Please pass a "
                "nlp.DownloadConfig(beam_runner=...) object to the "
                "builder.download_and_prepare(download_config=...) method"
            )

        beam_options = download_config.beam_options or beam.options.pipeline_options.PipelineOptions()
        # Beam type checking assumes transforms multiple outputs are of same type,
        # which is not our case. Plus it doesn't handle correctly all types, so we
        # are better without it.
        beam_options.view_as(beam.options.pipeline_options.TypeOptions).pipeline_type_check = False
        # Use a single pipeline for all splits
        with beam.Pipeline(runner=download_config.beam_runner, options=beam_options,) as pipeline:
            # TODO(nlp): Should eventually try to add support to
            # download_config.max_examples_per_split
            super(BeamBasedBuilder, self)._download_and_prepare(
                dl_manager, pipeline=pipeline,
            )

        # Update `info.splits` with number of shards and shard lengths.
        split_dict = self.info.splits
        for split_name, beam_writer in self._beam_writers.items():
            logger.info("Retrieving shard lengths for %s...", split_name)
            shard_lengths, total_size = beam_writer.finalize()
            split_info = split_dict[split_name]
            split_info.shard_lengths.extend(shard_lengths)
            split_info.num_shards = len(shard_lengths)
            split_info.num_bytes = total_size
        logger.info("Updating split info...")
        self.info.update_splits_if_different(split_dict)

    def _prepare_split(self, split_generator, pipeline):
        beam = lazy_imports.apache_beam

        os.makedirs(self._data_dir, exist_ok=True)

        split_name = split_generator.split_info.name
        output_prefix = filename_prefix_for_split(self.name, split_name)
        output_prefix = os.path.join(self._data_dir, output_prefix)

        # To write examples to disk:
        fname = "{}-{}.arrow".format(self.name, split_name)
        fpath = os.path.join(self._data_dir, fname)
        examples_type = self.info.features.get_type()
        beam_writer = BeamWriter(examples_type, fpath, hash_salt=split_name)
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
