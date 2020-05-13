# flake8: noqa
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
# pylint: enable=line-too-long
# pylint: disable=g-import-not-at-top,g-bad-import-order,wrong-import-position

__version__ = "0.0.3"

from pyarrow import total_allocated_bytes

from . import datasets
from .arrow_dataset import Dataset
from .arrow_reader import ReadInstruction
from .builder import ArrowBasedBuilder, BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder
from .features import ClassLabel, Features, Sequence, Tensor, Translation, TranslationVariableLanguages, Value
from .info import DatasetInfo, MetricInfo
from .inspect import inspect_dataset, inspect_metric, list_datasets, list_metrics
from .load import import_main_class, load_dataset, load_metric, prepare_module
from .metric import Metric
from .splits import NamedSplit, Split, SplitBase, SplitDict, SplitGenerator, SplitInfo, SubSplitInfo, percent
from .utils import *
from .utils.tqdm_utils import disable_progress_bar
