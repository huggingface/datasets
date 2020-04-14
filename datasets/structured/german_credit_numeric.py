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
"""German Credit (numeric) dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data-numeric"

_CITATION = """\
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences"
}
"""

_DESCRIPTION = """
This dataset classifies people described by a set of attributes as good or bad
credit risks. The version here is the "numeric" variant where categorical and
ordered categorical attributes have been encoded as indicator and integer
quantities respectively.
"""


class GermanCreditNumeric(tfds.core.GeneratorBasedBuilder):
  """German Credit (numeric) dataset."""

  VERSION = tfds.core.Version("1.0.0")

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            "features":
                tfds.features.Tensor(shape=(24,), dtype=tf.int32),
            "label":
                tfds.features.ClassLabel(names=["Bad", "Good"]),
        }),
        supervised_keys=("features", "label"),
        homepage="https://archive.ics.uci.edu/ml/datasets/Statlog+(German+Credit+Data)",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    data_file = dl_manager.download(URL)
    with tf.io.gfile.GFile(data_file) as f:
      all_lines = f.read().split("\n")
    records = [l for l in all_lines if l]  # get rid of empty lines

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={"records": records}),
    ]

  def _generate_examples(self, records):
    """Yields examples."""
    for i, row in enumerate(records):
      elems = row.split()
      yield i, {
          "features": [int(e) for e in elems[:-1]],
          "label": 2 - int(elems[-1]),
      }
