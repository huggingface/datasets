# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
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
"""Titanic dataset.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import numpy as np
import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
@ONLINE {titanic,
author = "Frank E. Harrell Jr., Thomas Cason",
title  = "Titanic dataset",
month  = "oct",
year   = "2017",
url    = "https://www.openml.org/d/40945"
}
"""

_DESCRIPTION = ("Dataset describing the survival status of "
                "individual passengers on the Titanic. Missing values in "
                "the original dataset are represented using ?. "
                "Float and int missing values are replaced with -1, string "
                "missing values are replaced with 'Unknown'.")

_EMBARKED_DICT = collections.OrderedDict([
    ("C", "Cherbourg"), ("Q", "Queenstown"), ("S", "Southampton"),
    ("?", "Unknown")
])

_PCLASS_DICT = collections.OrderedDict([
    ("1", "1st_class"), ("2", "2nd_class"), ("3", "3rd_class")
])

_SURVIVED_DICT = {"1": "survived", "0": "died"}


def convert_to_float(d):
  return -1.0 if d == "?" else np.float32(d)


def convert_to_int(d):
  return -1 if d == "?" else np.int32(d)


def convert_to_string(d):
  return "Unknown" if d == "?" else d


def convert_to_label(d, dictionary):
  return dictionary[d]


def return_same(d):
  return d


FEATURE_DICT = collections.OrderedDict([
    ("pclass", (tfds.features.ClassLabel(names=_PCLASS_DICT.values()),
                lambda d: convert_to_label(d, _PCLASS_DICT))),
    ("name", (tf.string, convert_to_string)),
    ("sex", (tfds.features.ClassLabel(names=["male", "female"]), return_same)),
    ("age", (tf.float32, convert_to_float)),
    ("sibsp", (tf.int32, convert_to_int)),
    ("parch", (tf.int32, convert_to_int)),
    ("ticket", (tf.string, convert_to_string)),
    ("fare", (tf.float32, convert_to_float)),
    ("cabin", (tf.string, convert_to_string)),
    ("embarked", (tfds.features.ClassLabel(names=_EMBARKED_DICT.values()),
                  lambda d: convert_to_label(d, _EMBARKED_DICT))),
    ("boat", (tf.string, convert_to_string)),
    ("body", (tf.int32, convert_to_int)),
    ("home.dest", (tf.string, convert_to_string))
])

_URL = "https://www.openml.org/data/get_csv/16826755/phpMYEkMl"


class Titanic(tfds.core.GeneratorBasedBuilder):
  """Titanic dataset."""
  VERSION = tfds.core.Version(
      "2.0.0", "New split API (https://tensorflow.org/datasets/splits)")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "survived": tfds.features.ClassLabel(names=["died", "survived"]),
            "features": {name: dtype
                         for name, (dtype, func) in FEATURE_DICT.items()}
        }),
        supervised_keys=("features", "survived"),
        homepage="https://www.openml.org/d/40945",
        citation=_CITATION
        )

  def _split_generators(self, dl_manager):
    path = dl_manager.download(_URL)

    # There is no predefined train/val/test split for this dataset.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "file_path": path
            }),
    ]

  def _generate_examples(self, file_path):
    """Generate features and target given the directory path.

    Args:
      file_path: path where the csv file is stored

    Yields:
      The features and the target
    """

    with tf.io.gfile.GFile(file_path) as f:
      raw_data = csv.DictReader(f)
      for i, row in enumerate(raw_data):
        survive_val = row.pop("survived")
        yield i, {
            "survived": convert_to_label(survive_val, _SURVIVED_DICT),
            "features": {
                name: FEATURE_DICT[name][1](value)
                for name, value in row.items()
            }
        }
