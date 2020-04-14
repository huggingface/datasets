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
"""XNLI: The Cross-Lingual NLI Corpus."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import csv
import os
import six

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """\
@InProceedings{conneau2018xnli,
  author = "Conneau, Alexis
                 and Rinott, Ruty
                 and Lample, Guillaume
                 and Williams, Adina
                 and Bowman, Samuel R.
                 and Schwenk, Holger
                 and Stoyanov, Veselin",
  title = "XNLI: Evaluating Cross-lingual Sentence Representations",
  booktitle = "Proceedings of the 2018 Conference on Empirical Methods
               in Natural Language Processing",
  year = "2018",
  publisher = "Association for Computational Linguistics",
  location = "Brussels, Belgium",
}"""

_DESCRIPTION = """\
XNLI is a subset of a few thousand examples from MNLI which has been translated
into a 14 different languages (some low-ish resource). As with MNLI, the goal is
to predict textual entailment (does sentence A imply/contradict/neither sentence
B) and is a classification task (given two sentences, predict one of three
labels).
"""

_DATA_URL = 'https://www.nyu.edu/projects/bowman/xnli/XNLI-1.0.zip'

_LANGUAGES = ('ar', 'bg', 'de', 'el', 'en', 'es', 'fr', 'hi', 'ru', 'sw', 'th',
              'tr', 'ur', 'vi', 'zh')


class Xnli(tfds.core.GeneratorBasedBuilder):
  """XNLI: The Cross-Lingual NLI Corpus. Version 1.0."""
  BUILDER_CONFIGS = [
      tfds.core.BuilderConfig(
          name='plain_text',
          version=tfds.core.Version(
              '1.0.0',
              'New split API (https://tensorflow.org/datasets/splits)'),
          description='Plain text import of XNLI',
      )
  ]

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'premise':
                tfds.features.Translation(
                    languages=_LANGUAGES,),
            'hypothesis':
                tfds.features.TranslationVariableLanguages(
                    languages=_LANGUAGES,),
            'label':
                tfds.features.ClassLabel(
                    names=['entailment', 'neutral', 'contradiction']),
        }),
        # No default supervised_keys (as we have to pass both premise
        # and hypothesis as input).
        supervised_keys=None,
        homepage='https://www.nyu.edu/projects/bowman/xnli/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    dl_dir = dl_manager.download_and_extract(_DATA_URL)
    data_dir = os.path.join(dl_dir, 'XNLI-1.0')
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            gen_kwargs={'filepath': os.path.join(data_dir, 'xnli.test.tsv')}),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            gen_kwargs={'filepath': os.path.join(data_dir, 'xnli.dev.tsv')}),
    ]

  def _generate_examples(self, filepath):
    """This function returns the examples in the raw (text) form."""
    rows_per_pair_id = collections.defaultdict(list)

    with tf.io.gfile.GFile(filepath) as f:
      reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
      for row in reader:
        rows_per_pair_id[row['pairID']].append(row)

    for rows in six.itervalues(rows_per_pair_id):
      premise = {row['language']: row['sentence1'] for row in rows}
      hypothesis = {row['language']: row['sentence2'] for row in rows}
      yield rows[0]['pairID'], {
          'premise': premise,
          'hypothesis': hypothesis,
          'label': rows[0]['gold_label'],
      }
