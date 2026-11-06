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

__version__ = "5.2.0.dev0"

# Explicit aliases mark public re-exports for type checkers.
from .arrow_dataset import Column as Column
from .arrow_dataset import Dataset as Dataset
from .arrow_reader import ReadInstruction as ReadInstruction
from .builder import ArrowBasedBuilder as ArrowBasedBuilder
from .builder import BuilderConfig as BuilderConfig
from .builder import DatasetBuilder as DatasetBuilder
from .builder import GeneratorBasedBuilder as GeneratorBasedBuilder
from .combine import concatenate_datasets as concatenate_datasets
from .combine import interleave_datasets as interleave_datasets
from .dataset_dict import DatasetDict as DatasetDict
from .dataset_dict import IterableDatasetDict as IterableDatasetDict
from .download import *
from .features import *
from .fingerprint import disable_caching as disable_caching
from .fingerprint import enable_caching as enable_caching
from .fingerprint import is_caching_enabled as is_caching_enabled
from .info import DatasetInfo as DatasetInfo
from .inspect import get_dataset_config_info as get_dataset_config_info
from .inspect import get_dataset_config_names as get_dataset_config_names
from .inspect import get_dataset_default_config_name as get_dataset_default_config_name
from .inspect import get_dataset_infos as get_dataset_infos
from .inspect import get_dataset_split_names as get_dataset_split_names
from .iterable_dataset import IterableColumn as IterableColumn
from .iterable_dataset import IterableDataset as IterableDataset
from .load import load_dataset as load_dataset
from .load import load_dataset_builder as load_dataset_builder
from .load import load_from_disk as load_from_disk
from .splits import NamedSplit as NamedSplit
from .splits import NamedSplitAll as NamedSplitAll
from .splits import Split as Split
from .splits import SplitBase as SplitBase
from .splits import SplitDict as SplitDict
from .splits import SplitGenerator as SplitGenerator
from .splits import SplitInfo as SplitInfo
from .splits import SubSplitInfo as SubSplitInfo
from .splits import percent as percent
from .utils import *
from .utils import logging as logging
