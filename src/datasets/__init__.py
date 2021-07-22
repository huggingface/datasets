# flake8: noqa
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
# pylint: enable=line-too-long
# pylint: disable=g-import-not-at-top,g-bad-import-order,wrong-import-position

__version__ = "1.10.2.dev0"

import pyarrow
from pyarrow import total_allocated_bytes


if tuple(int(i) for i in pyarrow.__version__.split(".")) < (1, 0, 0):
    raise ImportWarning(
        "To use `datasets`, the module `pyarrow>=1.0.0` is required, and the current version of `pyarrow` doesn't match this condition.\n"
        "If you are running this in a Google Colab, you should probably just restart the runtime to use the right version of `pyarrow`."
    )

from .arrow_dataset import Dataset, concatenate_datasets
from .arrow_reader import ArrowReader, ReadInstruction
from .arrow_writer import ArrowWriter
from .builder import ArrowBasedBuilder, BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from .combine import interleave_datasets
from .dataset_dict import DatasetDict, IterableDatasetDict
from .features import (
    Array2D,
    Array3D,
    Array4D,
    Array5D,
    ClassLabel,
    Features,
    Sequence,
    Translation,
    TranslationVariableLanguages,
    Value,
)
from .fingerprint import is_caching_enabled, set_caching_enabled
from .info import DatasetInfo, MetricInfo
from .inspect import (
    get_dataset_config_names,
    get_dataset_infos,
    inspect_dataset,
    inspect_metric,
    list_datasets,
    list_metrics,
)
from .iterable_dataset import IterableDataset
from .keyhash import KeyHasher
from .load import import_main_class, load_dataset, load_dataset_builder, load_from_disk, load_metric, prepare_module
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
from .utils import *


SCRIPTS_VERSION = "master" if __version__.split(".")[-1].startswith("dev") else __version__
