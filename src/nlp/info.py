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
from typing import ClassVar, List, NamedTuple, Optional

from .features import Features, FeatureType, Sequence
from .splits import SplitDict, check_splits_equals


logger = logging.getLogger(__name__)

# Name of the file to output the DatasetInfo p rotobuf object.
DATASET_INFO_FILENAME = "dataset_info.json"
LICENSE_FILENAME = "LICENSE"
METRIC_INFO_FILENAME = "metric_info.json"


class SupervisedKeysData(NamedTuple):
    input: str = ""
    output: str = ""


class DownloadChecksumsEntryData(NamedTuple):
    key: str = ""
    value: str = ""


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
    name: Optional[str] = None
    version: Optional[str] = None
    splits: Optional[dict] = field(default_factory=SplitDict)
    size_in_bytes: int = 0
    download_size: int = 0
    download_checksums: List[DownloadChecksumsEntryData] = field(default_factory=list)

    def __post_init__(self):
        # Convert back to the correct classes when we reload from dict
        if self.features is not None and not isinstance(self.features, Features):
            self.features = Features.from_dict(self.features)
        if self.supervised_keys is not None and not isinstance(self.supervised_keys, SupervisedKeysData):
            self.supervised_keys = SupervisedKeysData(*self.supervised_keys)
        if self.splits is not None and not isinstance(self.splits, SplitDict):
            self.splits = SplitDict.from_split_dict(self.splits)
        if self.download_checksums and not isinstance(self.download_checksums[0], DownloadChecksumsEntryData):
            self.download_checksums = [DownloadChecksumsEntryData(*args) for args in self.download_checksums]

    @property
    def dataset_size(self):
        """Generated dataset files size, in bytes."""
        # For old datasets, maybe empty.
        return sum(split.num_bytes for split in self.splits.values())

    def update_splits_if_different(self, split_dict):
        """Overwrite the splits if they are different from the current ones.

        * If splits aren't already defined or different (ex: different number of
            shards), then the new split dict is used. This will trigger stats
            computation during download_and_prepare.
        * If splits are already defined in DatasetInfo and similar (same names and
            shards): keep the restored split which contains the statistics (restored
            from GCS or file)

        Args:
            split_dict: `nlp.SplitDict`, the new split
        """
        assert isinstance(split_dict, SplitDict)

        # If splits are already defined and identical, then we do not update
        if self.splits and check_splits_equals(self.splits, split_dict):
            return

        self.splits = split_dict.copy()

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
    predictions_features: FeatureType
    references_features: Optional[FeatureType] = None
    inputs_description: str = field(default_factory=str)
    homepage: str = field(default_factory=str)
    licence: str = field(default_factory=str)
    codebase_urls: List[str] = field(default_factory=list)
    reference_urls: List[str] = field(default_factory=list)
    streamable: bool = False

    # Set later by the builder
    name: Optional[str] = None
    version: Optional[str] = None

    # Automatically constructed
    features: ClassVar[Features] = None

    def __post_init__(self):
        assert isinstance(self.predictions_features, Sequence)
        feat_dic = {
            "predictions": self.predictions_features.feature
        }  # Remove the batch axis for our Arrow table schema
        if self.references_features is not None:
            assert isinstance(self.references_features, Sequence)
            feat_dic.update(
                {"references": self.references_features.feature}
            )  # Remove the batch axis for our Arrow table schema
        self.features = Features(feat_dic)

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
