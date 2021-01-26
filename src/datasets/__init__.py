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

__version__ = "1.2.1"

import pyarrow
from pyarrow import total_allocated_bytes


if tuple(int(i) for i in pyarrow.__version__.split(".")) < (0, 17, 1):
    raise ImportWarning(
        "To use `datasets`, the module `pyarrow>=0.17.1` is required, and the current version of `pyarrow` doesn't match this condition.\n"
        "If you are running this in a Google Colab, you should probably just restart the runtime to use the right version of `pyarrow`."
    )

from .arrow_dataset import Dataset, concatenate_datasets
from .arrow_reader import ArrowReader, ReadInstruction
from .arrow_writer import ArrowWriter
from .builder import ArrowBasedBuilder, BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from .dataset_dict import DatasetDict
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
from .load import import_main_class, load_dataset, load_from_disk, load_metric, prepare_module
from .metric import Metric
from .splits import NamedSplit, Split, SplitBase, SplitDict, SplitGenerator, SplitInfo, SubSplitInfo, percent
from .utils import *
from .utils.tqdm_utils import disable_progress_bar


SCRIPTS_VERSION = "master"
