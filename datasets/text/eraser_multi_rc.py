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
"""Passage, query, answers and answer classification with explanations."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os
import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION = """
@unpublished{eraser2019,
    title = {ERASER: A Benchmark to Evaluate Rationalized NLP Models},
    author = {Jay DeYoung and Sarthak Jain and Nazneen Fatema Rajani and Eric Lehman and Caiming Xiong and Richard Socher and Byron C. Wallace}
}
@inproceedings{MultiRC2018,
    author = {Daniel Khashabi and Snigdha Chaturvedi and Michael Roth and Shyam Upadhyay and Dan Roth},
    title = {Looking Beyond the Surface:A Challenge Set for Reading Comprehension over Multiple Sentences},
    booktitle = {NAACL},
    year = {2018}
}
"""

_DESCRIPTION = """
Eraser Multi RC is a dataset for queries over multi-line passages, along with
answers and a rationalte. Each example in this dataset has the following 5 parts
1. A Mutli-line Passage
2. A Query about the passage
3. An Answer to the query
4. A Classification as to whether the answer is right or wrong
5. An Explanation justifying the classification
"""

_DOWNLOAD_URL = 'http://www.eraserbenchmark.com/zipped/multirc.tar.gz'


class EraserMultiRc(tfds.core.GeneratorBasedBuilder):
  """Multi Sentence Reasoning with Explanations (Eraser Benchmark)."""

  VERSION = tfds.core.Version('0.1.1')

  def _info(self):
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'passage': tfds.features.Text(),
            'query_and_answer': tfds.features.Text(),
            'label': tfds.features.ClassLabel(names=['False', 'True']),
            'evidences': tfds.features.Sequence(tfds.features.Text())
        }),
        supervised_keys=None,
        homepage='https://cogcomp.seas.upenn.edu/multirc/',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Returns SplitGenerators."""

    dl_dir = dl_manager.download_and_extract(_DOWNLOAD_URL)
    data_dir = os.path.join(dl_dir, 'multirc')
    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={'data_dir': data_dir,
                        'filepath': os.path.join(data_dir, 'train.jsonl')},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.VALIDATION,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={'data_dir': data_dir,
                        'filepath': os.path.join(data_dir, 'val.jsonl')},
        ),
        tfds.core.SplitGenerator(
            name=tfds.Split.TEST,
            # These kwargs will be passed to _generate_examples
            gen_kwargs={'data_dir': data_dir,
                        'filepath': os.path.join(data_dir, 'test.jsonl')},
        ),
    ]

  def _generate_examples(self, data_dir, filepath):
    """Yields examples."""

    multirc_dir = os.path.join(data_dir, 'docs')
    with tf.io.gfile.GFile(filepath) as f:
      for line in f:
        row = json.loads(line)
        evidences = []

        for evidence in row['evidences'][0]:
          docid = evidence['docid']
          evidences.append(evidence['text'])

        passage_file = os.path.join(multirc_dir, docid)
        with tf.io.gfile.GFile(passage_file) as f1:
          passage_text = f1.read()

        yield row['annotation_id'], {
            'passage': passage_text,
            'query_and_answer': row['query'],
            'label': row['classification'],
            'evidences': evidences
        }
