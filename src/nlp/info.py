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
""" DatasetInfo and MetricInfo record information we know about a dataset and a metric.

This includes things that we know about the dataset statically, i.e.:
 - description
 - canonical location
 - does it have validation and tests splits
 - size
 - etc.

This also includes the things that can and should be computed once we've
processed the dataset as well:
 - number of examples (in each split)
 - etc.
"""

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Union

from nlp.utils.checksums_utils import (
    CACHED_SIZES_FILE_NAME,
    CHECKSUMS_FILE_NAME,
    load_cached_sizes,
    load_sizes_checksums,
    store_cached_sizes,
)
from nlp.utils.version import Version

from .features import Features, Value
from .splits import SplitDict


logger = logging.getLogger(__name__)

# Name of the file to output the DatasetInfo p rotobuf object.
DATASET_INFO_FILENAME = "dataset_info.json"
LICENSE_FILENAME = "LICENSE"
METRIC_INFO_FILENAME = "metric_info.json"


@dataclass
class SupervisedKeysData:
    input: str = ""
    output: str = ""


@dataclass
class DownloadChecksumsEntryData:
    key: str = ""
    value: str = ""


class MissingCachedSizesConfigError(Exception):
    """The expected cached sizes of the download file are missing."""


class NonMatchingCachedSizesError(Exception):
    """The prepared split doesn't have expected sizes."""


@dataclass
class DatasetInfo:
    """Information about a dataset.

    `DatasetInfo` documents datasets, including its name, version, and features.
    See the constructor arguments and properties for a full list.

    Note: Not all fields are known on construction and may be updated later.
    """

    # Set in the dataset scripts
    description: str = field(default_factory=str)
    citation: str = field(default_factory=str)
    homepage: str = field(default_factory=str)
    license: str = field(default_factory=str)
    features: Features = None
    supervised_keys: Optional[SupervisedKeysData] = None

    # Set later by the builder
    builder_name: Optional[str] = None
    config_name: Optional[str] = None
    version: Optional[Union[str, Version]] = None
    splits: Optional[dict] = field(default_factory=SplitDict)
    size_in_bytes: int = 0
    download_size: int = 0
    dataset_size: int = 0
    download_checksums: dict = field(default_factory=dict)

    def __post_init__(self):
        # Convert back to the correct classes when we reload from dict
        if self.features is not None and not isinstance(self.features, Features):
            self.features = Features.from_dict(self.features)
        if self.version is not None and not isinstance(self.version, Version):
            if isinstance(self.version, str):
                self.version = Version(self.version)
            else:
                self.version = Version.from_dict(self.version)
        if self.splits is not None and not isinstance(self.splits, SplitDict):
            self.splits = SplitDict.from_split_dict(self.splits)
        if self.supervised_keys is not None and not isinstance(self.supervised_keys, SupervisedKeysData):
            if isinstance(self.supervised_keys, (tuple, list)):
                self.supervised_keys = SupervisedKeysData(*self.supervised_keys)
            else:
                self.supervised_keys = SupervisedKeysData(**self.supervised_keys)

    def _license_path(self, dataset_info_dir):
        return os.path.join(dataset_info_dir, LICENSE_FILENAME)

    def write_to_directory(self, dataset_info_dir):
        """ Write `DatasetInfo` as JSON to `dataset_info_dir`.
            Also save the license separately in LICENCE.
        """
        with open(os.path.join(dataset_info_dir, DATASET_INFO_FILENAME), "w") as f:
            json.dump(asdict(self), f)

        with open(os.path.join(dataset_info_dir, LICENSE_FILENAME), "w") as f:
            f.write(self.license)

    @classmethod
    def from_directory(cls, dataset_info_dir):
        """Create DatasetInfo from the JSON file in `dataset_info_dir`.

        This function updates all the dynamically generated fields (num_examples,
        hash, time of creation,...) of the DatasetInfo.

        This will overwrite all previous metadata.

        Args:
            dataset_info_dir: `str` The directory containing the metadata file. This
                should be the root directory of a specific dataset version.
        """
        logger.info("Loading Dataset info from %s", dataset_info_dir)
        if not dataset_info_dir:
            raise ValueError("Calling DatasetInfo.from_directory() with undefined dataset_info_dir.")

        with open(os.path.join(dataset_info_dir, DATASET_INFO_FILENAME), "r") as f:
            dataset_info_dict = json.load(f)
        return cls(**dataset_info_dict)

    def prefill_dataset_size_attributes_from_urls_checksums_dir(self, urls_checksums_dir: str):
        """Store upper bounds of dataset size if available"""
        checksums_file_path = os.path.join(urls_checksums_dir, CHECKSUMS_FILE_NAME)
        cached_sizes_file_path = os.path.join(urls_checksums_dir, CACHED_SIZES_FILE_NAME)
        if os.path.exists(checksums_file_path):
            self.download_checksums = load_sizes_checksums(checksums_file_path)
        if os.path.exists(cached_sizes_file_path):
            cached_sizes = load_cached_sizes(cached_sizes_file_path)
            self.dataset_size = sum(size_nexamples[0] for size_nexamples in cached_sizes.values())

    def cached_sizes(self):
        return {
            "/".join([str(self.builder_name), str(self.config_name), str(self.version), split_name]): (
                split_info.num_bytes,
                split_info.num_examples,
            )
            for split_name, split_info in self.splits.items()
        }

    def check_or_save_cached_sizes(self, urls_checksums_dir: str, ignore_cached_sizes: bool, save_cached_sizes):
        if not ignore_cached_sizes:
            cached_sizes_file_path = os.path.join(urls_checksums_dir, CACHED_SIZES_FILE_NAME)
            if save_cached_sizes:
                store_cached_sizes(self.cached_sizes(), cached_sizes_file_path)
                logger.info("Stored the recorded cached sizes in {}.".format(urls_checksums_dir))
            elif os.path.exists(cached_sizes_file_path):
                expected_cached_sizes = load_cached_sizes(cached_sizes_file_path)
                for full_config_name, rec_size_numexamples in self.cached_sizes().items():
                    exp_size_numexamples = expected_cached_sizes.get(full_config_name)
                    if exp_size_numexamples is None:
                        raise MissingCachedSizesConfigError(full_config_name)
                    if exp_size_numexamples != rec_size_numexamples:
                        raise NonMatchingCachedSizesError(full_config_name)
                logger.info("All cached sizes matched successfully.")
            else:
                logger.info("Cached sizes file not found.")
        else:
            logger.info("Cached sizes tests were ignored.")


@dataclass
class MetricInfo:
    """Information about a metric.

    `MetricInfo` documents a metric, including its name, version, and features.
    See the constructor arguments and properties for a full list.

    Note: Not all fields are known on construction and may be updated later.
    """

    # Set in the dataset scripts
    description: str
    citation: str
    features: Features
    inputs_description: str = field(default_factory=str)
    homepage: str = field(default_factory=str)
    licence: str = field(default_factory=str)
    codebase_urls: List[str] = field(default_factory=list)
    reference_urls: List[str] = field(default_factory=list)
    streamable: bool = False
    format: Optional[str] = None

    # Set later by the builder
    metric_name: Optional[str] = None
    config_name: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self):
        assert "predictions" in self.features, "Need to have at least a 'predictions' field in 'features'."
        if self.format is not None:
            for key, value in self.features.items():
                if not isinstance(value, Value):
                    raise ValueError(
                        f"When using 'numpy' format, all features should be a `nlp.Value` feature. "
                        f"Here {key} is an instance of {value.__class__.__name__}"
                    )

    def write_to_directory(self, metric_info_dir):
        """ Write `MetricInfo` as JSON to `metric_info_dir`.
            Also save the license separately in LICENCE.
        """
        with open(os.path.join(metric_info_dir, DATASET_INFO_FILENAME), "w") as f:
            json.dump(asdict(self), f)

        with open(os.path.join(metric_info_dir, LICENSE_FILENAME), "w") as f:
            f.write(self.license)

    @classmethod
    def from_directory(cls, metric_info_dir):
        """Create MetricInfo from the JSON file in `metric_info_dir`.

        Args:
            metric_info_dir: `str` The directory containing the metadata file. This
                should be the root directory of a specific dataset version.
        """
        logger.info("Loading Metric info from %s", metric_info_dir)
        if not metric_info_dir:
            raise ValueError("Calling MetricInfo.from_directory() with undefined metric_info_dir.")

        with open(os.path.join(metric_info_dir, METRIC_INFO_FILENAME), "r") as f:
            dataset_info_dict = json.load(f)
        return cls(**dataset_info_dict)
