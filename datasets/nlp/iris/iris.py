# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
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
"""Iris dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import nlp

IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

_CITATION = """\
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences"
}
"""

_DESCRIPTION = """\
This is perhaps the best known database to be found in the pattern recognition
literature. Fisher's paper is a classic in the field and is referenced
frequently to this day. (See Duda & Hart, for example.) The data set contains
3 classes of 50 instances each, where each class refers to a type of iris
plant. One class is linearly separable from the other 2; the latter are NOT
linearly separable from each other.
"""


class Iris(nlp.GeneratorBasedBuilder):
  """Iris flower dataset."""
  NUM_CLASSES = 3
  VERSION = nlp.Version(
      "2.0.0", "New split API (https://tensorflow.org/datasets/splits)")

  def _info(self):
    return nlp.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        # nlp.features.FeatureConnectors
        features=nlp.features.FeaturesDict({
            "features":
                nlp.features.Tensor(shape=(4,), dtype=nlp.float32),
            # Here, labels can be one of 3 classes
            "label":
                nlp.features.ClassLabel(
                    names=["Iris-setosa", "Iris-versicolor", "Iris-virginica"]),
        }),
        supervised_keys=("features", "label"),
        homepage="https://archive.ics.uci.edu/ml/datasets/iris",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    iris_file = dl_manager.download(IRIS_URL)
    all_lines = open(iris_file).read().split("\n")
    records = [l for l in all_lines if l]  # get rid of empty lines

    # Specify the splits
    return [
        nlp.SplitGenerator(
            name=nlp.Split.TRAIN,
            gen_kwargs={"records": records}),
    ]

  def _generate_examples(self, records):
    for i, row in enumerate(records):
      elems = row.split(",")
      yield i, {
          "features": [float(e) for e in elems[:-1]],
          "label": elems[-1],
      }
