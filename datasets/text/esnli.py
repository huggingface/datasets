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
"""e-SNLI: Natural Language Inference with Natural Language Explanations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import csv
import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
@incollection{NIPS2018_8163,
title = {e-SNLI: Natural Language Inference with Natural Language Explanations},
author = {Camburu, Oana-Maria and Rockt\"{a}schel, Tim and Lukasiewicz, Thomas and Blunsom, Phil},
booktitle = {Advances in Neural Information Processing Systems 31},
editor = {S. Bengio and H. Wallach and H. Larochelle and K. Grauman and N. Cesa-Bianchi and R. Garnett},
pages = {9539--9549},
year = {2018},
publisher = {Curran Associates, Inc.},
url = {http://papers.nips.cc/paper/8163-e-snli-natural-language-inference-with-natural-language-explanations.pdf}
}
"""

_DESCRIPTION = """
The e-SNLI dataset extends the Stanford Natural Language Inference Dataset to
include human-annotated natural language explanations of the entailment
relations.
"""
_URL = 'https://raw.githubusercontent.com/OanaMariaCamburu/e-SNLI/master/dataset/'


class Esnli(tfds.core.GeneratorBasedBuilder):
  """e-SNLI: Natural Language Inference with Natural Language Explanations corpus."""

  # Version History
  # 0.0.2 Added explanation_2, explanation_3 fields which exist in the dev/test
  # splits only.
  # 0.0.1 Initial version
  BUILDER_CONFIGS = [
      tfds.core.BuilderConfig(
          name='plain_text',
          version=tfds.core.Version('0.0.2'),
          description='Plain text import of e-SNLI',
      )
  ]

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'premise':
                tfds.features.Text(),
            'hypothesis':
                tfds.features.Text(),
            'label':
                tfds.features.ClassLabel(
                    names=['entailment', 'neutral', 'contradiction']),
            'explanation_1':
                tfds.features.Text(),
            'explanation_2':
                tfds.features.Text(),
            'explanation_3':
                tfds.features.Text(),
        }),
        supervised_keys=None,
        homepage='https://github.com/OanaMariaCamburu/e-SNLI',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""

    files = dl_manager.download_and_extract({
        'train': [os.path.join(_URL, 'esnli_train_1.csv'),
                  os.path.join(_URL, 'esnli_train_2.csv')],
        'validation': [os.path.join(_URL, 'esnli_dev.csv')],
        'test': [os.path.join(_URL, 'esnli_test.csv')]
    })

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={'files': files['train']},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={'files': files['validation']},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={'files': files['test']},
        ),
    ]

  def _generate_examples(self, files):
    """Yields examples."""
    for filepath in files:
      with tf.io.gfile.GFile(filepath) as f:
        reader = csv.DictReader(f)
        for _, row in enumerate(reader):
          yield row['pairID'], {
              'premise': row['Sentence1'],
              'hypothesis': row['Sentence2'],
              'label': row['gold_label'],
              'explanation_1': row['Explanation_1'],
              'explanation_2': row.get('Explanation_2', ''),
              'explanation_3': row.get('Explanation_3', ''),
          }
