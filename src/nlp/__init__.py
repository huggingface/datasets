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
# pylint: disable=line-too-long
"""`nlp` defines a collection of datasets ready-to-use.

Each dataset is defined as a `nlp.DatasetBuilder`, which encapsulates
the logic to download the dataset and construct an input pipeline, as well as
contains the dataset documentation (version, splits, number of examples, etc.).

The main library entrypoints are:

* `nlp.builder`: fetch a `nlp.DatasetBuilder` by name
* `nlp.load`: convenience method to construct a builder, download the data, and
    create an input pipeline, returning an NLP dataset.

"""
# pylint: enable=line-too-long
# pylint: disable=g-import-not-at-top,g-bad-import-order,wrong-import-position

__version__ = "0.0.1"

# Types are pyarrow types
from pyarrow import (null, bool_,
                     int8, int16, int32, int64,
                     uint8, uint16, uint32, uint64,
                     time32, time64, timestamp, date32, date64, duration,
                     float16, float32, float64,
                     binary, string, utf8,
                     large_binary, large_string, large_utf8,
                     decimal128,
                     list_, large_list, map_, struct, union, dictionary)
from pyarrow import total_allocated_bytes

from . import download, features, load, datasets
from .load import builder, load
from .download import GenerateMode
from .arrow_dataset import Dataset
from .splits import percent
from .splits import Split
from .utils.tqdm_utils import disable_progress_bar

from .builder import BeamBasedBuilder, BuilderConfig, DatasetBuilder, GeneratorBasedBuilder

from .info import DatasetInfo

from .lazy_imports_lib import lazy_imports

from .splits import NamedSplit, SplitBase, SplitDict, SplitGenerator, SplitInfo, SubSplitInfo

from .arrow_reader import ReadInstruction

from .utils import *
