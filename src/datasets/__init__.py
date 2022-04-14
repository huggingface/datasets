# flake8: noqa
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

__version__ = "2.1.0"

import pyarrow
from packaging import version


if version.parse(pyarrow.__version__).major < 5:
    raise ImportWarning(
        "To use `datasets`, the module `pyarrow>=5.0.0` is required, and the current version of `pyarrow` doesn't match this condition.\n"
        "If you are running this in a Google Colab, you should probably just restart the runtime to use the right version of `pyarrow`."
    )

SCRIPTS_VERSION = "master" if version.parse(__version__).is_devrelease else __version__

del pyarrow
del version

from .arrow_dataset import Dataset, concatenate_datasets
from .arrow_reader import ReadInstruction
from .builder import ArrowBasedBuilder, BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from .combine import interleave_datasets
from .dataset_dict import DatasetDict, IterableDatasetDict
from .features import *
from .fingerprint import disable_caching, enable_caching, is_caching_enabled, set_caching_enabled
from .info import DatasetInfo, MetricInfo
from .inspect import (
    get_dataset_config_info,
    get_dataset_config_names,
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
