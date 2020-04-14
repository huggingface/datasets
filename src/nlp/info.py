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
 - schema
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

import abc
import collections
import json
import logging
import os
import shutil
import tempfile
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import numpy as np
import posixpath
from dataclasses_json import dataclass_json

from .splits import SplitDict, check_splits_equals

logger = logging.getLogger(__name__)

# Name of the file to output the DatasetInfo p rotobuf object.
DATASET_INFO_FILENAME = "dataset_info.json"
LICENSE_FILENAME = "LICENSE"

INFO_STR = """DatasetInfo(
        name='{name}',
        version={version},
        description='{description}',
        homepage='{homepage}',
        features={features},
        total_num_examples={total_num_examples},
        splits={splits},
        supervised_keys={supervised_keys},
        citation={citation},
        license={license},
)
"""


##### Replacing the p roto buff with a bunch of dataclasses for now
@dataclass
class SupervisedKeysData:
    input: str = ""
    output: str = ""


@dataclass
class RedistributionInfoData:
    license: str = ""

@dataclass
class DownloadChecksumsEntryData:
    key: str = ""
    value: str = ""

@dataclass_json
@dataclass
class DatasetInfoData:
    name: str = ""
    description: str = ""
    version: str = ""
    size_in_bytes: int = 0
    download_size: int = 0
    citation: Optional[str] = None
    homepage: Optional[str] = None
    license: Optional[str] = None
    splits: dict = field(default_factory=dict)
    supervised_keys: Optional[SupervisedKeysData] = None
    download_checksums: List[DownloadChecksumsEntryData] = field(default_factory=list)
    schema: Dict[str, Any] = field(default_factory=dict)


# TODO(nlp): Do we require to warn the user about the peak memory used while
# constructing the dataset?
class DatasetInfo(object):
    """Information about a dataset.

    `DatasetInfo` documents datasets, including its name, version, and features.
    See the constructor arguments and properties for a full list.

    Note: Not all fields are known on construction and may be updated later
    by `compute_dynamic_properties`. For example: the min and max values of a
    feature is typically updated during data generation (i.e. on calling
    builder.download_and_prepare()`).
    """

    def __init__(self,
                    builder,
                    description=None,
                    features=None,
                    supervised_keys=None,
                    homepage=None,
                    citation=None,
                    metadata=None,
                    license=None):
        """Constructs DatasetInfo.

        Args:
            builder: `DatasetBuilder`, dataset builder for this info.
            description: `str`, description of this dataset.
            features: `nlp.features.FeaturesDict`, Information on the feature dict
                of the `Dataset()` object from the `builder.as_dataset()`
                method.
            supervised_keys: `tuple` of `(input_key, target_key)`, Specifies the
                input feature and the label for supervised learning, if applicable for
                the dataset. The keys correspond to the feature names to select in
                `info.features`. When calling `nlp.DatasetBuilder.as_dataset()`
                with `as_supervised=True`, the `Dataset` object will yield
                the (input, target) defined here.
            homepage: `str`, optional, the homepage for this dataset.
            citation: `str`, optional, the citation to use for this dataset.
            metadata: dict, additonal object which will be
                stored/restored with the dataset. This allows for storing additional
                information with the dataset.
            license: `str`, optional,  will automatically be written to a
                LICENSE file stored with the dataset.
        """
        self._builder = builder

        self._info_data = DatasetInfoData(
                name=builder.name,
                description=description,
                version=str(builder._version),  # pylint: disable=protected-access
                citation=citation,
                homepage=homepage,
                splits=SplitDict(builder.name),
                license=license)

        if supervised_keys is not None:
            assert isinstance(supervised_keys, tuple)
            assert len(supervised_keys) == 2
            self._info_data.supervised_keys = SupervisedKeysData(input=supervised_keys[0],
                                                                 output=supervised_keys[1])

        self._features = features

        self._metadata = metadata

    @property
    def data(self):
        return self._info_data

    @property
    def name(self):
        return self.data.name

    @property
    def full_name(self):
        """Full canonical name: (<dataset_name>/<config_name>/<version>)."""
        names = [self._builder.name]
        if self._builder.builder_config:
            names.append(self._builder.builder_config.name)
        names.append(str(self.version))
        return posixpath.join(*names)

    @property
    def description(self):
        return self.data.description

    @property
    def version(self):
        return self._builder.version

    @property
    def homepage(self):
        return self.data.homepage

    @property
    def citation(self):
        return self.data.citation

    @property
    def data_dir(self):
        return self._builder.data_dir

    @property
    def dataset_size(self):
        """Generated dataset files size, in bytes."""
        # For old datasets, maybe empty.
        return sum(split.num_bytes for split in self.splits.values())

    @property
    def download_size(self):
        """Downloaded files size, in bytes."""
        # Fallback to deprecated `size_in_bytes` if `download_size` is empty.
        return self.data.download_size or self.data.size_in_bytes

    @download_size.setter
    def download_size(self, size):
        self.data.download_size = size

    @property
    def features(self):
        return self._features

    @property
    def metadata(self):
        return self._metadata

    @property
    def supervised_keys(self):
        if not self.data.supervised_keys is not None:
            return None
        supervised_keys = self.data.supervised_keys
        return (supervised_keys.input, supervised_keys.output)

    @property
    def license(self):
        return self.data.license

    @property
    def splits(self):
        return self.data.splits

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
        if self.splits and check_splits_equals(
                self.splits, split_dict):
            return

        self.data.splits = split_dict.copy()

    def _dataset_info_path(self, dataset_info_dir):
        return os.path.join(dataset_info_dir, DATASET_INFO_FILENAME)

    def _license_path(self, dataset_info_dir):
        return os.path.join(dataset_info_dir, LICENSE_FILENAME)

    def write_to_directory(self, dataset_info_dir):
        """Write `DatasetInfo` as JSON to `dataset_info_dir`."""
        # Save the metadata from the features (vocabulary, labels,...)
        if self.features:
            self.features.save_metadata(dataset_info_dir)

        # Save any additional metadata
        if self.metadata is not None:
            self.metadata.save_metadata(dataset_info_dir)

        if self.data.license:
            with open(self._license_path(dataset_info_dir), "w") as f:
                f.write(self.data.license)

        with open(self._dataset_info_path(dataset_info_dir), "w") as f:
            f.write(self.data.to_json())

    def read_from_directory(self, dataset_info_dir):
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
            raise ValueError(
                    "Calling read_from_directory with undefined dataset_info_dir.")

        dataset_info_path = self._dataset_info_path(dataset_info_dir)

        with open(dataset_info_path, "r") as f:
            # # Parse it back.
            dataset_info_json_str = f.read()
            self._info_data = DatasetInfoData.from_json(dataset_info_json_str)

        # Make sure we have a SplitDict back
        split_dict = self._info_data.splits
        self._info_data.splits = SplitDict.from_split_dict(split_dict)

        # Restore the feature metadata (vocabulary, labels names,...)
        if self.features:
            self.features.load_metadata(dataset_info_dir)

        if self.metadata is not None:
            self.metadata.load_metadata(dataset_info_dir)

        if self._builder._version != self.version:  # pylint: disable=protected-access
            raise AssertionError(
                    "The constructed DatasetInfo instance and the restored proto version "
                    "do not match. Builder version: {}. Proto version: {}".format(
                            self._builder._version, self.version))  # pylint: disable=protected-access

    def __repr__(self):
        splits_pprint = _indent("\n".join(["{"] + [
                "    '{}': {},".format(k, split.num_examples)
                for k, split in sorted(self.splits.items())
        ] + ["}"]))
        features_pprint = _indent(repr(self.features))
        citation_pprint = _indent('"""{}"""'.format(self.citation.strip()))
        return INFO_STR.format(
                name=self.name,
                version=self.version,
                description=self.description,
                total_num_examples=self.splits.total_num_examples,
                features=features_pprint,
                splits=splits_pprint,
                citation=citation_pprint,
                homepage=self.homepage,
                supervised_keys=self.supervised_keys,
                # Proto add a \n that we strip.
                license=str(self.license).strip())


def _indent(content):
    """Add indentation to all lines except the first."""
    lines = content.split("\n")
    return "\n".join([lines[0]] + ["    " + l for l in lines[1:]])
