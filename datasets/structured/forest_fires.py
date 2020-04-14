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
"""Forest fires dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = r"""
@misc{Dua:2019 ,
author = "Dua, Dheeru and Graff, Casey",
year = "2017",
title = "{UCI} Machine Learning Repository",
url = "http://archive.ics.uci.edu/ml",
institution = "University of California, Irvine, School of Information and Computer Sciences" }

@article{cortez2007data,
  title={A data mining approach to predict forest fires using meteorological data},
  author={Cortez, Paulo and Morais, Anibal de Jesus Raimundo},
  year={2007},
  publisher={Associa{\c{c}}{\~a}o Portuguesa para a Intelig{\^e}ncia Artificial (APPIA)}
}
"""

_DESCRIPTION = """

This is a regression task, where the aim is to predict the burned area of
forest fires, in the northeast region of Portugal,
by using meteorological and other data.


Data Set Information:

In [Cortez and Morais, 2007], the output 'area' was first transformed
with a ln(x+1) function.
Then, several Data Mining methods were applied. After fitting the models,
the outputs were
post-processed with the inverse of the ln(x+1) transform. Four different
input setups were
used. The experiments were conducted using a 10-fold (cross-validation)
x 30 runs. Two
regression metrics were measured: MAD and RMSE. A Gaussian support vector
machine (SVM) fed
with only 4 direct weather conditions (temp, RH, wind and rain) obtained
the best MAD value:
12.71 +- 0.01 (mean and confidence interval within 95% using a t-student
distribution). The
best RMSE was attained by the naive mean predictor. An analysis to the
regression error curve
(REC) shows that the SVM model predicts more examples within a lower
admitted error. In effect,
the SVM model predicts better small fires, which are the majority.

Attribute Information:

For more information, read [Cortez and Morais, 2007].

1. X - x-axis spatial coordinate within the Montesinho park map: 1 to 9
2. Y - y-axis spatial coordinate within the Montesinho park map: 2 to 9
3. month - month of the year: 'jan' to 'dec'
4. day - day of the week: 'mon' to 'sun'
5. FFMC - FFMC index from the FWI system: 18.7 to 96.20
6. DMC - DMC index from the FWI system: 1.1 to 291.3
7. DC - DC index from the FWI system: 7.9 to 860.6
8. ISI - ISI index from the FWI system: 0.0 to 56.10
9. temp - temperature in Celsius degrees: 2.2 to 33.30
10. RH - relative humidity in %: 15.0 to 100
11. wind - wind speed in km/h: 0.40 to 9.40
12. rain - outside rain in mm/m2 : 0.0 to 6.4
13. area - the burned area of the forest (in ha): 0.00 to 1090.84
(this output variable is very skewed towards 0.0, thus it may make
sense to model with the logarithm transform).

"""

_MONTHS = [
    'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov',
    'dec'
]

_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/forest-fires/forestfires.csv'

FEATURES = collections.OrderedDict([
    ('X', tf.uint8),
    ('Y', tf.uint8),
    ('month', tfds.features.ClassLabel(names=_MONTHS)),
    ('day', tfds.features.ClassLabel(names=_DAYS)),
    ('FFMC', tf.float32),
    ('DMC', tf.float32),
    ('DC', tf.float32),
    ('ISI', tf.float32),
    ('temp', tf.float32),
    ('RH', tf.float32),
    ('wind', tf.float32),
    ('rain', tf.float32),
])


class ForestFires(tfds.core.GeneratorBasedBuilder):
  """Regression task aimed to predict the burned area of forest fires."""

  VERSION = tfds.core.Version('0.0.1')

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'area': tf.float32,
            'features': {name: dtype for name, dtype in FEATURES.items()}
        }),
        supervised_keys=('area', 'features'),
        homepage='https://archive.ics.uci.edu/ml/datasets/Forest+Fires',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""
    data = dl_manager.download(_URL)

    # There is no predefined train/val/test split for this dataset.
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={'file_path': data},
        ),
    ]

  def _generate_examples(self, file_path):
    """Yields examples."""
    with tf.io.gfile.GFile(file_path) as f:
      raw_data = csv.DictReader(f)
      for i, row in enumerate(raw_data):
        yield i, {
            'area': row.pop('area'),
            'features': {name: value for name, value in row.items()},
        }
