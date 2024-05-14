# ruff: noqa
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

__version__ = "2.19.2.dev0"

from .arrow_dataset import Dataset
from .arrow_reader import ReadInstruction
from .builder import ArrowBasedBuilder, BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from .combine import concatenate_datasets, interleave_datasets
from .dataset_dict import DatasetDict, IterableDatasetDict
from .download import *
from .features import *
from .fingerprint import disable_caching, enable_caching, is_caching_enabled, set_caching_enabled
from .info import DatasetInfo, MetricInfo
from .inspect import (
    get_dataset_config_info,
    get_dataset_config_names,
    get_dataset_default_config_name,
    get_dataset_infos,
    get_dataset_split_names,
    inspect_dataset,
    inspect_metric,
    list_datasets,
    list_metrics,
)
from .iterable_dataset import IterableDataset
from .load import load_dataset, load_dataset_builder, load_from_disk, load_metric
from .metric import Metric
from .splits import (
    NamedSplit,
    NamedSplitAll,
    Split,
    SplitBase,
    SplitDict,
    SplitGenerator,
    SplitInfo,
    SubSplitInfo,
    percent,
)
from .tasks import *
from .utils import *
from .utils import logging


# deprecated modules
from datasets import arrow_dataset as _arrow_dataset  # isort:skip
from datasets import utils as _utils  # isort:skip
from datasets.utils import download_manager as _deprecated_download_manager  # isort:skip

_arrow_dataset.concatenate_datasets = concatenate_datasets
_utils.DownloadConfig = DownloadConfig
_utils.DownloadManager = DownloadManager
_utils.DownloadMode = DownloadMode
_deprecated_download_manager.DownloadConfig = DownloadConfig
_deprecated_download_manager.DownloadMode = DownloadMode
_deprecated_download_manager.DownloadManager = DownloadManager

del _arrow_dataset, _utils, _deprecated_download_manager

__all__ = [
    "DatasetInfo",
    "Dataset",
    "DatasetDict",
    "IterableDataset",
    "IterableDatasetDict",
    "Features",
    "Sequence",
    "ClassLabel",
    "Value",
    "Translation",
    "TranslationVariableLanguages",
    "Array2D",
    "Array3D",
    "Array4D",
    "Array5D",
    "Audio",
    "Image",
    "MetricInfo",
    "Metric",
    "DatasetBuilder",
    "GeneratorBasedBuilder",
    "BeamBasedBuilder",
    "ArrowBasedBuilder",
    "BuilderConfig",
    "DownloadManager",
    "StreamingDownloadManager",
    "DownloadConfig",
    "DownloadMode",
    "SplitGenerator",
    "Split",
    "NamedSplit",
    "NamedSplitAll",
    "ReadInstruction",
    "Version",
    "list_datasets",
    "load_dataset",
    "load_from_disk",
    "load_dataset_builder",
    "get_dataset_config_names",
    "get_dataset_infos",
    "get_dataset_split_names",
    "inspect_dataset",
    "list_metrics",
    "load_metrics",
    "inspect_metric",
    "enable_progress_bar",
    "disable_progress_bar",
    "is_progress_bar_enabled",
    "AutomaticSpeechRecognition",
    "AudioClassification",
    "ImageClassification",
    "LanguageModelling",
    "QuestionAnsweringExtractive",
    "Summarization",
    "TextClassification",
]
