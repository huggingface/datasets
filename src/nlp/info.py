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
"""DatasetInfo records the information we know about a dataset.

This includes things that we know about the dataset statically, i.e.:
 - description
 - canonical location
 - does it have validation and tests splits
 - size
 - etc.

This also includes the things that can and should be computed once we've
processed the dataset as well:
 - number of examples (in each split)
 - feature statistics (in each split)
 - etc.
"""

import logging
import os
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

from .splits import SplitDict, check_splits_equals
from .features import Features

logger = logging.getLogger(__name__)

# Name of the file to output the DatasetInfo p rotobuf object.
DATASET_INFO_FILENAME = "dataset_info.json"
LICENSE_FILENAME = "LICENSE"

# Replacing the p roto buff with a bunch of dataclasses for now
@dataclass
class SupervisedKeysData:
    input: str = ""
    output: str = ""


@dataclass
class DownloadChecksumsEntryData:
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
            self.supervised_keys = SupervisedKeysData(**self.supervised_keys)
        if self.splits is not None and not isinstance(self.splits, SplitDict):
            self.splits = SplitDict.from_split_dict(self.splits)
        if self.download_checksums and not isinstance(self.download_checksums[0], SupervisedKeysData):
            self.supervised_keys = [SupervisedKeysData(**kwargs) for kwargs in self.supervised_keys]


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
            # f.write(self.to_json())

        with open(os.path.join(dataset_info_dir, LICENSE_FILENAME), "w") as f:
            f.write(self.license)

    @classmethod
    def from_directory(cls, dataset_info_dir):
        """Update DatasetInfo from the JSON file in `dataset_info_dir`.

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
