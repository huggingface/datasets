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

import copy
import dataclasses
import json
import os
from dataclasses import asdict, dataclass, field
from typing import List, Optional, Union

from . import config
from .features import Features, Value
from .splits import SplitDict
from .tasks import TaskTemplate, task_template_from_dict
from .utils import Version
from .utils.logging import get_logger


logger = get_logger(__name__)


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
class PostProcessedInfo:
    features: Optional[Features] = None
    resources_checksums: Optional[dict] = None

    def __post_init__(self):
        # Convert back to the correct classes when we reload from dict
        if self.features is not None and not isinstance(self.features, Features):
            self.features = Features.from_dict(self.features)

    @classmethod
    def from_dict(cls, post_processed_info_dict: dict) -> "PostProcessedInfo":
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in post_processed_info_dict.items() if k in field_names})


@dataclass
class DatasetInfo:
    """Information about a dataset.

    `DatasetInfo` documents datasets, including its name, version, and features.
    See the constructor arguments and properties for a full list.

    Note: Not all fields are known on construction and may be updated later.

    Attributes:
        description (str): A description of the dataset.
        citation (str): A BibTeX citation of the dataset.
        homepage (str): A URL to the official homepage for the dataset.
        license (str): The dataset's license. It can be the name of the license or a paragraph containing the terms of the license.
        features (Features, optional): The features used to specify the dataset's column types.
        post_processed (PostProcessedInfo, optional): Information regarding the resources of a possible post-processing of a dataset. For example, it can contain the information of an index.
        supervised_keys (SupervisedKeysData, optional): Specifies the input feature and the label for supervised learning if applicable for the dataset (legacy from TFDS).
        builder_name (str, optional): The name of the :class:`GeneratorBasedBuilder` subclass used to create the dataset. Usually matched to the corresponding script name. It is also the snake_case version of the dataset builder class name.
        config_name (str, optional): The name of the configuration derived from :class:`BuilderConfig`
        version (str or Version, optional): The version of the dataset.
        splits (dict, optional): The mapping between split name and metadata.
        download_checksums (dict, optional): The mapping between the URL to download the dataset's checksums and corresponding metadata.
        download_size (int, optional): The size of the files to download to generate the dataset, in bytes.
        post_processing_size (int, optional): Size of the dataset in bytes after post-processing, if any.
        dataset_size (int, optional): The combined size in bytes of the Arrow tables for all splits.
        size_in_bytes (int, optional): The combined size in bytes of all files associated with the dataset (downloaded files + Arrow files).
        task_templates (List[TaskTemplate], optional): The task templates to prepare the dataset for during training and evaluation. Each template casts the dataset's :class:`Features` to standardized column names and types as detailed in :py:mod:`datasets.tasks`.
        **config_kwargs: Keyword arguments to be passed to the :class:`BuilderConfig` and used in the :class:`DatasetBuilder`.
    """

    # Set in the dataset scripts
    description: str = field(default_factory=str)
    citation: str = field(default_factory=str)
    homepage: str = field(default_factory=str)
    license: str = field(default_factory=str)
    features: Optional[Features] = None
    post_processed: Optional[PostProcessedInfo] = None
    supervised_keys: Optional[SupervisedKeysData] = None
    task_templates: Optional[List[TaskTemplate]] = None

    # Set later by the builder
    builder_name: Optional[str] = None
    config_name: Optional[str] = None
    version: Optional[Union[str, Version]] = None
    # Set later by `download_and_prepare`
    splits: Optional[dict] = None
    download_checksums: Optional[dict] = None
    download_size: Optional[int] = None
    post_processing_size: Optional[int] = None
    dataset_size: Optional[int] = None
    size_in_bytes: Optional[int] = None

    def __post_init__(self):
        # Convert back to the correct classes when we reload from dict
        if self.features is not None and not isinstance(self.features, Features):
            self.features = Features.from_dict(self.features)
        if self.post_processed is not None and not isinstance(self.post_processed, PostProcessedInfo):
            self.post_processed = PostProcessedInfo.from_dict(self.post_processed)
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

        if self.task_templates is not None:
            if isinstance(self.task_templates, (list, tuple)):
                templates = [
                    template if isinstance(template, TaskTemplate) else task_template_from_dict(template)
                    for template in self.task_templates
                ]
                self.task_templates = [template for template in templates if template is not None]
            elif isinstance(self.task_templates, TaskTemplate):
                self.task_templates = [self.task_templates]
            else:
                template = task_template_from_dict(self.task_templates)
                self.task_templates = [template] if template is not None else []

    def _license_path(self, dataset_info_dir):
        return os.path.join(dataset_info_dir, config.LICENSE_FILENAME)

    def write_to_directory(self, dataset_info_dir):
        """Write `DatasetInfo` as JSON to `dataset_info_dir`.

        Also save the license separately in LICENCE.
        """
        with open(os.path.join(dataset_info_dir, config.DATASET_INFO_FILENAME), "wb") as f:
            self._dump_info(f)

        with open(os.path.join(dataset_info_dir, config.LICENSE_FILENAME), "wb") as f:
            self._dump_license(f)

    def _dump_info(self, file):
        """Dump info in `file` file-like object open in bytes mode (to support remote files)"""
        file.write(json.dumps(asdict(self)).encode("utf-8"))

    def _dump_license(self, file):
        """Dump license in `file` file-like object open in bytes mode (to support remote files)"""
        file.write(self.license.encode("utf-8"))

    @classmethod
    def from_merge(cls, dataset_infos: List["DatasetInfo"]):
        def unique(values):
            seen = set()
            for value in values:
                if value not in seen:
                    seen.add(value)
                    yield value

        dataset_infos = [dset_info.copy() for dset_info in dataset_infos if dset_info is not None]
        description = "\n\n".join(unique(info.description for info in dataset_infos))
        citation = "\n\n".join(unique(info.citation for info in dataset_infos))
        homepage = "\n\n".join(unique(info.homepage for info in dataset_infos))
        license = "\n\n".join(unique(info.license for info in dataset_infos))
        features = None
        supervised_keys = None
        task_templates = None

        # Find common task templates across all dataset infos
        all_task_templates = [info.task_templates for info in dataset_infos if info.task_templates is not None]
        if len(all_task_templates) > 1:
            task_templates = list(set(all_task_templates[0]).intersection(*all_task_templates[1:]))
        elif len(all_task_templates):
            task_templates = list(set(all_task_templates[0]))
        # If no common task templates found, replace empty list with None
        task_templates = task_templates if task_templates else None

        return cls(
            description=description,
            citation=citation,
            homepage=homepage,
            license=license,
            features=features,
            supervised_keys=supervised_keys,
            task_templates=task_templates,
        )

    @classmethod
    def from_directory(cls, dataset_info_dir: str) -> "DatasetInfo":
        """Create DatasetInfo from the JSON file in `dataset_info_dir`.

        This function updates all the dynamically generated fields (num_examples,
        hash, time of creation,...) of the DatasetInfo.

        This will overwrite all previous metadata.

        Args:
            dataset_info_dir (`str`): The directory containing the metadata file. This
                should be the root directory of a specific dataset version.
        """
        logger.info("Loading Dataset info from %s", dataset_info_dir)
        if not dataset_info_dir:
            raise ValueError("Calling DatasetInfo.from_directory() with undefined dataset_info_dir.")

        with open(os.path.join(dataset_info_dir, config.DATASET_INFO_FILENAME), "r", encoding="utf-8") as f:
            dataset_info_dict = json.load(f)
        return cls.from_dict(dataset_info_dict)

    @classmethod
    def from_dict(cls, dataset_info_dict: dict) -> "DatasetInfo":
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in dataset_info_dict.items() if k in field_names})

    def update(self, other_dataset_info: "DatasetInfo", ignore_none=True):
        self_dict = self.__dict__
        self_dict.update(
            **{
                k: copy.deepcopy(v)
                for k, v in other_dataset_info.__dict__.items()
                if (v is not None or not ignore_none)
            }
        )

    def copy(self) -> "DatasetInfo":
        return self.__class__(**{k: copy.deepcopy(v) for k, v in self.__dict__.items()})


class DatasetInfosDict(dict):
    def write_to_directory(self, dataset_infos_dir, overwrite=False):
        total_dataset_infos = {}
        dataset_infos_path = os.path.join(dataset_infos_dir, config.DATASETDICT_INFOS_FILENAME)
        if os.path.exists(dataset_infos_path) and not overwrite:
            logger.info("Dataset Infos already exists in {}. Completing it with new infos.".format(dataset_infos_dir))
            total_dataset_infos = self.from_directory(dataset_infos_dir)
        else:
            logger.info("Writing new Dataset Infos in {}".format(dataset_infos_dir))
        total_dataset_infos.update(self)
        with open(dataset_infos_path, "w", encoding="utf-8") as f:
            json.dump({config_name: asdict(dset_info) for config_name, dset_info in total_dataset_infos.items()}, f)

    @classmethod
    def from_directory(cls, dataset_infos_dir):
        logger.info("Loading Dataset Infos from {}".format(dataset_infos_dir))
        with open(os.path.join(dataset_infos_dir, config.DATASETDICT_INFOS_FILENAME), "r", encoding="utf-8") as f:
            dataset_infos_dict = {
                config_name: DatasetInfo.from_dict(dataset_info_dict)
                for config_name, dataset_info_dict in json.load(f).items()
            }
        return cls(**dataset_infos_dict)


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
    license: str = field(default_factory=str)
    codebase_urls: List[str] = field(default_factory=list)
    reference_urls: List[str] = field(default_factory=list)
    streamable: bool = False
    format: Optional[str] = None

    # Set later by the builder
    metric_name: Optional[str] = None
    config_name: Optional[str] = None
    experiment_id: Optional[str] = None

    def __post_init__(self):
        assert "predictions" in self.features, "Need to have at least a 'predictions' field in 'features'."
        if self.format is not None:
            for key, value in self.features.items():
                if not isinstance(value, Value):
                    raise ValueError(
                        f"When using 'numpy' format, all features should be a `datasets.Value` feature. "
                        f"Here {key} is an instance of {value.__class__.__name__}"
                    )

    def write_to_directory(self, metric_info_dir):
        """Write `MetricInfo` as JSON to `metric_info_dir`.
        Also save the license separately in LICENCE.
        """
        with open(os.path.join(metric_info_dir, config.METRIC_INFO_FILENAME), "w", encoding="utf-8") as f:
            json.dump(asdict(self), f)

        with open(os.path.join(metric_info_dir, config.LICENSE_FILENAME), "w", encoding="utf-8") as f:
            f.write(self.license)

    @classmethod
    def from_directory(cls, metric_info_dir) -> "MetricInfo":
        """Create MetricInfo from the JSON file in `metric_info_dir`.

        Args:
            metric_info_dir: `str` The directory containing the metadata file. This
                should be the root directory of a specific dataset version.
        """
        logger.info("Loading Metric info from %s", metric_info_dir)
        if not metric_info_dir:
            raise ValueError("Calling MetricInfo.from_directory() with undefined metric_info_dir.")

        with open(os.path.join(metric_info_dir, config.METRIC_INFO_FILENAME), "r", encoding="utf-8") as f:
            metric_info_dict = json.load(f)
        return cls.from_dict(metric_info_dict)

    @classmethod
    def from_dict(cls, metric_info_dict: dict) -> "MetricInfo":
        field_names = set(f.name for f in dataclasses.fields(cls))
        return cls(**{k: v for k, v in metric_info_dict.items() if k in field_names})
